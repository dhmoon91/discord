import os

dirname = os.path.dirname(__file__)


def getFilePath(filePath):
    return os.path.join(dirname, filePath)
