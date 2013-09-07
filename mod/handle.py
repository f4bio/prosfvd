import os
import configparser
from mod import hashing
from mod import logger

## vars
__author__ = "ft2011@gmail.com"
baseDir = os.path.dirname(os.path.abspath(__file__))

## config
config = configparser.ConfigParser()
config.read(os.path.join(baseDir, "../config.ini"))

## system:
logLevel = config.get("log", "level")
log = logger.getLogger("handle", logLevel)


def sfv(sfvPath):
    log.debug("processing sfv: '" + sfvPath + "'")
    with open(sfvPath, "r") as sp:
        for line in sp.readlines():
            fileName, crcValue = line.split(" ")

            missing = os.path.join(os.path.dirname(sfvPath), fileName + "-MiSSiNG")
            with open(missing, "w") as m:
                m.write(crcValue)

def file(filePath):
    log.debug("processing file: '" + filePath + "'")


def folder(folderPath):
    log.debug("processing folder: '" + folderPath + "'")
