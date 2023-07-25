from ADBInterface.RK import RKChip
from Common import CommonFunction, AssertResult, DealAlert
from Common.Log import MyLog, OutPutText
import os
import datetime
import time
from ADBInterface import simplify_interface_code

commData = CommonFunction.CommonData()
assertData = AssertResult.AssertOutput()
sim_code = simplify_interface_code.simplify_code()
log = MyLog()
my_text = OutPutText()
meta_alert = DealAlert.AlertData()


class RKAndroid7_1_2(RKChip.RKInterface):
    def __init__(self):
        pass

    def reboot_dev(self):
        commData.adb_restart_devices()
        self.open_root_auth()

    # # 安卓11版本的状态栏命令不一样,需要问研发
    # def show_status_bar(self):
    #     cmd = "am broadcast -a android.intent.action.show.statusbar"
    #     exp = "Broadcasting: Intent { act=android.intent.action.show.statusbar flg=0x400000 }" \
    #           "Broadcast completed: result=0"
    #     sim_code.simplify_text_exit(cmd, exp)
    #
    # def hide_status_bar(self):
    #     cmd = "am broadcast -a android.intent.action.hide.statusbar"
    #     exp = "Broadcasting: Intent { act=android.intent.action.hide.statusbar flg=0x400000 }" \
    #           "Broadcast completed: result=0"
    #     sim_code.simplify_text_exit(cmd, exp)
    def cur_user(self):
        cmd = "getprop ro.build.type"
        comment = "User or Debug版本："
        sim_code.simplify_txt_file(cmd, comment)

    def navigationbar_status_on(self):
        # navigation_bar_show
        cmd = "settings get system navigation_bar_show"
        exp = 1
        sim_code.simplify_text_exit(cmd, str(exp))

    def navigationbar_status_off(self):
        cmd = "settings get system navigation_bar_show"
        exp = 0
        sim_code.simplify_text_exit(cmd, str(exp))

    # def langauga_input_method(self):
    #     cmd = "getprop |grep ro.product.locale.language"
    #     act = sim_code.str_replace(commData.send_shell_cmd(cmd))
    #     log.info(cmd)
    #     if "zh" in act:
    #         res = "zh-CN"
    #     else:
    #         res = "未定义"
    #     return res

    def hand_type_modify_brightness(self, value=102):
        # 0:10%, 102:82%, 255:100%
        cmd = "settings put system screen_brightness %s" % str(value)

        text1 = ''

        if value == 0:
            text1 = "亮度已经修改为0了,  检查设置是否为0%, 请观察亮度变化有没有黑屏 "
        elif value == 255:
            text1 = "亮度已经修改为100%了,  检查设置是否为100%, 请观察亮度变化"
        else:
            text1 = "亮度已经修改为默认亮度了, 请观察亮度变化"

        meta_alert.getAlert(text=text1)
        # act = self.cur_brightness()
        sim_code.simplify_no_return(cmd)
        # print(type(self.cur_brightness()))
        assertData.assert_text_exit(str(value), self.cur_brightness())

    # 使用于RK芯片
    def open_bluetooth_btn(self):
        if "1" not in self.get_cur_bluetooth_status():
            commData.send_shell_cmd("service call bluetooth_manager 6")
            time.sleep(1)

    def close_bluetooth_btn(self):
        if "0" not in self.get_cur_bluetooth_status():
            commData.send_shell_cmd("service call bluetooth_manager 8")

    def reboot_recovery(self):
        cmd = "am broadcast -a android.intent.action.MASTER_CLEAR"
        commData.send_shell_cmd(cmd)
        time.sleep(270)
        # meta_alert.get_yes_or_no("请确认设备已经恢复出厂设置了吗, 请set up SD卡并且打开USB debug后请点击确认")
        commData.adb_dev_exit()
        commData.adb_dev_completed()
