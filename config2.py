import os

messageFilePath = os.sep.join(["/home", "deployer", "ReceiveFile", "message"])
replySavePath = os.sep.join(["/home", "deployer", "ReplyFile"])
g5_savePath = os.sep.join(["/home", "deployer", "g5_save"])
sourceSavePath = os.sep.join(["/home", "deployer", "ReceiveFile", "Answer"])


def mkdir(path):
    path = path.strip()
    path = path.rstrip(os.sep)
    isExist = os.path.exists(path)
    if not isExist:
        try:
            os.makedirs(path)
        except Exception as e:
            print(e)
            return False
        return True
    else:
        return True
