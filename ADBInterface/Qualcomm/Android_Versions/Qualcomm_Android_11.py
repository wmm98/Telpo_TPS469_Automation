# from ADBInterface import
from Common import CommonFunction, AssertResult, ADBCommand, DealAlert
from Common.Log import MyLog, OutPutText
import re
from Conf.Config import Config
from ADBInterface import simplify_interface_code
from ADBInterface.Qualcomm import QualcommChip
import time
import datetime

meta_alert = DealAlert.AlertData()
log = MyLog()
my_text = OutPutText()
sim_code = simplify_interface_code.simplify_code()
assertData = AssertResult.AssertOutput()
commData = CommonFunction.CommonData()
adbData = ADBCommand.ADBManage()


class QualcommAndroid11(QualcommChip.QualcommChipInterface):
    def __init__(self):
        pass

    def reboot_dev(self):
        commData.adb_restart_devices()
        self.open_root_auth()
        commData.adb_reboot()

    def reboot_dev_only(self):
        commData.adb_restart_devices()

    def open_root_auth(self):
        act = commData.adb_root()
        ret = assertData.assert_is_true(act)
        act = commData.adb_remout()
        ret = assertData.assert_is_true(act)
        # commData.adb_reboot()
        # 调试先不开
        # self.reboot_dev_only()

    def get_volume_offset(self):
        my_text.write_text("alarm_speaker: [1, 7]")
        my_text.write_text("music_speaker: [0, 15]")
        my_text.write_text("ring_speaker: [0, 15]")
        my_text.write_text("volume_voice_earpiece: [1, 5]")

    def get_volume_info(self, stream):
        cmd = "settings get system %s" % str(stream)
        res = commData.send_shell_cmd(cmd)
        meg = "当前的音量信息为： %s" % res
        sim_code.print_log(meg)
        my_text.write_text(meg)

    # def get_cur_volume_value(self, stream):
    #     cmd = "settings get system %s" % str(stream)
    #     return sim_code.str_replace(commData.send_shell_cmd(cmd))
    #
    # def set_volume_value(self, stream, value):
    #     cmd = "settings put system %s %s" % (stream, str(value))
    #     sim_code.simplify_no_return(cmd)
    #
    # def check_volume_value(self, stream, value):
    #     act = sim_code.str_replace(self.get_cur_volume_value(stream))
    #     if str(value) != act:
    #         sim_code.print_err_log("音量设置失败！！！")
    #         assert False, "音量设置失败！！！"
    #     sim_code.print_log("音量设置成功！！！")

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
            value = str(2147483647)
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

    def hand_type_modify_brightness(self, value=102):
        # 0:10%, 102:82%, 255:100%
        cmd = "settings put system screen_brightness %s" % str(value)

        text1 = ''

        if value == 0:
            text1 = "亮度已经修改为0了,  检查设置是否为0%, 请观察亮度变化有没有黑屏 "
        elif value == 102:
            text1 = "亮度已经修改为默认亮度了, 请观察亮度变化"
        elif value == 255:
            text1 = "亮度已经修改为100%了,  检查设置是否为100%, 请观察亮度变化"
        meta_alert.getAlert(text=text1)
        # act = self.cur_brightness()
        sim_code.simplify_no_return(cmd)
        # print(type(self.cur_brightness()))
        assertData.assert_text_exit(str(value), self.cur_brightness())

    def test_for_screen_timeout(self):
        self.set_screen_sleep("2147483647")
        self.reboot_dev()
        self.screen_sleep()
        # self.screen_wake()
        self.unlock_screen()
        self.unlock_screen()
        my_text.write_text("##########设置1min后进入休眠################")
        my_text.write_text("开始计算======")
        cmd = "dumpsys power | grep \"Display Power: state=\""
        self.set_screen_sleep("60000")
        my_text.write_text("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        my_text.write_text(str(0) + "秒后 " + commData.send_shell_cmd(cmd))
        time.sleep(52)
        my_text.write_text(str(52) + "秒后 " + commData.send_shell_cmd(cmd))
        time.sleep(2)
        my_text.write_text(str(54) + "秒后 " + commData.send_shell_cmd(cmd))
        time.sleep(1)
        my_text.write_text(str(55) + "秒后 " + commData.send_shell_cmd(cmd))
        time.sleep(1)
        my_text.write_text(str(56) + "秒后 " + commData.send_shell_cmd(cmd))
        time.sleep(1)
        my_text.write_text(str(57) + "秒后 " + commData.send_shell_cmd(cmd))
        time.sleep(1)
        my_text.write_text(str(58) + "秒后 " + commData.send_shell_cmd(cmd))
        time.sleep(1)
        my_text.write_text(str(59) + "秒后 " + commData.send_shell_cmd(cmd))
        my_text.write_text("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        assert "OFF" in self.get_screen_status(), "@@@1min中后进入休眠失败，请检查！！！"

        self.screen_wake()
        self.unlock_screen()
        my_text.write_text("##########设置15sec后进入休眠################")
        my_text.write_text("开始计算======")
        self.set_screen_sleep("15000")
        my_text.write_text("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        for i in range(1, 15):
            time.sleep(1)
            my_text.write_text(str(i) + "秒后 " + commData.send_shell_cmd(cmd))

        my_text.write_text("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        assert "OFF" in self.get_screen_status()

        my_text.write_text("##########设置永不休眠休眠################")
        self.screen_wake()
        self.unlock_screen()
        self.set_screen_sleep("2147483647")
