import logging
import os


def getLogger(name, level):
    ## logging
    # http://docs.python.org/3/howto/logging.html#configuring-logging
    baseDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    fileName = name + ".log"
    filePath = os.path.join(baseDir, "logs")

    logger = logging.getLogger("Log - " + name)
    logger.setLevel(level)

    if not os.path.exists(filePath):
        os.mkdir(filePath)

    ch = logging.StreamHandler()
    fh = logging.FileHandler(os.path.join(filePath, fileName))

    ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger