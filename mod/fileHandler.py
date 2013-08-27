import os
import configparser
from mod import hashing
from mod import logger

## vars
__author__ = "ft2011 (teeee))"
baseDir = os.path.dirname(os.path.abspath(__file__))

## config
config = configparser.ConfigParser()
config.read(os.path.join(baseDir, "../config.ini"))

## system:
tmpFileNameStatus = ".tSfvPyTmp_v0_2_File"
logLevel = config.get("log", "level")
log = logger.getLogger("fileHandler", logLevel)
uSF = config.get("style", "status")
uFF = config.get("style", "floating")
rSF = config.get("rule", "sfvFist")


def calc(sfvFile):
    cntGood = 0
    good = []
    cntMissing = 0
    missing = []
    cntBroken = 0
    broken = []
    cntAll = 0
    baseDir = os.path.dirname(sfvFile)

    with open(sfvFile, 'r') as sfv:
        for line in sfv.readlines():

            fileName, hashList = line.strip().split(" ")
            fp = os.path.join(baseDir, fileName)
            cntAll += 1

            # check if file exists:
            if not os.path.isfile(fp):
                cntMissing += 1
                missing.append(fileName)
                continue

            # check if file-hash is good
            hashCalc = hashing.crc32(fp).lower()

            if hashCalc == hashList:
                cntGood += 1
                good.append(fileName)
                continue

            # or bad
            if hashCalc != hashList:
                log.debug("bad file: " + fileName+" ('"+hashCalc+"' != '"+hashList+"')")
                cntBroken += 1
                broken.append(fileName)
                continue

            # impossible outcome?!
            else:
                log.error("impossible outcome?!")

    log.debug("Good: "+str(good))
    log.debug("Missing: "+str(missing))
    log.debug("Broken: "+str(broken))

    return [cntAll, len(missing), len(good), len(broken)]


def saveStatus(baseDir, sfvFile, status):
    if status == 0:
        log.debug("status error")
        return

    avail = (status[2] + status[3])
    comp = (avail / status[0]) * 100
    good = 0
    broken = 0
    if comp != 0:
        good = (status[2] / comp) * 100
        broken = (status[3] / comp) * 100

    user = uSF.format(status[0],
                      status[1],
                      status[2],
                      status[3],
                      avail,
                      format(comp, uFF),
                      format(good, uFF),
                      format(broken, uFF))

    statusDir = os.path.join(baseDir, user)
    if not os.path.exists(statusDir):
        os.mkdir(statusDir)

    with open(os.path.join(baseDir, tmpFileNameStatus), "w") as tmp:
        tmp.write(sfvFile + "\n")
        tmp.write(statusDir + "\n")
        for line in status:
            tmp.write(str(line))
            tmp.write("\n")


def removeStatus(baseDir, userStatus):
    statusDir = os.path.join(baseDir, userStatus)
    log.debug("removing: " + statusDir)
    if os.path.exists(statusDir):
        os.rmdir(statusDir)


def processSfv(baseDir, fileName):
    sfvFile = os.path.join(baseDir, fileName)
    log.debug("processing sfv: '" + sfvFile + "'")
    status = calc(sfvFile)
    log.debug("status: " + str(status))
    saveStatus(baseDir, fileName, status)


def processFile(baseDir, fileName):
    log.debug("processing file: '" + fileName + "'")
    # looking for tmp-file in folder
    if not os.path.exists(os.path.join(baseDir, tmpFileNameStatus)):
        log.error("no tmp file found in " + baseDir)
        return

    with open(os.path.join(baseDir, tmpFileNameStatus), "r") as tmp:
        tmpLines = tmp.readlines()

        sfvFile = str(tmpLines[0]).strip()
        userStatus = str(tmpLines[1]).strip()

        removeStatus(baseDir, userStatus)
        processSfv(baseDir, sfvFile)


def processFolder(dirName):
    log.debug("processing folder: '" + dirName + "'")

    # remove old files
    if os.path.isfile(os.path.join(dirName, tmpFileNameStatus)):
        with open(os.path.join(dirName, tmpFileNameStatus), "r") as tmp:
            tmpLines = tmp.readlines()
            userStatus = str(tmpLines[1]).strip()
            removeStatus(dirName, userStatus)
        os.remove(os.path.join(dirName, tmpFileNameStatus))

    # search new
    for file in os.listdir(os.path.abspath(dirName)):
        name, ext = os.path.splitext(file)
        if ext.lower() == ".sfv":
            processSfv(dirName, file)
        else:
            continue
