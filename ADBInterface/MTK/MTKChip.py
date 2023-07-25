from ADBInterface import CommonADB
from Common import CommonFunction, AssertResult, ADBCommand
import time
from ADBInterface import simplify_interface_code
from Common.Log import MyLog
from Conf.Config import Config
import os

simple_code = simplify_interface_code.simplify_code()
ADBSend = ADBCommand.ADBManage()
assertData = AssertResult.AssertOutput()
comInterface = CommonADB.CommonInterface

commData = CommonFunction.CommonData()
conf = Config()


class MTKChipInterface(comInterface):
    def __init__(self):
        pass
