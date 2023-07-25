from ADBInterface import CommonADB
from Common import CommonFunction
import os
from ADBInterface import simplify_interface_code
from Common import CommonFunction, AssertResult, ADBCommand
from Common.Log import MyLog

sim_code = simplify_interface_code.simplify_code()

log = MyLog()

assertData = AssertResult.AssertOutput()
commData = CommonFunction.CommonData()


class QualcommChipInterface(CommonADB.CommonInterface):
    def __init__(self):
        pass

    def cur_user(self):
        cmd = "getprop ro.build.type"
        comment = "User or Debug版本："
        sim_code.simplify_txt_file(cmd, comment)
