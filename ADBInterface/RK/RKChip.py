from ADBInterface import CommonADB
from Common import CommonFunction, AssertResult, ADBCommand
import time
from ADBInterface import simplify_interface_code
from Common.Log import MyLog
import os
from Common import DealAlert, Log
from Conf.Config import Config


my_text = Log.OutPutText()
conf = Config()
log = Log.MyLog()
meta_alert = DealAlert.AlertData()
simple_code = simplify_interface_code.simplify_code()

ADBSend = ADBCommand.ADBManage()
assertData = AssertResult.AssertOutput()
comInterface = CommonADB.CommonInterface
commData = CommonFunction.CommonData()


class RKInterface(CommonADB.CommonInterface):

    def __init__(self):
        # self.retFlag = []
        pass

    def get_screen_status(self):
        cmd = "dumpsys window policy |grep mAwake="
        res = commData.send_shell_cmd(cmd)
        simple_code.print_log(res)
        return res

    def screen_wake(self):
        if "false" in self.get_screen_status():
            self.sleep_and_wake_screen()
            assertData.assert_text_exit("true", self.get_screen_status())

    def screen_sleep(self):
        if "true" in self.get_screen_status():
            self.sleep_and_wake_screen()
            assertData.assert_text_exit("false", self.get_screen_status())

    def reboot_dev(self):
        commData.adb_restart_devices()
        self.open_root_auth()

    def open_root_auth(self):
        act = commData.adb_root()
        ret = assertData.assert_is_true(act)
        act = commData.adb_remout()
        ret = assertData.assert_is_true(act)

    def cur_user(self):
        cmd = "getprop | grep product.build.type"
        comment = "User or Debug版本："
        simple_code.simplify_txt_file(cmd, comment)

    def selinux_auth(self):
        cmd = "getenforce"
        comment = "selinux状态："
        simple_code.simplify_txt_file(cmd, comment)

    def internal_model(self):
        cmd = "getprop | grep ro.internal.model"
        comment = "内部型号是:"
        simple_code.simplify_txt_file(cmd, comment)

    def product_model(self):
        cmd = "getprop | grep ro.product.model"
        comment = "外部型号是:"
        simple_code.simplify_txt_file(cmd, comment)

    def get_volume_offset(self):
        my_text.write_text("alarm_speaker: [1, 7]")
        my_text.write_text("music_speaker: [0, 15]")
        my_text.write_text("ring_speaker: [0, 15]")
        my_text.write_text("volume_voice_earpiece: [1, 5]")

    def get_volume_info(self, stream):
        cmd = "settings get system %s" % str(stream)
        res = commData.send_shell_cmd(cmd)
        meg = "当前的音量信息为： %s" % res
        simple_code.print_log(meg)
        my_text.write_text(meg)

    def single_process_exit(self, package):
        cmd = "ps | grep %s" % package
        try:
            simple_code.simplify_text_exit(cmd, package)
        except AssertionError:
            time.sleep(1)
            simple_code.simplify_text_exit(cmd, package)

    def single_process_not_exit(self, package):
        cmd = "ps | grep %s" % package
        simple_code.simplify_no_return(cmd)

    def add_language(self, language):
        # 国内外核添加英文 en-US zh-Hans-CN
        cmd = "am broadcast -a android.intent.action.language --es language_choose_list %s" % language
        exp = "android.intent.action.language"
        act = commData.send_sub_pro_cmd(cmd)
        assertData.assert_text_exit(exp, act)

    def set_sys_langauge(self, lang):
        cmd = "am broadcast -a android.intent.action.language --es language %s" % lang
        exp = "android.intent.action.language"
        act = commData.send_sub_pro_cmd(cmd)
        assertData.assert_text_exit(exp, act)


if __name__ == '__main__':
    ADBSend.clientConnect()
    data = RKInterface()
    data.open_root_auth()
    # print(data.retFlag)
