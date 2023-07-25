import allure
from Common import DealAlert, Shell
from Common.ADBCommand import ADBManage
from ADBInterface import DealInterface
import os
from Common.Log import MyLog, OutPutText
import time
import datetime

s_shell = Shell.Shell()
log = MyLog()
adbFunc = ADBManage()
alertFunc = DealAlert.AlertData()
my_text = OutPutText()


class Test_469_BaseFeature:

    def setup_class(self):
        # 获取芯片
        # self.chipPlan = alertFunc.getChip()
        # 获取设备名称
        # self.dev_name = alertFunc.get_dev_name()
        # 获取安卓版本
        self.androidVer = adbFunc.getAndrVer()
        self.interFunc = DealInterface.InterfaceData(self.androidVer)
        # 调用相应的接口
        self.interface = self.interFunc.interfaceReturn()
        self.dev = adbFunc.return_device()
        # 设置不休眠，解锁， 涉及到有些默认操作，开始运行先先不设置
        # self.interface.screen_wake()
        # self.interface.unlock_screen()
        # self.interface.set_screen_never_sleep(0)

    def teardown_class(self):
        # 设置不休眠，解锁
        self.interface.screen_wake()
        self.interface.unlock_screen()
        # self.interface.set_screen_sleep(2147483647)
        self.interface.set_screen_sleep(self.interface.get_default_screen_off_timeout())
        print("基本功能模块（冒烟测试）所有的测试用例运行完毕！！！")

    @allure.feature('TPS_469_TestBaseFeature-root')
    @allure.title("Root测试")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo1(self):
        log.info("********Root测试*********")
        my_text.write_text("********Root测试*********")
        self.interface.open_root_auth()

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("系统默认设置")
    @allure.description("""测试前的描述""")
    def test_469_demo2(self):
        log.info("********系统默认设置*********")
        my_text.write_text("********系统默认设置*********")
        self.interface.get_ifconfig_relate_status("wlan0")
        # 469为单一的口，网口/Type C口不可公用，待讨论一下
        self.interface.get_ifconfig_relate_status("eth0")
        self.interface.get_default_bluetooth_status()
        self.interface.get_permission("USB")
        self.interface.get_USB_permission()
        # 查看手机流量开关
        self.interface.check_data_default_status("sim_card")
        # 查看数据网络类型--可能要更正
        # self.interface.get_network_type()
        # 查看GPS状态
        self.interface.get_gps_status()
        # 查看锁屏状态
        self.interface.get_cur_screen_lock_status()
        #  查看音量大小，
        # self.interface.get_volume_offset()
        my_text.write_text("Media volume：")
        self.interface.get_volume_info("volume_music")
        my_text.write_text("Call volume：")
        self.interface.get_volume_info("volume_voice")
        my_text.write_text("Ring volume：")
        self.interface.get_volume_info("volume_ring")
        my_text.write_text("Alarm volume：")
        self.interface.get_volume_info("volume_alarm")
        # 默认亮度系统系数
        # 默认的百分比待指令
        # 查看默认亮度值
        def_brightness = self.interface.get_default_brightness()
        # self.interface.sys_brightness_setting()
        my_text.write_text("默认的亮度： %s" % str(def_brightness))
        # 时间同步按钮开关状态
        self.interface.get_auto_time_btn_status()
        self.interface.get_auto_time_zone_btn_status()
        # 默认的休眠时间
        # self.interface.get_default_brightness_time_out()
        my_text.write_text("默认休眠时间： %s" % self.interface.get_default_screen_off_timeout())
        # 默认亮度

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("CPU主频")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo3(self):
        log.info("********CPU主频测试*********")
        my_text.write_text("********CPU主频测试*********")
        for i in range(self.interface.kernals_sum()):
            self.interface.cur_cpu_freq(i)
            self.interface.max_cpu_freq(i)
            self.interface.min_cpu_freq(i)

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("系统类型")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo4(self):
        log.info("********系统类型测试*********")
        my_text.write_text("********系统类型测试*********")
        self.interface.cur_user()
        self.interface.selinux_auth()

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("存储空间分配")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo5(self):
        log.info("********存储空间分配测试*********")
        my_text.write_text("********存储空间分配测试*********")
        self.interface.check_DDR()

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("应用安装卸载(非静默)")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo6(self):
        log.info("********应用安装卸载测试*********")
        log.info("****删除内部应用测试****")
        self.interface.del_internal_app("com.android.settings")
        # self.interface.del_internal_app("com.android.theme.icon_pack.rounded.settings")
        # 安装测试

        # 测试前先卸载
        self.interface.pre_pro_test_uninstall("com.tencent.qqmusic")

        # 低版本安装测试
        log.info("****第一次低版本安装测试****")
        self.interface.comm_install("QQ_Music_old_version.apk")
        self.interface.comm_app_is_installed("com.tencent.qqmusic")
        app_old_version = self.interface.get_package_version("com.tencent.qqmusic")
        print(app_old_version)
        log.info("版本： %s" % app_old_version)
        try:
            self.interface.start_activity("com.tencent.qqmusic/.activity.AppStarterActivity")
            self.interface.single_process_exit("com.tencent.qqmusic")
        except AssertionError:
            self.interface.start_activity("com.tencent.qqmusic/.activity.AppStarterActivity")
            self.interface.single_process_exit("com.tencent.qqmusic")
        self.interface.force_stop_process("com.tencent.qqmusic")
        self.interface.single_process_not_exit("com.tencent.qqmusic")

        # 相同版本覆盖安装
        log.info("****相同版本覆盖安装测试****")
        self.interface.comm_install("QQ_Music_old_version.apk")
        self.interface.comm_app_is_installed("com.tencent.qqmusic")
        app_old_version = self.interface.get_package_version("com.tencent.qqmusic")
        print(app_old_version)
        log.info("版本： %s" % app_old_version)
        try:
            self.interface.start_activity("com.tencent.qqmusic/.activity.AppStarterActivity")
            self.interface.single_process_exit("com.tencent.qqmusic")
        except AssertionError:
            self.interface.start_activity("com.tencent.qqmusic/.activity.AppStarterActivity")
            self.interface.single_process_exit("com.tencent.qqmusic")
        self.interface.force_stop_process("com.tencent.qqmusic")
        self.interface.single_process_not_exit("com.tencent.qqmusic")

        # 高版本覆盖安装
        log.info("****相高版本覆盖安装覆盖安装测试****")
        self.interface.comm_install("QQ_Music_new_version.apk")
        self.interface.comm_app_is_installed("com.tencent.qqmusic")
        app_new_version = self.interface.get_package_version("com.tencent.qqmusic")
        print(app_new_version)
        log.info("版本： %s" % app_new_version)
        try:
            self.interface.start_activity("com.tencent.qqmusic/.activity.AppStarterActivity")
            self.interface.single_process_exit("com.tencent.qqmusic")
        except AssertionError:
            self.interface.start_activity("com.tencent.qqmusic/.activity.AppStarterActivity")
            self.interface.single_process_exit("com.tencent.qqmusic")
        self.interface.force_stop_process("com.tencent.qqmusic")
        self.interface.single_process_not_exit("com.tencent.qqmusic")
        #
        # 检查高低版本
        self.interface.assert_compare(app_old_version, app_new_version)

        log.info("****卸载应用测试****")
        # 卸载
        self.interface.comm_uninstall("com.tencent.qqmusic")
        self.interface.app_not_exit("com.tencent.qqmusic")

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("静默安装卸载")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo7(self):
        # 等待接口
        assert False, "@@@等待接口"
        # cmd_install = "am broadcast -a android.intent.action.application --es quiet_install"
        # try:
        #     self.interface.silent_install(cmd_install, "QQ_Music_old_version.apk")
        # except Exception:
        #     self.interface.silent_install(cmd_install, "QQ_Music_old_version.apk")
        # time.sleep(60)
        # self.interface.comm_app_is_installed("com.tencent.qqmusic")
        #
        # self.interface.start_activity("com.tencent.qqmusic/.activity.AppStarterActivity")
        # # 杀掉进程、检查进程
        # self.interface.single_process_exit("com.tencent.qqmusic")
        # self.interface.force_stop_process("com.tencent.qqmusic")
        # self.interface.single_process_not_exit("com.tencent.qqmusic")
        # cmd_uninstall = "am broadcast -a android.intent.action.application --es uninstall"
        # self.interface.silent_uninstall(cmd_uninstall, "com.tencent.qqmusic")
        # self.interface.app_not_exit("com.tencent.qqmusic")
        # self.interface.comm_rm_file("QQ_Music_old_version.apk")

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("内外部型号")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo8(self):
        log.info("********内外部型号检查*********")
        my_text.write_text("********内外部型号检查*********")
        self.interface.internal_model()
        self.interface.product_model()

    @allure.feature('TPS_TPS980P_TestBaseFeature')
    @allure.title("状态栏下拉")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo9(self, wake_and_unlock_screen):
        log.info("********状态栏下拉*********")
        # 允许下拉
        self.interface.drop_down_status_bar_close()
        # 查询下拉框返回结果，待问研发
        # self.interface.drop_down_status_bar_off()
        self.interface.service_show_drop_down_status_bar()
        self.interface.operate_screen_shot("drop_down_status_bar_0")
        self.interface.service_recover_drop_down_status_bar()
        # 禁止下拉
        self.interface.drop_down_status_bar_open()
        # # 查询下拉框返回结果，待问研发
        # self.interface.drop_down_status_bar_on()
        self.interface.service_show_drop_down_status_bar()
        self.interface.operate_screen_shot("drop_down_status_bar_1")
        self.interface.service_recover_drop_down_status_bar()

    @allure.feature('TPS_TPS980P_TestBaseFeature')
    @allure.title("导航栏")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo10(self, wake_and_unlock_screen):
        log.info("********导航栏*********")
        # 导航栏
        self.interface.hide_navigation_bar()
        self.interface.navigationbar_status_off()
        self.interface.operate_screen_shot("navigation_bar_status_bar_0")

        self.interface.show_navigation_bar()
        self.interface.navigationbar_status_on()
        self.interface.operate_screen_shot("navigation_bar_status_bar_1")

    @allure.feature('TPS_TPS980P_TestBaseFeature')
    @allure.title("状态栏")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo11(self, wake_and_unlock_screen):
        log.info("********状态栏*********")
        # 状态栏
        self.interface.hide_status_bar()
        self.interface.status_bar_off()
        self.interface.operate_screen_shot("status_bar_0")
        self.interface.show_status_bar()
        self.interface.status_bar_on()
        self.interface.operate_screen_shot("status_bar_1")

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("语言和输入法")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo12(self):
        log.info("********语言和输入法*********")
        my_text.write_text("********语言和输入法*********")
        # 语言和输入法
        my_text.write_text("********语言和输入法*********")
        # assert False, "@@@等待指令"
        # 语言和输入法
        if "zh-CN" in self.interface.langauga_input_method():
            self.interface.CN_defualt_language_input()
            self.interface.start_activity("com.android.settings/com.android.settings.Settings")
            self.interface.operate_screen_shot("before_transfer_language_default")
            # 国内的不能设置语言，注意
            self.interface.add_language("en-US")
            # 设置为英文
            self.interface.set_sys_langauge("en-US")
            time.sleep(1)
            self.interface.check_cur_language("en-US")
            # 截图
            self.interface.operate_screen_shot("after_transfer_language_English")
            # 切换回默认的语言
            self.interface.set_sys_langauge(self.interface.check_default_language())
            self.interface.check_cur_language(self.interface.check_default_language())
        else:
            # 先截图原来的语言
            self.interface.start_activity("com.android.settings/com.android.settings.Settings")
            self.interface.operate_screen_shot("before_transfer_language_default")
            # 添加中文
            self.interface.add_language("zh-CN")
            # 设置为中文
            self.interface.set_sys_langauge("zh-CN")
            time.sleep(1)
            self.interface.check_cur_language("zh-CN")
            # 截图
            self.interface.operate_screen_shot("after_transfer_language_Chinese")
            # 切换回默认的语言
            self.interface.set_sys_langauge(self.interface.check_default_language())
            self.interface.check_cur_language(self.interface.check_default_language())

    # TPS469
    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("播放音视频测试--半自动化")  # 设置case的名字
    @allure.description("""测试前的描述""")  # 添加描述
    def test_469_demo13(self, wake_and_unlock_screen, stop_gallery_3d_app):
        log.info("********金融类的播放音视频测试*********")
        if self.interface.pre_pro_app_is_exit("com.tencent.qqmusic"):
            self.interface.pre_pro_test_uninstall("com.tencent.qqmusic")
        # 测试前先杀掉
        # video = "testVideo.mp4" ["testMusic.mp3"]
        # ["testVideo.mp4", "testMusic.mp3", "testVideo.m4v"]
        meta_list = ["testVideo.mp4", "testMusic.mp3", "testVideo.m4v"]
        for video in meta_list:
            if "Music" in video:
                self.interface.comm_push_file("Media\\Music", video)
                self.interface.comm_ls_exit(video)
                act_name = "-n com.android.gallery3d/com.android.gallery3d.app.MovieActivity -d /sdcard/%s" % video
                self.interface.manual_listen_music(act_name)
                # 补充进程检查
                self.interface.single_process_exit("com.android.gallery3d")
                self.interface.media_adjust_volumn()
                self.interface.force_stop_process("com.android.gallery3d")
                self.interface.single_process_not_exit("com.android.gallery3d")
            else:
                self.interface.comm_push_file("Media\\Video", video)
                self.interface.comm_ls_exit(video)
                act_name = "-n com.android.gallery3d/com.android.gallery3d.app.MovieActivity -d /sdcard/%s" % video
                self.interface.manual_listen_music(act_name)
                # 补充进程检查
                self.interface.single_process_exit("com.android.gallery3d")
                self.interface.adjust_volumn()
                self.interface.force_stop_process("com.android.gallery3d")
                self.interface.single_process_not_exit("com.android.gallery3d")
                #
            self.interface.comm_rm_file(video)
            self.interface.comm_ls_not_exit(video)

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("默认亮度--半自动化")
    @allure.description("""测试前的描述""")
    def test_469_demo14(self, wake_and_unlock_screen, recovery_default_brightness, back_to_desktop):
        # 需要修改
        log.info("********默认亮度测试*********")
        my_text.write_text("********默认亮度测试*********")
        log.info("***查看默认亮度***")
        # 测试前调为默认的
        # self.interface.sys_brightness_setting()
        # 先进入Dipplay活动页面
        act_name = "com.android.settings/com.android.settings.DisplaySettings"
        self.interface.start_activity(act_name)
        self.interface.page_is_exit(act_name)
        # self.interface.hand_type_check_default_brightness()
        log.info("***修改亮度***")
        self.interface.hand_type_modify_brightness(0)
        self.interface.hand_type_modify_brightness(self.interface.get_default_brightness())
        self.interface.hand_type_modify_brightness(255)
        # 测试最后修改为默认
        time.sleep(2)

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("休眠时间设置")
    @allure.description("""测试前的描述""")
    def test_469_demo15(self):
        log.info("********休眠时间设置*********")
        my_text.write_text("********休眠时间设置*********")
        log.info("********休眠时间设置*********")
        my_text.write_text("********休眠时间设置*********")

        wake_cmd = "dumpsys window policy |grep mAwake="
        unlock_cmd = "dumpsys window policy|grep showing="
        # self.dev.shell("input keyevent 82")
        # self.dev.shell("input keyevent 82")
        # time.sleep(2)
        # assert "true" in self.dev.shell(wake_cmd)
        # self.dev.shell("settings put system screen_off_timeout %s" % str(2147483647))
        # assert str(2147483647) in self.dev.shell("settings get system screen_off_timeout")
        self.interface.reboot_dev()
        # alertFunc.getAlert("重启")
        # adbFunc.open_root()
        # adbFunc.open_remount()
        # 熄屏
        # if "true" in self.dev.shell(wake_cmd):
        #     self.dev.shell("input keyevent 26")
        #     time.sleep(3)
        #     assert "false" in self.dev.shell(wake_cmd)
        self.dev.shell("input keyevent 82")
        time.sleep(1)
        assert "true" in self.dev.shell(wake_cmd)
        # 解锁
        self.dev.shell("input keyevent 82")
        time.sleep(1)
        # 验证已经解锁
        assert "false" in self.dev.shell(unlock_cmd)
        my_text.write_text("##########设置1min后进入休眠################")
        my_text.write_text("开始计算======")

        self.dev.shell("settings put system screen_off_timeout %s" % str(60000))
        # assert str(60000) in self.dev.shell("settings get system screen_off_timeout")
        my_text.write_text("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        # print("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        for i in range(1, 31):
            time.sleep(2)
            my_text.write_text(str(i * 2) + "秒后 " + self.dev.shell(wake_cmd))
            # print(str(i*2) + "秒后 " + self.dev.shell(cmd))
        # print("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        my_text.write_text("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        assert "false" in self.dev.shell(wake_cmd)

        my_text.write_text("##########设置15sec后进入休眠################")
        my_text.write_text("开始计算======")
        self.dev.shell("input keyevent 82")
        self.dev.shell("input keyevent 82")
        time.sleep(2)
        assert "true" in self.dev.shell(wake_cmd)

        self.dev.shell("settings put system screen_off_timeout %s" % str(2147483647))
        assert str(2147483647) in self.dev.shell("settings get system screen_off_timeout")

        self.interface.reboot_dev()
        # 熄屏
        if "true" in self.dev.shell(wake_cmd):
            self.dev.shell("input keyevent 26")
            time.sleep(3)
            assert "false" in self.dev.shell(wake_cmd)
        self.dev.shell("input keyevent 82")
        time.sleep(1)
        assert "true" in self.dev.shell(wake_cmd)
        # 解锁
        self.dev.shell("input keyevent 82")
        time.sleep(1)
        assert "false" in self.dev.shell(unlock_cmd)
        my_text.write_text("开始计算======")

        self.dev.shell("settings put system screen_off_timeout %s" % str(15000))
        # assert str(60000) in self.dev.shell("settings get system screen_off_timeout")
        my_text.write_text("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        # print("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        for i in range(1, 15):
            time.sleep(1)
            my_text.write_text(str(i) + "秒后 " + self.dev.shell(wake_cmd))
            # print(str(i) + "秒后 " + self.dev.shell(cmd))
        # print("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        my_text.write_text("当前网络时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        assert "false" in self.dev.shell(wake_cmd)

        my_text.write_text("##########设置永不休眠################")
        self.dev.shell("input keyevent 82")
        self.dev.shell("input keyevent 82")
        time.sleep(2)
        assert "true" in self.dev.shell(wake_cmd)
        time.sleep(1)
        self.dev.shell("settings put system screen_off_timeout %s" % str(2147483647))
        assert str(2147483647) in self.dev.shell("settings get system screen_off_timeout")

    # 时间同步和时区
    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("WIFI时间同步测试")
    @allure.description("""测试前的描述""")
    def test_469_demo16(self, back_to_desktop):
        log.info("********WIFI时间同步测试*********")
        my_text.write_text("********WIFI时间同步测试*********")

        # 弹出弹窗连接wifi
        alertFunc.getAlert("************请连接wifi, 并且拔出网线**************")
        # 关闭网络
        # 确保以太网不存在"eth0"
        self.interface.ifconfig_eth0_down()
        # self.interface.close_wifi_btn()
        # self.interface.wifi_close_status()
        self.interface.close_mobile_data('sim_card')
        self.interface.mobile_data_close_status('sim_card')
        # self.interface.close_mobile_data('sim_card')
        # self.interface.mobile_data_close_status('sim_card')
        self.interface.wifi_open_status()
        # 修改时区为亚洲
        self.interface.modify_time_zone("Asia/Shanghai")
        # 关闭时区，时间按钮
        self.interface.close_time_sync_btn()
        self.interface.close_time_zone_sync_btn()

        # 修改网络时间
        self.interface.modify_date_time("10111000")
        cur_time = self.interface.get_cur_dev_date_time()
        my_text.write_text("修改后系统当前时间为：%s" % cur_time)
        log.info("修改后系统当前时间为：%s" % cur_time)
        cur_network_time = self.interface.get_network_date_time()
        my_text.write_text("当前网络时间为：%s" % cur_network_time)
        log.info("当前网络时间为：%s" % cur_network_time)

        self.interface.reboot_dev()

        log.info("********设备重启后**********")
        my_text.write_text("********设备重启后**********")

        self.interface.mobile_data_close_status('sim_card')
        # print("未开网络设备重启后的时间：", self.interface.get_cur_dev_date_time())
        # self.interface.wifi_close_status()
        # self.interface.eth0_is_not_exit("eth0")
        self.interface.open_wifi_btn()
        self.interface.wifi_open_status()

        # 确保能上网
        self.interface.ping_ip_addr(5, "www.baidu.com")
        self.interface.open_time_sync_btn()
        self.interface.open_time_zone_sync_btn()
        for i in range(3):
            cur_time_pro = self.interface.get_cur_dev_date_time()
            cur_network_time_pro = self.interface.get_network_date_time()
            my_text.write_text("设备重启并且打开时间同步按钮后当前时间为：%s" % cur_time_pro)
            log.info("设备重启并且打开时间同步按钮后当前时间为：%s" % cur_time_pro)
            my_text.write_text("当前网络时间为：%s" % cur_network_time_pro)
            log.info("当前网络时间为：%s" % cur_network_time_pro)
            time.sleep(5)
            # 每间隔5秒的时间更新状况
            log.info("每间隔5秒的时间更新状况")

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("sim卡时间同步测试")
    @allure.description("""测试前的描述""")
    def test_469_demo16_1(self, back_to_desktop, wake_and_unlock_screen):
        log.info("********sim卡时间同步测试*********")
        my_text.write_text("********sim卡时间同步测试*********")
        # 禁用wifi
        self.interface.ifconfig_eth0_down()
        self.interface.close_wifi_btn()
        self.interface.wifi_close_status()
        # self.interface.close_mobile_data('sim_card')
        # self.interface.mobile_data_close_status('sim_card')
        # self.interface.close_mobile_data('sim_card')
        # self.interface.mobile_data_close_status('sim_card')
        # 关闭时区，时间按钮
        self.interface.close_time_sync_btn()
        self.interface.close_time_zone_sync_btn()

        # 修改为国外时区
        self.interface.modify_time_zone("Pacific/Midway")

        # 修改网络时间
        self.interface.modify_date_time("01111100")
        cur_time = self.interface.get_cur_dev_date_time()
        my_text.write_text("修改花间后设备当前时间为：%s" % cur_time)
        log.info("修改时间后设备当前时间为：%s" % cur_time)
        cur_network_time = self.interface.get_network_date_time()
        my_text.write_text("当前网络时间为：%s" % cur_network_time)
        log.info("当前网络时间为：%s" % cur_network_time)

        # 暂定指令
        self.interface.reboot_dev()
        # self.interface.reboot_dev_only()

        log.info("********设备重启后**********")
        my_text.write_text("********设备重启后**********")

        # 确保wifi关闭
        # self.interface.wifi_close_status()
        # self.interface.mobile_data_close_status('sim_card')
        # self.interface.mobile_data_close_status('sim_card')
        # sim卡确保能上网
        self.interface.wifi_close_status()
        # self.interface.eth0_is_not_exit("eth0")
        self.interface.open_mobile_data('sim_card')
        self.interface.mobile_data_open_status('sim_card')
        self.interface.start_activity("am start com.android.launcher3/.Launcher")
        # time.sleep(3)
        self.interface.ping_ip_addr(5, "www.baidu.com")

        self.interface.open_time_sync_btn()
        self.interface.open_time_zone_sync_btn()
        for i in range(3):
            cur_time_pro = self.interface.get_cur_dev_date_time()
            cur_network_time_pro = self.interface.get_network_date_time()
            cur_time_zone = self.interface.get_cur_time_zone()
            my_text.write_text("设备重启并且打开时间同步按钮后当前时间为：%s" % cur_time_pro)
            my_text.write_text("当前网络时间为：%s" % cur_network_time_pro)
            my_text.write_text("当前时区为：%s" % cur_time_zone)
            log.info("设备重启并且打开时间同步按钮后当前时间为：%s" % cur_time_pro)
            log.info("当前网络时间为：%s" % cur_network_time_pro)
            log.info("当前时区为：%s" % cur_time_zone)
            time.sleep(5)
            # 每间隔5秒的时间更新状况
            log.info("每间隔5秒的时间更新状况")

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("触摸键测试")
    @allure.description("""测试前的描述""")
    def test_469_demo17(self, wake_and_unlock_screen):
        log.info("********按键测试*********")
        home_page = "com.android.launcher3/com.android.launcher3.Launcher"
        set_page = "com.android.settings/com.android.settings.Settings"
        recent_page = "com.android.systemui/com.android.systemui.recents.RecentsActivity"
        pages = {"home_page": home_page, "set_page": set_page, "recent_page": recent_page}
        self.interface.check_btns(pages)

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("触摸键测试--手工点击")
    @allure.description("""测试前的描述""")
    def test_469_demo17_1(self, wake_and_unlock_screen):
        alertFunc.getAlert("请手工确认下 ”返回键“、”Home键“、”最近键“")
        res = alertFunc.get_yes_or_no("测试通过吗？")
        if "是" not in res:
            assert False, "@@@测试失败！！！"

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("IMEI和MEID")
    @allure.description("""测试前的描述""")
    def test_469_demo18(self):
        log.info("********IMEI和MEID检查*********")
        my_text.write_text("********IMEI和MEID检查*********")
        self.interface.get_IMEI_info()
        self.interface.get_MEID_info()
        assert False, "@@@@@等待指令"

    @allure.feature('TPS_469_TestBaseFeature')
    @allure.title("音量设置与功能验证、亮度测试")
    @allure.description("""测试前的描述""")
    def test_469_demo19(self, back_to_desktop, recovery_default_brightness):
        log.info("********音量设置与功能验证*********")
        my_text.write_text("********音量设置与功能验证*********")
        # media
        # 先获取默认的的音量
        media_default_volume = self.interface.get_cur_volume_value("volume_music")
        if media_default_volume != 15:
            # 修改音量
            self.interface.set_volume_value("3", 15)
            media_volume = 15
        else:
            self.interface.set_volume_value("3", 0)
            media_volume = 0
        self.interface.check_volume_value('volume_music_speaker', media_volume)

        # call
        call_default_volume = self.interface.get_cur_volume_value("volume_voice")
        if call_default_volume != 5:
            # 修改音量
            self.interface.set_volume_value("0", 5)
            call_volume = 5
        else:
            self.interface.set_volume_value("0", 1)
            call_volume = 1
        self.interface.check_volume_value('volume_voice_earpiece', call_volume)

        # ring
        ring_default_volume = self.interface.get_cur_volume_value("volume_ring")
        if ring_default_volume != 7:
            # 修改音量
            self.interface.set_volume_value("2", 7)
            ring_volume = 7
        else:
            self.interface.set_volume_value("2", 0)
            ring_volume = 0
        self.interface.check_volume_value('volume_ring_speaker', ring_volume)

        # alarm
        alarm_default_volume = self.interface.get_cur_volume_value("volume_alarm")
        if alarm_default_volume != 7:
            # 修改音量
            self.interface.set_volume_value("4", 7)
            ring_volume = 7
        else:
            self.interface.set_volume_value("4", 1)
            ring_volume = 1
        self.interface.check_volume_value('volume_alarm_speaker', ring_volume)

        log.info("*******重启前后亮度比对测试*******")
        my_text.write_text("******重启前后亮度比对测试*******")
        # 修改亮度
        log.info("***修改亮度***")
        # if int(self.interface.get_default_brightness() != 255):
        #     self.interface.modify_brightness(255)
        #     brightness_value = str(255)
        # else:
        #     self.interface.modify_brightness(0)
        #     brightness_value = str(0)

        # 获取当前百分比，等待指令

        self.interface.reboot_dev()
        #
        self.interface.check_volume_value('volume_music_speaker', media_volume)
        self.interface.check_volume_value('volume_voice_earpiece', call_volume)
        self.interface.check_volume_value('volume_ring_speaker', ring_volume)
        self.interface.check_volume_value('volume_alarm_speaker', ring_volume)

        # 获取当前亮度
        # res = self.interface.cur_brightness()
        # # 对比当前百分比，等待指令
        # if brightness_value not in res:
        #     assert False, "@@@重启前后亮度值不一致, 请检查！！！"

    @allure.feature('TPS_TPS980P_TestBaseFeature')
    @allure.title("恢复出厂测试")
    @allure.description("""测试前的描述""")
    def test_469_demo20(self):
        log.info("********恢复出厂测试*********")
        my_text.write_text("*****************恢复出厂测试*******************")
        # alertFunc.get_yes_or_no("请确认SD卡 setup 为外部存储")
        my_text.write_text("**********这是恢复出厂设置前的信息*******")
        test_file = "QQ_Music_new_version.apk"
        package = "com.tencent.qqmusic"

        if not self.interface.pre_pro_app_is_exit(package):
            self.interface.pre_pro_test_uninstall(package)
            # # 传文件到sdcard下
            self.interface.comm_push_file("APK", test_file)
            self.interface.comm_ls_exit(test_file)
            my_text.write_text("sdcard目录下存在 %s" % test_file)
            # 传文件到外部SD卡下
            # self.interface.comm_push_file("APK", test_file, des="storage/9242-DA74")
            # self.interface.comm_ls_exit(test_file, des="storage/9242-DA74")
            # my_text.write_text("外部SD目录下存在 %s" % test_file)

            # 安装一个app
            self.interface.comm_install(test_file)

            self.interface.app_is_exit(package)
        my_text.write_text("已经安装了QQ音乐软件 %s" % package)

        # 打开wifi,蓝牙
        self.interface.open_bluetooth_btn()
        self.interface.bluetooth_open_status()
        my_text.write_text("蓝牙状态：1")
        self.interface.open_wifi_btn()
        self.interface.wifi_open_status()
        my_text.write_text("wifi状态：1")
        # 检查GPS状态
        self.interface.get_gps_status()
        # self.interface.get_

        self.interface.get_wlan0_mac()
        self.interface.get_serial_no()

        # 修改默认亮度
        def_res = self.interface.get_default_brightness()
        if def_res != '0':
            res_bri_pre = self.interface.modify_brightness(0)
        else:
            res_bri_pre = self.interface.modify_brightness(255)
        my_text.write_text("当前亮度为 %s" % res_bri_pre)

        my_text.write_text("**IMEI和MEID检查**")
        self.interface.get_IMEI_info()
        self.interface.get_MEID_info()

        # 修改网络时间
        self.interface.modify_date_time("01111100")
        cur_time = self.interface.get_cur_dev_date_time()
        my_text.write_text("修改当前时间为：%s" % cur_time)
        # U盘恢复出设置测试自己手测
        self.interface.reboot_recovery()
        # time.sleep(120)
        # alertFunc.get_yes_or_no("请确认设备已经恢复出厂设置了吗, 请set up SD卡并且打开USB debug后请点击确认")
        log.info("***************这是恢复出厂设置后的的信息*******************")
        my_text.write_text("***************这是恢复出厂设置后的的信息*******************")
        # 重开root权限
        self.interface.open_root_auth()
        pro_time = self.interface.get_cur_dev_date_time()
        my_text.write_text("恢复出场设置后时间为：%s" % pro_time)

        try:
            # self.interface.comm_ls_exit(test_file, des="storage/9242-DA74")
            # my_text.write_text("外部SD目录下存在 %s" % test_file)
            # self.interface.app_not_exit(package)
            my_text.write_text("QQ音乐软件已不存在")
            self.interface.comm_ls_not_exit(test_file)
            my_text.write_text("sdcard目录存不存在 %s" % test_file)
        except AssertionError as e:
            err = "@@@恢复出场设置时候还存在安装文件，app ,恢复出厂设置失败, 请手动检查一遍！！！"
            log.error(err)
            my_text.write_text(err)
            assert False, err

        res_wifi = self.interface.get_cur_wifi_status()
        my_text.write_text("wifi状态：%s" % res_wifi)
        res_blue = self.interface.get_cur_bluetooth_status()
        my_text.write_text("蓝牙状态：%s" % res_blue)
        # 检查GPS状态
        self.interface.get_gps_status()

        self.interface.get_wlan0_mac()
        self.interface.get_serial_no()

        res_bri_pro = self.interface.cur_brightness()
        my_text.write_text("当前亮度为 %s" % res_bri_pro)

        my_text.write_text("**IMEI和MEID检查**")
        self.interface.get_IMEI_info()
        self.interface.get_MEID_info()

        my_text.write_text("当前时区为：%s" % self.interface.get_cur_time_zone())
        log.info("当前时区为：%s" % self.interface.get_cur_time_zone())
