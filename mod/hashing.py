import zlib
__author__ = 'ft2011 (teeee))'

def crc32(fileName):
    prev = 0
    for line in open(fileName, "rb"):
        prev = zlib.crc32(line, prev)
    return str("{0:08x}").format((prev & 0xFFFFFFFF))