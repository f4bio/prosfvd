import fnmatch
import os
import configparser
from mod import logger

## vars
from mod.hashing import crc32

__author__ = "ft2011@gmail.com"
baseDir = os.path.dirname(os.path.abspath(__file__))

## config
config = configparser.ConfigParser()
config.read(os.path.join(baseDir, "../config.ini"))

tmpFileName = str(".prosfvd-tmp")

missingStyle = str(config.get("style", "missing"))
brokenStyle = str(config.get("style", "broken"))
statusStyle = str(config.get("style", "status"))

## system:
logLevel = config.get("log", "level")
log = logger.getLogger("handle", logLevel)


def parseSfv(filePath):
    log.debug("searching sfv in: '" + os.path.dirname(filePath) + "'")

    sfv = {}
    folderPath = os.path.dirname(filePath)

    for root, dirs, files in os.walk(folderPath):
        for name in files:
            if fnmatch.fnmatch(name, "*.sfv"):
                sfvPath = os.path.join(root, name)
                with open(sfvPath, "r") as sp:
                    for line in sp.readlines():
                        fileName, crcValue = line.split(" ")
                        sfv[str(fileName).strip()] = str(crcValue).strip()
                return sfv


def getFormattedMissing(filePath):
    missingName = str(missingStyle).format(os.path.basename(filePath))
    return os.path.join(os.path.dirname(filePath), missingName)


def getFormattedBroken(filePath):
    brokenName = str(brokenStyle).format(os.path.basename(filePath))
    return os.path.join(os.path.dirname(filePath), brokenName)


def getFormattedStatus(cntTotal, cntMissing, cntBroken):
    cntComplete = (cntTotal - cntMissing - cntBroken)
    pctComplete = (cntComplete / cntTotal) * 100
    pctMissing = (cntMissing / cntTotal) * 100
    pctBroken = (cntBroken / cntTotal) * 100

    return statusStyle.format(cntTotal, cntComplete, cntMissing, cntBroken, pctComplete, pctMissing, pctBroken)


def show(filePath):
    log.debug("showing status in: '" + os.path.dirname(filePath) + "'")

    cntTotal = 0
    cntMissing = 0
    cntBroken = 0

    sfv = parseSfv(filePath)
    working = os.path.dirname(filePath)

    for key in sfv.keys():
        tmp = os.path.join(os.path.dirname(filePath), key)
        missing = getFormattedMissing(tmp)
        broken = getFormattedBroken(tmp)

        if os.path.exists(missing):
            cntMissing += 1
        elif os.path.exists(broken):
            cntBroken += 1

        cntTotal += 1

    statusFormatted = getFormattedStatus(cntTotal, cntMissing, cntBroken)
    tmpFile = os.path.join(working, tmpFileName)

    if os.path.exists(tmpFile):
        with open(tmpFile, "r") as tF:
            os.rmdir(os.path.join(working, tF.readline()))

    with open(tmpFile, "w") as tF:
        tF.write(statusFormatted)
        os.mkdir(os.path.join(working, statusFormatted))


def sfv(sfvPath):
    log.debug("processing sfv: '" + sfvPath + "'")
    sfv = parseSfv(sfvPath)
    for kv in sfv.items():
        missing = os.path.join(os.path.dirname(sfvPath), missingStyle.format(kv[0]))
        with open(missing, "w") as m:
            m.write(kv[1])

    show(sfvPath)


def file(filePath):
    log.debug("processing file: '{0}' - '{1}'".format(filePath, str(os.path.basename(filePath))))
    sfv = parseSfv(filePath)

    if not sfv:
        log.debug("no sfv found at '{0}' - skipping...".format(os.path.basename(filePath)))
        return

    if not str(os.path.basename(filePath)) in sfv:
        log.debug("file '{0}' not in sfv - skipping...".format(os.path.basename(filePath)))
        return

    # get hashes
    hashCalc = crc32(filePath).strip()
    hashList = sfv.get(os.path.basename(filePath))

    # init missing-file and broken-file
    missing = getFormattedMissing(filePath)
    broken = getFormattedBroken(filePath)

    # get hash from sfv-file, saved in missing-file or broken-file and remove file
    if os.path.exists(missing):
        os.remove(missing)

    if os.path.exists(broken):
        os.remove(broken)

    # remove file (no resume!?) and create broken-file if not same hash
    if hashCalc != hashList:
        with open(broken, "w") as b:
            b.write(hashList)
        os.remove(filePath)

    show(filePath)
