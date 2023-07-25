from ADBInterface.RK import RKChip
from Common import CommonFunction, AssertResult, ADBCommand
from Common.Log import MyLog
import os
import time
from ADBInterface import simplify_interface_code
from ADBInterface.Qualcomm import QualcommChip

sim_code = simplify_interface_code.simplify_code()
assertData = AssertResult.AssertOutput()
commData = CommonFunction.CommonData()
adbData = ADBCommand.ADBManage()


class QualcommAndroid8_1(QualcommChip.QualcommChipInterface):
    def __init__(self):
        pass

    def open_root_auth(self):
        act = commData.adb_root()
        assertData.assert_is_true(act)
        # 需要等待1秒再执行adb disable-verity
        # time.sleep(2)
        dis_act1 = commData.send_sub_pro_cmd("adb disable-verity")
        dis_exp = "Verity disabled on"
        try:
            assertData.assert_text_exit(dis_exp, dis_act1)
        except AssertionError as e:
            exp_deal = "Verityalreadydisabledon".replace("\n", "").replace(" ", "")
            act_deal = dis_act1.replace("\n", "").replace(" ", "")
            if exp_deal not in act_deal:
                assert False, e
            else:
                pass

        commData.adb_reboot()
        ro_act = commData.adb_root()
        assertData.assert_is_true(ro_act)

        re_act = commData.adb_remout()
        assertData.assert_is_true(re_act)
