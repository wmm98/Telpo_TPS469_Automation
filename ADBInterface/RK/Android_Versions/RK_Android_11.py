from ADBInterface.RK import RKChip
from Common import CommonFunction, AssertResult
from Common.Log import MyLog
import os
from ADBInterface import simplify_interface_code

sim_code = simplify_interface_code.simplify_code()
assertData = AssertResult.AssertOutput()
commData = CommonFunction.CommonData()


class RKAndroid11(RKChip.RKInterface):
    def __init__(self):
        pass

    # 安卓11版本的状态栏命令不一样,需要问研发
    def show_status_bar(self):
        cmd = "am broadcast -a android.intent.action.show.statusbar"
        exp = "Broadcasting: Intent { act=android.intent.action.show.statusbar flg=0x400000 }" \
              "Broadcast completed: result=0"
        sim_code.simplify_text_exit(cmd, exp)

    def hide_status_bar(self):
        cmd = "am broadcast -a android.intent.action.hide.statusbar"
        exp = "Broadcasting: Intent { act=android.intent.action.hide.statusbar flg=0x400000 }" \
              "Broadcast completed: result=0"
        sim_code.simplify_text_exit(cmd, exp)

    def navigationbar_status_on(self):
        cmd = "settings get system navigationbar_show"
        exp = 1
        sim_code.simplify_text_exit(cmd, str(exp))

    def navigationbar_status_off(self):
        cmd = "settings get system navigationbar_show"
        exp = 0
        sim_code.simplify_text_exit(cmd, str(exp))
