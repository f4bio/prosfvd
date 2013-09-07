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
log = logger.getLogger("fileHandler", logLevel)


def sfv(baseDir, fileName):
    sfvFile = os.path.join(baseDir, fileName)
    log.debug("processing sfv: '" + sfvFile + "'")


def file(baseDir, fileName):
    log.debug("processing file: '" + fileName + "'")


def folder(dirName):
    log.debug("processing folder: '" + dirName + "'")
