from ADBInterface import CommonADB
from ADBInterface.MTK import MTKChip
from ADBInterface.Qualcomm import QualcommChip
from ADBInterface.Qualcomm.Android_Versions import Qualcomm_Android_8_1, Qualcomm_Android_10, Qualcomm_Android_11
from ADBInterface.RK import RKChip
from ADBInterface.RK.Android_Versions import RK_Android_11, RK_Android_7_1_2
from Common.Log import MyLog

log = MyLog()

RK = RKChip.RKInterface()
MTK = MTKChip.MTKChipInterface()
RK_ver_11 = RK_Android_11.RKAndroid11()
QualComm = QualcommChip.QualcommChipInterface()
Qual_ver_8_1 = Qualcomm_Android_8_1.QualcommAndroid8_1()
Qual_ver_11 = Qualcomm_Android_11.QualcommAndroid11()
RK_ver_7_1_2 = RK_Android_7_1_2.RKAndroid7_1_2()
comm = CommonADB.CommonInterface()


class InterfaceData:
    def __init__(self, ver):
        # self.chipPlan = chip
        self.androidVer = ver

    def finalReturn(self, interface):
        # print(interface.retFlag)
        if False in interface.retFlag:
            interface.retFlag = []
            err = "@@@@用例测试不通过"
            log.error(err)
            print(err)
            return False
        else:
            interface.retFlag = []
            meg = "用例测试通过~"
            log.info(meg)
            print(meg)
            return True

    def interfaceReturn(self):
        # if self.chipPlan == "Rockchip" and self.androidVer == "11":
        #     return RK_ver_11
        # elif self.chipPlan == "MTKChip":
        #     return MTK
        if self.androidVer == "8.1.0":
            return Qual_ver_8_1
        elif self.androidVer == "11":
            return Qual_ver_11
        elif self.androidVer == "7.1.2":
            return RK_ver_7_1_2


