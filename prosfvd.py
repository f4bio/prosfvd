#!/usr/bin/python3

## system imports
import os
import time
import sys
import queue
import threading
import configparser
## own imports
from mod.fileHandler import processSfv, processFile, processFolder
from mod import logger

## constants:
__author__ = "ft (ft@secure.la))"
baseDir = os.path.dirname(os.path.abspath(__file__))

## config
config = configparser.RawConfigParser()
config.read(os.path.join(baseDir, "config.ini"))

## vars:
now = time.localtime()
fifoPipe = os.path.abspath(config.get("io", "fifoPipe"))
ftpBase = os.path.abspath(config.get("io", "ftpBase"))
logLevel = config.get("log", "level")
trigger = [x.strip().upper() for x in str(config.get("io", "trigger")).split(",")]
log = logger.getLogger("tsfvpy", logLevel)
que = queue.Queue()
running = True


def worker():
    working = True
    while working:
        entry = que.get()
        baseDir = os.path.dirname(entry)
        name, ext = os.path.splitext(entry)
        if ext.lower() == ".sfv":
            processSfv(baseDir, entry)
        elif os.path.isdir(entry):
            processFolder(entry)
        else:
            processFile(baseDir, entry)
        que.task_done()


## daemon, wait for new files
def daemon(pipe):
    t = threading.Thread(target=worker)
    t.setDaemon(True)
    try:
        log.debug("starting daemon...")
        t.start()
        while running:
            with open(pipe, "r") as p:
                newFifo = p.readline()
                # log.debug("new fifo entry: " + newFifo)
                fifoSplit = newFifo.split("|")

                if fifoSplit[0] in trigger:
                    log.debug("triggered: '" + str(fifoSplit) + "'")
                    path = os.path.abspath(ftpBase+""+fifoSplit[2].strip())
                    # log.debug("-----------------------")
                    # log.debug(os.path.abspath(fifoSplit[2].strip()))
                    # log.debug(os.path.abspath(ftpBase))
                    # log.debug(os.path.abspath(ftpBase+""+fifoSplit[2].strip()))
                    # log.debug("-----------------------")
                    args = fifoSplit[1].strip()

                    if fifoSplit[0].lower() == "site tsfv":
                        args = args.split(" ")
                        if args[0].lower() == "tsfv":
                            log.debug("adding to queue for recheck...")
                            que.put(path)
                    else:
                        log.debug("adding to queue...")
                        que.put(os.path.join(path, args))

    except:
        log.debug("Unexpected error in daemon loop: " + str(sys.exc_info()[0]))
        raise

## main
def main(argv=None):
    log.debug("starting...")
    daemon(fifoPipe)

if __name__ == '__main__':
    sys.exit(main())