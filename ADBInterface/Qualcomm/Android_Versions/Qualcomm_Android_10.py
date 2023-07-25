# from ADBInterface import
from Common import CommonFunction, AssertResult, ADBCommand, DealAlert
from Common.Log import MyLog, OutPutText
import re
from Conf.Config import Config
from ADBInterface import simplify_interface_code
from ADBInterface.Qualcomm import QualcommChip

meta_alert = DealAlert.AlertData()
log = MyLog()
my_text = OutPutText()
sim_code = simplify_interface_code.simplify_code()
assertData = AssertResult.AssertOutput()
commData = CommonFunction.CommonData()
adbData = ADBCommand.ADBManage()


class QualcommAndroid10(QualcommChip.QualcommChipInterface):
    def __init__(self):
        pass

    def reboot_dev(self):
        commData.adb_reboot_no_debug_auth()
        self.open_root_auth()

    def sys_brightness_setting(self):
        cmd = "dumpsys power | grep mScreenBrightnessSetting"
        sim_code.simplify_txt_file(cmd, "系统亮度系数：")

    def hand_type_check_default_brightness(self):
        cmd = "dumpsys power | grep mScreenBrightnessSettingDefault"
        def_res = commData.send_shell_cmd(cmd)
        def_value_list = re.findall(r'\d+\.?\d*', def_res)
        def_value = def_value_list[0]
        cur_value = self.cur_brightness()
        # if def_valule in self.cur_brightness():
        if int(def_value) <= 149 and int(cur_value) <= 149:
            log.info("默认亮度不超过90%")
            my_text.write_text(def_value)
            my_text.write_text(cur_value)
        else:
            err = "@@@默认亮度超过90%， 请手动检查"
            log.error(err)
            my_text.write_text(err)
            my_text.write_text(def_value)
        # else:
        #     err = "系统默认的亮度和当前的亮度不一致"
        #     log.error(err)
        #     assert False, err
        return int(def_value)

    def modify_brightness_time_out(self, time_out):
        if time_out.strip() == "永不":
            value = str(0)
            self.deal_brigthness_time_out(time_out, value)
        elif time_out.strip() == "15sec":
            value = str(15000)
            self.deal_brigthness_time_out(time_out, value)
        elif time_out.strip() == "1min":
            value = str(60000)
            self.deal_brigthness_time_out(time_out, value)
        elif time_out.strip() == "5min":
            value = str(300000)
            self.deal_brigthness_time_out(time_out, value)


if __name__ == '__main__':
    adb = ADBCommand.ADBManage()
    adb.clientConnect()
    data = QualcommAndroid10()
    data.hand_type_modify_brightness()
