from Common import CommonFunction, AssertResult, ADBCommand, DealAlert
from Common.Log import MyLog, OutPutText
import os
import datetime
import time
from ADBInterface import simplify_interface_code
from Conf.Config import Config
import re

meta_alert = DealAlert.AlertData()
conf = Config()
my_text = OutPutText()
sim_code = simplify_interface_code.simplify_code()
adb_data = ADBCommand.ADBManage()
log = MyLog()

assertData = AssertResult.AssertOutput()
commData = CommonFunction.CommonData()


class CommonInterface:
    def __init__(self):
        # self.retFlag = []
        pass

    def reboot_dev(self):
        commData.adb_reboot()

    def open_root_auth(self):
        act = commData.adb_root()
        ret = assertData.assert_is_true(act)
        act = commData.adb_remout()
        ret = assertData.assert_is_true(act)

    def cur_user(self):
        cmd = "getprop | grep product.build.type"
        comment = "User or Debug版本："
        sim_code.simplify_txt_file(cmd, comment)

    def selinux_auth(self):
        cmd = "getenforce"
        comment = "selinux状态："
        sim_code.simplify_txt_file(cmd, comment)

    def internal_model(self):
        cmd = "getprop | grep ro.internal.model"
        comment = "内部型号是:"
        sim_code.simplify_txt_file(cmd, comment)

    def product_model(self):
        cmd = "getprop | grep ro.product.model"
        comment = "外部型号是:"
        sim_code.simplify_txt_file(cmd, comment)

    def cur_cpu_freq(self, no):
        cmd = "cat /sys/devices/system/cpu/cpu%d/cpufreq/cpuinfo_cur_freq" % no
        comment = "*****系统cpu%d当前的主频为：" % no
        sim_code.simplify_txt_file(cmd, comment)

    def max_cpu_freq(self, no):
        cmd = "cat /sys/devices/system/cpu/cpu%d/cpufreq/cpuinfo_max_freq" % no
        comment = "*****系统cpu%d最大的主频为：" % no
        sim_code.simplify_txt_file(cmd, comment)

    def min_cpu_freq(self, no):
        cmd = "cat /sys/devices/system/cpu/cpu%d/cpufreq/cpuinfo_min_freq" % no
        comment = "*****系统cpu%d最小的主频为：" % no
        sim_code.simplify_txt_file(cmd, comment)

    def kernals_sum(self):
        cmd = "cat /proc/cpuinfo |grep processor"
        ker_info = commData.send_shell_cmd(cmd)
        kernal_count = ker_info.count("processor")
        return kernal_count

    def check_DDR(self):
        cmd = "df -h"
        comment = "*****存储空间分配情况："
        sim_code.simplify_txt_file(cmd, comment)

    def del_internal_app(self, package):
        cmd = "pm uninstall %s" % package
        exp = "Failure [DELETE_FAILED_INTERNAL_ERROR]"
        sim_code.simplify_text_exit(cmd, exp)

    def comm_install_discard_now(self, apk):
        self.comm_push_file("APK", apk)
        cmd = "pm install -r /sdcard/%s" % apk
        exp = "Success"
        sim_code.simplify_text_exit(cmd, exp)

    def comm_install(self, apk):
        # path = conf.project_path + '\\APK\\' + apk
        # print(path)
        act = commData.adb_install(apk)
        # assertData.assert_is_true(act)

    def comm_push_file(self, dire, file_name, des="sdcard"):
        act = commData.adb_push(dire, file_name, des)
        # exp = "100 %"
        # assertData.assert_text_exit(exp, act)

    def comm_pull_file(self, file_name, src="sdcard"):
        act = commData.adb_pull(file_name, org=src)

    def comm_rm_file(self, file_name):
        cmd = "rm sdcard/%s" % file_name
        sim_code.simplify_no_return(cmd)

    def comm_ls_exit(self, file_name, des="sdcard"):
        cmd = "ls %s | grep %s" % (des, file_name)
        exp = file_name
        sim_code.simplify_text_exit(cmd, exp)

    def comm_ls_not_exit(self, file_name, des="sdcard"):
        cmd = "ls %s | grep %s" % (des, file_name)
        sim_code.simplify_no_return(cmd)

    def comm_uninstall(self, package):
        act = commData.adb_uninstall(package)
        # print("卸载调试。。。。")
        # print(act)
        res = assertData.assert_is_true(act)

    def pre_pro_test_uninstall(self, package):
        try:
            act = commData.adb_uninstall(package)
            # if act == True:
            #     # log.info("安装前已卸载app")
            #     pass
            # if act == False:
            #     pass
        except Exception as e:
            assert False, e

    def pre_pro_app_is_exit(self, package):
        cmd = "pm list packages -3|grep %s" % package
        res = commData.send_shell_cmd(cmd)
        log.info(res)
        if package in res:
            return True
        else:
            return False

    def internal_installed_apps(self):
        cmd = "pm list packages -s"
        comment = "已经安装的内部应用服务"
        sim_code.simplify_txt_file(cmd, comment)

    def third_installed_apps(self):
        cmd = "pm list packages -3"
        comment = "已经安装的第三方应用服务"
        sim_code.simplify_txt_file(cmd, comment)

    # 查看第三方应用是否存在啊
    def app_is_exit(self, package):
        cmd = "pm list packages -3|grep %s" % package
        sim_code.simplify_text_exit(cmd, package)

    def app_not_exit(self, package):
        cmd = "pm list packages -3|grep %s" % package
        sim_code.simplify_no_return(cmd)

    def get_package_version(self, package):
        act = commData.get_package_ver(package)
        # 先返回，后续相应的用例再进一步
        return act

    def assert_compare(self, low, high):
        res = assertData.compare_(low, high)

    def comm_app_is_installed(self, package):
        act = commData.adb_app_is_installed(package)
        # print("=========查看是否安装")
        # print(act)
        res = assertData.assert_is_true(act)

    def start_activity(self, activity_name):
        try:
            cmd = "am start %s" % activity_name
            exp = "Starting: Intent { cmp=%s }" % activity_name
            # 适配高通的机器，暂时先不用simply_code的方法
            act = commData.send_shell_cmd(cmd, 1)
            # 不做启动检查，只进行进程检查
            # res = assertData.assert_text_exit(exp, act)
        except AssertionError as e:
            time.sleep(3)
            self.force_stop_process("com.android.music")
            assert False, e

    def single_process_exit(self, package):
        cmd = "ps -A | grep %s" % package
        try:
            sim_code.simplify_text_exit(cmd, package)
        except AssertionError:
            time.sleep(1)
            sim_code.simplify_text_exit(cmd, package)

    def single_process_not_exit(self, package):
        cmd = "ps -A | grep %s" % package
        sim_code.simplify_no_return(cmd)

    def force_stop_process(self, package):
        cmd = "am force-stop %s" % package
        # 避免有时候没杀掉，执行多一遍
        # commData.send_shell_cmd(cmd)
        # time.sleep(1)
        try:
            sim_code.simplify_no_return(cmd)
        except AssertionError:
            self.clear_package(package)

    def clear_package(self, package):
        cmd = "pm clear %s" % package
        exp = "Success"
        sim_code.simplify_text_exit(cmd, exp)

    def pre_clear_package(self, package):
        cmd = "pm clear %s" % package
        commData.send_shell_cmd(cmd)

    def pre_pro_force_stop_process(self, package):
        try:
            cmd = "am force-stop %s" % package
            commData.send_shell_cmd(cmd)
        except Exception:
            pass

    def langauga_input_method(self):
        cmd = "getprop ro.product.locale"
        act = sim_code.str_replace(commData.send_shell_cmd(cmd))
        log.info(cmd)
        return act

    def check_cur_language(self, language):
        cmd = "getprop persist.sys.locale"
        act = sim_code.str_replace(commData.send_shell_cmd(cmd))
        log.info(cmd)
        assertData.assert_text_exit(language, act)
        return act

    def check_default_language(self):
        if "zh-CN" in self.langauga_input_method():
            # default_language = "Chinese"
            default_language = "zh-CN"
            return default_language
        elif "en-US" in self.langauga_input_method():
            # default_language = "English"
            default_language = "en-US"
            return default_language

    def CN_defualt_language_input(self):
        cmd = "settings get secure default_input_method"
        act = commData.send_shell_cmd(cmd)
        exp = conf.CN_input_method
        my_text.write_text("默认的输入法是： %s" % act)
        log.info(act)
        flag = 0
        for lan_inp in exp:
            if sim_code.str_replace(lan_inp) in sim_code.str_replace(act):
                flag += 1
                lan_spl = lan_inp.split("/")
                language = lan_spl[0]
                lan_ver = self.get_package_version(language)
                msg = "输入法为：%s, 版本为%s" % (language, lan_ver)
                log.info(msg)
                my_text.write_text(msg)
                break

        if flag == 0:
            err = "@@@@国内版本没有自带中文输入法"
            log.error(err)
            assert False, err

    def modify_default_langauge(self):
        # 待隐藏接口
        pass

    def manual_listen_music(self, cmd):
        # meta_path = conf.project_path + '/' + "Media\\Music\\testMusic.mp3"
        # res = os.path.exists(meta_path)
        # if not res:
        #     assert False, "文件路径不存在，"
        # 传输文件
        # self.comm_push_file("Media\\Music", music_name)
        text = "\n " * 10 + '请听和看！！！ \n 请注意声音由小变大再变小， 请听和看！' + " " * 100 + "\n " * 10
        meta_alert.getAlert(text)
        self.start_activity(cmd)

    # 用来调整媒体音量， 其他的有其他函数调整
    def adjust_volumn(self):
        # input keyevent 164 默认设置Media音量为静音
        commData.send_shell_cmd("input keyevent 164")
        # time.sleep(1)
        for i in range(10):
            commData.send_shell_cmd("input keyevent 24")
            # time.sleep(1)
        for i in range(8):
            commData.send_shell_cmd("input keyevent 25")
            # time.sleep(1)

        # 用来调整媒体音量， 其他的有其他函数调整

    def media_adjust_volumn(self):
        # commData.send_shell_cmd("input keyevent 164")
        self.set_volume_value(3, 0)
        time.sleep(1)
        self.set_volume_value(3, 5)
        time.sleep(1)
        self.set_volume_value(3, 7)
        time.sleep(1)
        self.set_volume_value(3, 9)
        time.sleep(1)
        self.set_volume_value(3, 11)
        time.sleep(1)
        self.set_volume_value(3, 13)
        time.sleep(1)
        self.set_volume_value(3, 15)
        time.sleep(1)
        self.set_volume_value(3, 13)
        time.sleep(1)
        self.set_volume_value(3, 11)
        time.sleep(1)
        self.set_volume_value(3, 9)
        time.sleep(1)
        self.set_volume_value(3, 5)
        time.sleep(1)
        self.set_volume_value(3, 2)
        time.sleep(1)

    def foreign_default_language_input(self):
        cmd = "adb shell settings get secure default_input_method"
        exp = ["com.android.inputmethod.latin/.LatinIME"]

    def operate_screen_shot(self, comment):
        cmd = "screencap -p /sdcard/%s.png" % comment
        sim_code.simplify_no_return(cmd)
        filename = "%s.png" % comment
        orignal = conf.project_path + "/%s" % "ScreenShot/%s" % filename
        # 修改原来图片名称
        re_org = conf.project_path + "/%s" % "ScreenShot/%s%s.png" % (comment, time.strftime("%Y-%m-%d_%H_%M_%S"))

        if os.path.exists(orignal):
            # os.rename(filename, path + '/err' + time.strftime("%Y-%m-%d_%H_%M_%S") + '.log')
            os.rename(orignal, re_org)
        # 截图
        commData.send_shell_cmd(cmd)
        self.comm_pull_file(filename, src="sdcard")
        # 检查存在截图
        if not os.path.exists(orignal):
            file_err = "@@@pull失败，不存在截图，请手动检查！！！"
            log.info(file_err)
            assert False, file_err
        try:
            self.comm_ls_exit(filename, des="sdcard")
        except AssertionError:
            e = "@@@不存在%s, 请检查！！！" % filename
            log.error(e)
            assert False, e
        self.comm_rm_file(filename)
        self.comm_ls_not_exit(filename, "sdcard")

    # 下拉状态栏
    def drop_down_status_bar_open(self):
        cmd = "am broadcast -a com.android.systemui.statusbar.phone.statusopen"
        exp = "com.android.systemui.statusbar.phone.statusopen"
        sim_code.simplify_text_exit(cmd, exp)

    def drop_down_status_bar_close(self):
        cmd = "am broadcast -a com.android.systemui.statusbar.phone.statusclose"
        exp = "com.android.systemui.statusbar.phone.statusclose"
        sim_code.simplify_text_exit(cmd, exp)

    def drop_down_status_bar_on(self):
        cmd = "settings get system dropdown_statusbar"
        exp = 1
        sim_code.simplify_text_exit(cmd, str(exp))

    def drop_down_status_bar_off(self):
        cmd = "settings get system dropdown_statusbar"
        exp = 0
        sim_code.simplify_text_exit(cmd, str(exp))

    def service_show_drop_down_status_bar(self):
        cmd = "service call statusbar 1"
        exp = "Result: Parcel(00000000    '....')"
        sim_code.simplify_text_exit(cmd, exp)

    def service_recover_drop_down_status_bar(self):
        cmd = "service call statusbar 2"
        exp = "Result: Parcel(00000000    '....')"
        sim_code.simplify_text_exit(cmd, exp)

    # 状态栏
    def show_status_bar(self):
        cmd = "am broadcast -a android.intent.action.show.statusbar"
        exp = "android.intent.action.show.statusbar"
        sim_code.simplify_text_exit(cmd, exp)

    def hide_status_bar(self):
        cmd = "am broadcast -a android.intent.action.hide.statusbar"
        exp = "android.intent.action.hide.statusbar"
        sim_code.simplify_text_exit(cmd, exp)

    def status_bar_on(self):
        cmd = "settings get system statusbar_show"
        exp = 1
        sim_code.simplify_text_exit(cmd, str(exp))

    def status_bar_off(self):
        cmd = "settings get system statusbar_show"
        exp = 0
        sim_code.simplify_text_exit(cmd, str(exp))

    # 导航栏
    def show_navigation_bar(self):
        cmd = "am broadcast -a com.android.internal.policy.impl.showNavigationBar"
        exp = "com.android.internal.policy.impl.showNavigationBar"
        sim_code.simplify_text_exit(cmd, exp)

    def hide_navigation_bar(self):
        cmd = "am broadcast -a com.android.internal.policy.impl.hideNavigationBar"
        exp = "com.android.internal.policy.impl.hideNavigationBar"
        sim_code.simplify_text_exit(cmd, exp)

    def navigationbar_status_on(self):
        cmd = "settings get system navigationbar_show"
        exp = 1
        sim_code.simplify_text_exit(cmd, str(exp))

    def navigationbar_status_off(self):
        cmd = "settings get system navigationbar_show"
        exp = 0
        sim_code.simplify_text_exit(cmd, str(exp))

    def get_default_brightness(self):
        # print("默认亮度为：", meta_alert.get_default_default_brightness())
        return meta_alert.get_default_default_brightness()

    def cur_brightness(self):
        #: settings put system screen_brightness 5000  //设置最高屏幕亮度
        # 亮度值为149时， 百分比为90%， 亮度值为41时， 百分比为60%
        cmd = "settings get system screen_brightness"
        # sim_code.simplify_txt_file(cmd, "屏幕当前亮度：")
        return commData.send_shell_cmd(cmd)

    # def brightness_value_is_exit(self, value):
    #     assertData.assert_text_exit(str(value), self.cur_brightness())

    def hand_type_modify_brightness(self, value=102):
        # 0:10%, 102:82%, 255:100%
        cmd = "settings put system screen_brightness %s" % str(value)

        text1 = ''
        if value != 102:
            if value == 0:
                text1 = "亮度已经修改为0了,  检查设置是否为0%, 请观察亮度变化有没有黑屏 "
            elif value == 31:
                text1 = "亮度已经修改为51%了,  检查设置是否为51%', 请观察亮度变化"
            elif value == 255:
                text1 = "亮度已经修改为100%了,  检查设置是否为100%, 请观察亮度变化"
            meta_alert.getAlert(text=text1)
        # act = self.cur_brightness()
        sim_code.simplify_no_return(cmd)
        # print(type(self.cur_brightness()))
        assertData.assert_text_exit(str(value), self.cur_brightness())

    def modify_brightness(self, value):
        cmd = "settings put system screen_brightness %s" % str(value)
        sim_code.simplify_no_return(cmd)
        assertData.assert_text_exit(str(value), self.cur_brightness())
        return str(value)

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
            my_text.write_text("默认亮度不超过90%")
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

    # 仅限限制第一次调用，用fixture
    def get_default_brightness_time_out(self):
        cmd = "settings get system screen_off_timeout"
        res = commData.send_shell_cmd(cmd).replace("\n", "").replace(" ", "")
        assertData.assert_text_file("默认的休眠时间是：", res)
        # sim_code.simplify_txt_file(cmd, "默认的休眠时间是：")
        return res

    def get_cur_brightness_time_out(self):
        cmd = "settings get system screen_off_timeout"
        act = commData.send_shell_cmd(cmd).replace("\n", "").replace(" ", "")
        return act

    def set_default_brightness_time_out(self, time_out):
        set_cmd = "settings put system screen_off_timeout %s" % time_out
        sim_code.simplify_no_return(set_cmd)
        exp = time_out
        assertData.assert_text_exit(exp, self.get_cur_brightness_time_out())

    def set_screen_sleep(self, time_out):
        cmd = "settings put system screen_off_timeout %s" % str(time_out)
        commData.send_shell_cmd(cmd)
        assertData.assert_text_exit(str(time_out), self.get_cur_brightness_time_out())

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

    def deal_brigthness_time_out(self, time_out, value):
        cmd = "settings put system screen_off_timeout %s" % value
        # cmd = "settings put system screen_off_timeout 60000"
        # if time_out.strip() == "永不":
        #     text = "设置了" + time_out + "休眠，" + "请并检查休眠情况" + " " * 100 + "\n" * 10
        # else:
        #     text = "设置了" + time_out + "休眠，" + "请" + time_out + "后前检查休眠情况" + " " * 100 + "\n" * 10
        # meta_alert.getAlert(text=text)
        # sim_code.simplify_no_return(cmd)
        commData.send_shell_cmd(cmd)
        assertData.assert_text_exit(value, self.get_cur_brightness_time_out())
        # if time_out.strip() == "15sec":
        #     for i in range(4):
        #         time.sleep(4)
        #         meg = "间隔%s秒睡眠状态为：%s" % ('4', self.get_screen_status())
        #         log.info(meg)
        #         my_text.write_text(meg)
        #
        # if time_out.strip() == "1min":
        #     for i in range(5):
        #         time.sleep(10)
        #         meg = "间隔%s秒睡眠状态为：%s" % ('10', self.get_screen_status())
        #         log.info(meg)
        #         my_text.write_text(meg)
        #     time.sleep(6)
        #     meg = "间隔%s秒睡眠状态为：%s" % ('6', self.get_screen_status())
        #     log.info(meg)
        #     my_text.write_text(meg)
        time.sleep(60)

        # time.sleep(5)
        # meg = "间隔%s秒睡眠状态为：%s" % ('5', self.get_screen_status())
        # log.info(meg)
        # my_text.write_text(meg)

        # if "永不" not in time_out:
        #     log.error("@@@永不休眠设置失败")
        #     assert "ON" in self.get_screen_status()

        # 唤醒
        self.sleep_and_wake_screen()
        # if time_out.strip() == "15min":
        #     time.sleep(900)

        # 待指令或接口，查询是否进入休眠、唤醒状态
        # if "永不" not in time_out:
        #     btn = meta_alert.get_yes_or_no("请检查设备有没有进入休眠模式" + " " * 100 + "\n" * 10)
        #     if btn == "否":
        #         err = "设置了" + time_out + "休眠，" + time_out + "后进入休眠失败"
        #         log.error(err)
        #         assert False, err
    #     # 唤醒屏幕，方便下一次观察

    def sleep_and_wake_screen(self):
        cmd = "input keyevent 26"
        commData.send_shell_cmd(cmd)
        # time.sleep(1)

    def get_ifconfig_relate_status(self, par):
        comment = par + "的状态为: "
        if self.get_ifconfig_param(par):
            assertData.assert_text_file(comment, str(1))
            return str(1)
        else:
            assertData.assert_text_file(comment, str(0))
            return str(0)

    def eth0_is_not_exit(self, par):
        assert par not in self.get_ifconfig_param(par)

    def eth0_is_exit(self, par):
        assert par in self.get_ifconfig_param(par)

    def get_ifconfig_param(self, par):
        cmd = "ifconfig |grep %s" % par
        my_text.write_text(cmd)
        return commData.send_shell_cmd(cmd)

    def print_ifconfig(self):
        cmd = "ifconfig"
        res = commData.send_shell_cmd(cmd)
        print(res)

    def get_default_bluetooth_status(self):
        cmd = "settings get global bluetooth_on"
        my_text.write_text(cmd)
        res = commData.send_shell_cmd(cmd).replace("\n", "").replace(" ", "")
        comment = "蓝牙的状态为: "
        if res:
            assertData.assert_text_file(comment, res)
            return res
        else:
            assertData.assert_text_file(comment, res)
            return res

    def get_cur_bluetooth_status(self):
        res = commData.send_shell_cmd("settings get global bluetooth_on")
        sim_code.print_log(res)
        return res

    def open_bluetooth_btn(self):
        if "1" not in self.get_cur_bluetooth_status():
            commData.send_shell_cmd("svc bluetooth enable")
            time.sleep(1)

    def close_bluetooth_btn(self):
        if "0" not in self.get_cur_bluetooth_status():
            commData.send_shell_cmd("svc bluetooth disable")
            # time.sleep(1)

    def bluetooth_open_status(self):
        assertData.assert_text_exit("1", self.get_cur_bluetooth_status())

    def bluetooth_close_status(self):
        assertData.assert_text_exit("0", self.get_cur_bluetooth_status())

    def get_cur_wifi_status(self):
        return commData.send_shell_cmd("settings get global wifi_on")

    def wifi_open_status(self):
        assertData.assert_text_exit("1", self.get_cur_wifi_status())

    def wifi_close_status(self):
        assertData.assert_text_exit("0", self.get_cur_wifi_status())

    def open_wifi_btn(self):
        if "0" in self.get_cur_wifi_status():
            commData.send_shell_cmd("svc wifi enable")
            self.wifi_open_status()

    def close_wifi_btn(self):
        if "1" in self.get_cur_wifi_status():
            commData.send_shell_cmd("svc wifi disable")
            self.wifi_close_status()

    def ping_ip_addr(self, times, addr):
        # 每隔0.6秒ping一次，一共ping5次
        # ping - c 5 - i 0.6 qq.com
        cmd = " ping -c %s %s" % (times, addr)
        exp = "ping: unknown host %s" % addr
        for i in range(5):
            res = commData.send_shell_cmd(cmd)
            sim_code.print_log(res)
            if exp not in res:
                break
            time.sleep(1)

        if exp in commData.send_shell_cmd(cmd):
            assert False, "无法上网,请检查网络"

    def get_permission(self, par):
        cmd = "pm list permissions | grep %s" % par
        comment = par + "权限情况"
        sim_code.simplify_txt_file(cmd, comment)

    def get_USB_permission(self):
        cmd = "ls -la /dev/bus/usb/0*"
        comment = "所有USB口的权限："
        sim_code.simplify_txt_file(cmd, comment)

    def click_go_back_btn(self):
        cmd = "input keyevent 4"
        sim_code.simplify_no_return(cmd)

    # 暂时不用，900P不太适用
    def click_seetings_btn_discard(self):
        cmd = "input keyevent 176"
        sim_code.simplify_no_return(cmd)

    def click_recent_items_btn(self):
        cmd = "input keyevent 187"
        sim_code.simplify_no_return(cmd)

    def click_home_btn(self):
        cmd = "input keyevent 3"
        sim_code.simplify_no_return(cmd)

    def get_cur_page(self):
        cmd = "dumpsys window | grep mCurrentFocus"
        return commData.send_shell_cmd(cmd)

    def page_is_exit(self, act_name):
        assertData.assert_text_exit(act_name, self.get_cur_page())

    # 休眠跟非休眠时状态不一样，等获取接口再改
    def get_settings_page(self, set_act):
        # cmd = "com.android.settings/com.android.settings.homepage.SettingsHomepageActivity"
        self.start_activity(set_act)
        assertData.assert_text_exit(set_act, self.get_cur_page())

    def get_home_page(self, home_page):
        assertData.assert_text_exit(home_page, self.get_cur_page())

    def get_recent_items_page(self, recent_page):
        # recent_page = "com.android.systemui/com.android.systemui.recents.RecentsActivity"
        assertData.assert_text_exit(recent_page, self.get_cur_page())

    def check_btns(self, pages):
        # home_page = "com.telpo.tpui/com.telpo.tpui.MainActivity"
        # 检查home按键
        # 进入settings:
        # 检查是否在setting页面
        self.get_settings_page(pages["set_page"])
        # 点击home健
        self.click_home_btn()
        time.sleep(1)
        self.get_home_page(pages["home_page"])
        # 返回按键检查
        # 检查是否在setting页面
        self.get_settings_page(pages["set_page"])
        # 点击返回按钮
        self.click_go_back_btn()
        # 检查是否在home页
        time.sleep(1)
        self.get_home_page(pages["home_page"])

        # 最近按键检查
        self.click_recent_items_btn()
        time.sleep(1)
        self.get_recent_items_page(pages["recent_page"])

        # 最后返回home
        self.click_home_btn()
        time.sleep(1)
        self.get_home_page(pages["home_page"])

    def click_increase_volume(self):
        cmd = "input keyevent 24"
        sim_code.simplify_no_return(cmd)

    def click_reduce_volume(self):
        cmd = "input keyevent 25"
        sim_code.simplify_no_return(cmd)

    def modify_date_time(self, date_time):
        # """date + % Y" " % m" " % d" " % H" " % M" " % S" " % N"""   精确到纳秒
        # eg: date 01111100  去掉后面的秒，默认为00
        # format: date +%Y%m%d.%H%M%S
        cmd = "date %s" % date_time
        res = commData.send_shell_cmd(cmd)
        sim_code.print_log(res)
        sim_code.simplify_text_exit("date +%Y\" \"%m\" \"%d\" \"%H\" \"%M\" \"%S", date_time)

    def get_cur_dev_date_time(self):
        res = commData.send_shell_cmd("date +%Y\"-\"%m\"-\"%d\" \"%H\":\"%M\":\"%S")
        # res = commData.send_shell_cmd("date")
        sim_code.print_log(res)
        return res

    def get_network_date_time(self):
        return datetime.datetime.now()

    def get_cur_time_zone(self):
        res = commData.send_shell_cmd("getprop persist.sys.timezone")
        sim_code.print_log(res)
        return res

    def modify_time_zone(self, time_zone):
        cmd = "setprop persist.sys.timezone %s" % time_zone
        commData.send_shell_cmd(cmd)
        # 验证是否修改成功
        assertData.assert_text_exit(time_zone, self.get_cur_time_zone())
        sim_code.print_log(self.get_cur_time_zone())

    def cur_time_sync_btn_status(self):
        cmd = "settings get global auto_time"
        res = commData.send_shell_cmd(cmd)
        sim_code.print_log(res)
        return res

    def cur_time_zone_sync_btn_status(self):
        cmd = "settings get global auto_time_zone"
        res = commData.send_shell_cmd(cmd)
        sim_code.print_log(res)
        return res

    def open_time_sync_btn(self):
        cmd = "settings put global auto_time 1"
        if "0" in self.cur_time_sync_btn_status():
            sim_code.simplify_no_return(cmd)
            assertData.assert_text_exit("1", self.cur_time_sync_btn_status())

    def close_time_sync_btn(self):
        cmd = "settings put global auto_time 0"
        if "1" in self.cur_time_sync_btn_status():
            sim_code.simplify_no_return(cmd)
            assertData.assert_text_exit("0", self.cur_time_sync_btn_status())

    def open_time_zone_sync_btn(self):
        cmd = "settings put global auto_time_zone 1"
        if "0" in self.cur_time_zone_sync_btn_status():
            sim_code.simplify_no_return(cmd)
            assertData.assert_text_exit("1", self.cur_time_zone_sync_btn_status())

    def close_time_zone_sync_btn(self):
        cmd = "settings put global auto_time_zone 0"
        if "1" in self.cur_time_zone_sync_btn_status():
            sim_code.simplify_no_return(cmd)
            assertData.assert_text_exit("0", self.cur_time_zone_sync_btn_status())

    def reboot_recovery(self):
        cmd = "am broadcast -a android.intent.action.FACTORY_RESET -p android --es android.intent.extra.REASON MasterClearConfirm"
        commData.send_shell_cmd(cmd)
        time.sleep(270)
        # meta_alert.get_yes_or_no("请确认设备已经恢复出厂设置了吗, 请set up SD卡并且打开USB debug后请点击确认")
        commData.adb_dev_exit()
        commData.adb_dev_completed()

    def get_screen_status(self):
        cmd = "dumpsys power | grep \"Display Power: state=\""
        res = commData.send_shell_cmd(cmd)
        sim_code.print_log(res)
        return res

    def screen_wake(self):
        if "OFF" in self.get_screen_status():
            self.sleep_and_wake_screen()
            assertData.assert_text_exit("ON", self.get_screen_status())

    def screen_sleep(self):
        if "ON" in self.get_screen_status():
            self.sleep_and_wake_screen()
            assertData.assert_text_exit("OFF", self.get_screen_status())

    def get_cur_screen_lock_status(self):
        cmd = "dumpsys window policy|grep showing="
        res = commData.send_shell_cmd(cmd)
        sim_code.print_log(res)
        if "false" in res:
            act = "unlock"
        else:
            act = "lock"
        meg = "当前锁屏状态为： %s" % act
        sim_code.print_log(res)
        my_text.write_text(meg)
        return res

    def unlock_screen(self):
        # 解锁, 唤醒功能
        cmd = "input keyevent 82"
        if "true" in self.get_cur_screen_lock_status():
            sim_code.simplify_no_return(cmd)
            # time.sleep(1)
            try:
                assertData.assert_text_exit("false", self.get_cur_screen_lock_status())
            except AssertionError:
                commData.send_shell_cmd(cmd)
                commData.send_shell_cmd(cmd)
                # time.sleep(1)
                assertData.assert_text_exit("false", self.get_cur_screen_lock_status())
                self.click_go_back_btn()

    def get_cur_mobile_data_status(self, sim_card):
        cmd = ""
        if sim_card == "sim_card1":
            cmd = "settings get global %s" % "mobile_data1"
        elif sim_card == "sim_card2":
            cmd = "settings get global %s" % "mobile_data2"
        elif sim_card == 'sim_card':
            cmd = "settings get global %s" % "mobile_data"
        res = commData.send_shell_cmd(cmd)
        sim_code.print_log(res)
        return res

    def check_data_default_status(self, sim_card):
        if "1" in self.get_cur_mobile_data_status(sim_card):
            my_text.write_text("%s当前移动数据开关状态: 1" % sim_card)
        elif "2" in self.get_cur_mobile_data_status(sim_card):
            my_text.write_text("%s当前移动数据开关状态: 0" % sim_card)
        else:
            my_text.write_text("%s当前移动数据开关状态: 0" % sim_card)

    def open_mobile_data(self, sim_card):
        cmd = "svc data enable"
        if "0" in self.get_cur_mobile_data_status(sim_card):
            sim_code.simplify_no_return(cmd)
            assertData.assert_text_exit("1", self.get_cur_mobile_data_status(sim_card))

    def close_mobile_data(self, sim_card):
        cmd = "svc data disable"
        if "1" in self.get_cur_mobile_data_status(sim_card):
            sim_code.simplify_no_return(cmd)
            assertData.assert_text_exit("0", self.get_cur_mobile_data_status(sim_card))

    def mobile_data_close_status(self, sim_card):
        assertData.assert_text_exit("0", self.get_cur_mobile_data_status(sim_card))

    def mobile_data_open_status(self, sim_card):
        assertData.assert_text_exit("1", self.get_cur_mobile_data_status(sim_card))

    def ifconfig_eth0_down(self):
        cmd = "ifconfig eth0 down"
        commData.send_shell_cmd(cmd)
        self.eth0_is_not_exit('eth0')

    def ifconfig_eth0_up(self):
        cmd = "ifconfig eth0 up"
        commData.send_shell_cmd(cmd)
        self.eth0_is_exit('eth0')

    # 待问
    def get_network_type(self):
        cmd = "getprop gsm.network.type"
        res = commData.send_shell_cmd(cmd)
        meg = "网络类型为： %s" % res
        log.info(meg)
        my_text.write_text(meg)

    def get_gps_status(self):
        cmd = "settings get secure location_providers_allowed"
        res = commData.send_shell_cmd(cmd)
        meg = "GPS状态为： %s" % res
        log.info(meg)
        my_text.write_text(meg)

    # 默认状态专用
    def get_auto_time_btn_status(self):
        cmd = "settings get global auto_time"
        res = commData.send_shell_cmd(cmd)
        meg = "当前的时间同步(auto_time_sync)按钮打开状态为： %s" % res
        sim_code.print_log(meg)
        my_text.write_text(meg)

    # 默认状态专用
    def get_auto_time_zone_btn_status(self):
        cmd = "settings get global auto_time_zone"
        res = commData.send_shell_cmd(cmd)
        meg = "当前的时区同步(auto_time_zone_sync)按钮打开状态为： %s" % res
        sim_code.print_log(meg)
        my_text.write_text(meg)

    def get_IMEI_info(self):
        # cmd = "settings list system|grep IMEI"
        cmd = "getprop |grep imei"
        res = commData.send_shell_cmd(cmd)
        meg = "IMEI_info： %s" % res
        sim_code.print_log(meg)
        my_text.write_text(meg)

    def get_MEID_info(self):
        # cmd = "settings list system|grep IMED"
        cmd = "getprop |grep meid"
        res = commData.send_shell_cmd(cmd)
        meg = "MEID_info： %s" % res
        sim_code.print_log(meg)
        my_text.write_text(meg)

    def get_volume_info(self, stream):
        cmd = "media volume --show --stream %s --get" % str(stream)
        res = commData.send_shell_cmd(cmd)
        meg = "当前的音量信息为： %s" % res
        sim_code.print_log(meg)
        my_text.write_text(meg)

    def get_cur_volume_value(self, stream):
        cmd = "settings get system %s" % str(stream)
        return int(sim_code.str_replace(commData.send_shell_cmd(cmd)))

    def set_volume_value(self, stream, value):
        cmd = "service call audio 10 i32 %s i32 %s i32 1" % (stream, value)
        sim_code.simplify_text_exit(cmd, "Result: Parcel")

    def check_volume_value(self, stream, value):
        act = self.get_cur_volume_value(stream)
        print("这是实际的值", act)
        print("这是设置的值", value)
        print(type(act))
        print(type(value))
        if value != act:
            sim_code.print_err_log("音量设置失败！！！")
            assert False, "音量设置失败！！！"
        sim_code.print_log("音量设置成功！！！")

    def get_serial_no(self):
        cmd = "getprop ro.serialno"
        log.info("设备的序列号为：%s" % commData.send_shell_cmd(cmd))
        my_text.write_text("设备的序列号为：%s" % commData.send_shell_cmd(cmd))

    def get_wlan0_mac(self):
        cmd = "cat sys/class/net/wlan0/address"
        log.info("wlan mac的地址为：%s" % commData.send_shell_cmd(cmd))
        my_text.write_text("wlan mac的地址为：%s" % commData.send_shell_cmd(cmd))

    def get_default_screen_off_timeout(self):
        return meta_alert.get_default_screen_time_out()

    def silent_install(self, command, apk, des="sdcard"):
        try:
            log.info("静默安装app应用")
            self.comm_push_file('APK', apk)
            # cmd = "am broadcast -a android.intent.action.application --es quiet_install /%s/%s" % (des, apk)
            cmd = command + " /%s/%s" % (des, apk)
            return commData.send_shell_cmd(cmd)
        except Exception as e:
            log.error(e)
            assert False, e

    def silent_uninstall(self, command, package):
        # cmd = "am broadcast -a android.intent.action.application --es uninstall %s" % package
        try:
            cmd = command + " %s" % package
            return commData.send_shell_cmd(cmd)
        except Exception:
            e = "@@@静默卸载失败！！！"
            log.error(e)
            assert False, e

#
# if __name__ == '__main__':
#     from Common.ADBCommand import ADBManage
#
#     adb = ADBManage()
#     adb.clientConnect()

#     inter = CommonInterface()
# inter.push_file("QQ_Music_old_version.apk")
