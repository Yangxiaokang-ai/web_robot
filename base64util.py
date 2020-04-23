import base64
import os

from config2 import mkdir

sendFilePath = os.sep.join(["/home", "deployer", "sendFile"])


def bytes2file(filename, content):
    mkdir(sendFilePath)
    fileContent = base64.b64decode(content)
    file = open(sendFilePath + os.sep + filename, 'wb')
    file.write(fileContent)
    file.close()
    return sendFilePath + os.sep + filename
