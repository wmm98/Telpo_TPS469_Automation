import time
from Conf import Config
import os
from ppadb.client import Client as AdbClient
from Common.Shell import *
from Common import Log
import pyautogui
import datetime
import ppadb
from Common import DealAlert

conf = Config.Config()
log = Log.MyLog()
shell = Shell()
alert_ = DealAlert.AlertData()


class ADBManage:
    def __init__(self):
        pass

    def clientConnect(self):
        try:
            global device, dev_name
            client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037
            devices = client.devices()

            if len(devices) == 0:
                # print('没有连接上设备， 请检查数据线的连接！！！')
                meg = '没有连接上设备， 请检查数据线的连接！！！'
                log.info(meg)
                raise Exception(meg)

            # 连接输入的设备
            input_dev = self.get_input_dev()
            if input_dev != 0:
                for dev in devices:
                    if dev.serial == input_dev:
                        device = dev
                        # print(device.serial)
                        sucessInfo = "设备连接成功!"
                        print(sucessInfo)
                        log.info(sucessInfo)

                        # return device, client
                        return device
            else:
                device = devices[0]
                dev_name = device.serial
                return device
            # return devices[0]
        except Exception as e:
            errInfo = '设备连接失败！！！,%s' % e
            log.error(errInfo)
            assert False, errInfo

    def return_device(self):
        return device

    def get_input_dev(self):
        return alert_.get_dev_name()

    def get_device_ser(self):
        res = (alert_.adb_devices_serial() + "device").replace("\n", "").replace(" ", "")
        return res

    # 在测试开始的时候执行,在run.py里面运行,暂时不用
    def adbDevices(self, command):
        devices = shell.invoke(command)
        # time.sleep(2)
        return devices

    # 查看安卓版本,chip方案
    def checkAndrVer(self):
        # 查看安卓版本, 0：睡眠时间
        global andriodVer
        andriodVer = self.adb_shell_cmd('getprop ro.build.version.release', 0).strip().replace("\n", '')
        # returnStr = self.adb_shell_cmd('dmesg | grep Machine')
        # chipPlan = ''
        verInfo = "安卓的版本是： Android %s" % andriodVer
        log.info(verInfo)
        print(verInfo)
        # return andriodVer

    def getAndrVer(self):
        return andriodVer

    # 进入安卓系统后可以输入的命令
    def adb_shell_cmd(self, command, times):
        try:
            returnStr = device.shell(command, timeout=120)
            self.logMeg(command)
            if times == 0:
                time.sleep(1)
            else:
                time.sleep(times)
            return returnStr
        except RuntimeError as e:
            print("USB连接断开，请检查USB连接！！！")
            raise RuntimeError
        except Exception as e:
            err = '发送指令: %s -> %s, 请检查命令！！！' % (command, e)
            # 沙袋哦当前的任务，避免占用还在执行命令，占用资源
            # print(res)
            assert False, err

    # 调用进程
    def sub_process_cmd(self, cmd, times):
        input_dev = self.get_input_dev()
        if input_dev != 0:
            command = "adb -s %s shell %s" % (input_dev, cmd)
        else:
            command = "adb -s %s shell %s" % (dev_name, cmd)
        try:
            returnStr = shell.invoke(command)
            self.logMeg(command)
            if times == 0:
                time.sleep(1)
            else:
                time.sleep(times)
            return returnStr
        except Exception as e:
            log.error("请检查连接， 发送指令失败！！！")
            raise e

        # 调用进程

    def sub_adb_cmd(self, cmd, times):
        try:
            input_dev = self.get_input_dev()
            if input_dev != 0:
                command = "adb -s %s %s" % (input_dev, cmd)
            else:
                command = "adb -s %s %s" % (dev_name, cmd)
            returnStr = shell.invoke(command)
            self.logMeg(command)
            if times == 0:
                time.sleep(1)
            else:
                time.sleep(times)
            return returnStr
        except Exception as e:
            log.error("请检查连接， 发送指令失败！！！")
            raise e

    def logMeg(self, cmd):
        exp_boot = "getprop sys.boot_completed".replace("\n", "").strip()
        exp_dev = "adb devices".replace("\n", "").strip()
        if exp_boot not in cmd:
            if exp_dev not in cmd:
                log.info(cmd)
                print(cmd)

    def install_app1(self, apk):
        try:
            log.info("安装app应用")
            path = conf.project_path + '\\APK\\' + apk
            print(path)
            return device.install(path, reinstall=True)
        except ppadb.InstallError as e:
            err = "安装错误-低版本的app不能覆盖高版本app,请在测试之前先卸载高版本的app"
            assert False, err
        except Exception as e:
            assert False, e
            
    def install_app(self, apk):
        try:
            log.info("安装app应用")
            path = conf.project_path + '\\APK\\' + apk
            print(path)
            # self.push_file(dire='APK', file_name=apk, des="sdcard")
            # return device.install(path, reinstall=True, grand_all_permissions=True)
            return self.sub_adb_cmd("install -r %s" % path, 0)
        except ppadb.InstallError as e:
            err = "安装错误-低版本的app不能覆盖高版本app,请在测试之前先卸载高版本的app"
            assert False, err
        except Exception as e:
            assert False, e

    def install_app(self, apk):
        try:
            log.info("安装app应用")
            path = conf.project_path + '\\APK\\' + apk
            print(path)
            # self.push_file(dire='APK', file_name=apk, des="sdcard")
            # return device.install(path, reinstall=True, grand_all_permissions=True)
            return self.sub_adb_cmd("install -r %s" % path, 0)
        except ppadb.InstallError as e:
            err = "安装错误-低版本的app不能覆盖高版本app,请在测试之前先卸载高版本的app"
            assert False, err
        except Exception as e:
            assert False, e

    def uninstall_app(self, package):
        try:
            log.info("卸载app应用")
            timeout = 15
            timedelta = 1
            end_time = time.time() + timeout
            res = device.uninstall(package)
            if time.time() > end_time:
                log.error("卸载app超过15秒！！！")
                assert False, "卸载app超过15秒！！！"
            return res
        except Exception as e:
            assert False, e

    def app_is_installed(self, package):
        log.info("检查%s的安装情况" % package)
        return device.is_installed(package)

    def get_package_ver_name(self, package):
        log.info("%s 的当前版本：" % package)
        return device.get_package_version_name(package)

    def push_file_discard(self, dire, file_name):
        try:
            src = conf.project_path + '/' + dire + '/' + file_name
            log.info("从%s push %s到 %s里面" % (src, file_name, "sdcard"))
            # print(os.path.exists(conf.project_path + '/' + dire + '/'))
            # src = "E:\Mingming\Telpo_Automation\Telpo_Automation_V2\APK\%s" % apk
            print(src)
            device.push(src, '/sdcard/%s' % file_name)
        except FileNotFoundError as e:
            assert False, e
        except Exception as e:
            log.error("push文件失败")
            assert False, e

    def push_file(self, dire, file_name, des="sdcard"):
        try:
            src = conf.project_path + '/' + dire + '/' + file_name
            log.info("从%s push %s到 %s里面" % (src, file_name, des))
            print(src)
            cmd = "push %s /%s/" % (src, des)
            return self.sub_adb_cmd(cmd, 0)
        except FileNotFoundError as e:
            log.error(e)
            assert False, e
        except Exception as e:
            log.error(e)
            assert False, e

    def pull_file(self, file_name, org="sdcard"):
        try:
            src = org + '/' + file_name
            des = conf.project_path + "/%s" % "ScreenShot"
            log.info("从%s pull %s到 %s里面" % (src, file_name, "ScreenShot"))
            print(src)
            cmd = "pull %s %s/%s" % (src, des, file_name)
            return self.sub_adb_cmd(cmd, 0)
        except Exception as e:
            log.error(e)
            assert False, e

    def open_root(self):
        try:
            self.logMeg("执行root")
            res = self.sub_adb_cmd("root", 0)
            if len(res) == 0:
                return True
            else:
                log.error("@@@root出错,请检查！！！")
                return False
        except Exception as e:
            log.error(e)
            assert False, e

    def open_remount(self):
        try:
            self.logMeg("执行remount")
            act = self.sub_adb_cmd("remount", 0)
            if "remount succeeded" in act:
                return True
            else:
                log.error("@@@remount出错, 请检查！！！")
                return False
        except Exception as e:
            assert False, "@@@remount出错， 请检查！！！"

    def device_exit(self):
        print("运行到这里=====device==========")
        while True:
            res = self.adbDevices("adb devices")
            # res = self.adbDevices("adb devices")
            if self.get_device_ser() in res.replace('\r', '').replace('\t', '').replace(' ', ''):
                break
            time.sleep(2)

    def device_boot_complete(self):
        print("运行到这里=====boot==========")
        try:
            while True:
                boot_res = self.sub_process_cmd("getprop sys.boot_completed", 0)
                print(boot_res)
                if str(1) in boot_res:
                    break
                time.sleep(2)
        except Exception as e:
            err = "@@@%s 启动还没有完全启动，完全启动超时！！！" % e
            log.error(err)
            assert False, err

    def rebootDevice(self, wait=10):
        # try:
        timeout = 90
        timedelta = 1
        end_time = time.time() + timeout
        # ser = self.get_input_dev()
        self.sub_adb_cmd("reboot", 0)
        time.sleep(wait)
        # 系统完全启动
        self.device_exit()
        self.device_boot_complete()
        if time.time() > end_time:
            assert False, "系统完全启动时间超过90秒！！！"
        # except Exception as e:
        #     err = "%s 重启出问题" % e
        #     assert False, err

    # def device_boot_complete(self):
    #     try:
    #         while True:
    #             boot_res = self.sub_process_cmd("getprop sys.boot_completed", 0)
    #             print(boot_res)
    #             if str(1) in boot_res:
    #                 break
    #             time.sleep(2)
    #     except Exception as e:
    #         err = "@@@%s 启动还没有完全启动，完全启动超时！！！" % e
    #         log.error(err)
    #         assert False, err

    def reboot_no_debug_auth(self, wait_time=30):
        self.sub_process_cmd("svc power reboot", 0)
        time.sleep(wait_time)
        alert_.getAlert("设备重启后，请打开USB debug模式再关掉提示窗")
        self.device_exit()
        self.device_boot_complete()

    def power_restart_devices(self, wait=10):
        # try:
        timeout = 90
        timedelta = 1
        end_time = time.time() + timeout
        self.adb_shell_cmd("svc power reboot", 0)
        time.sleep(wait)
        # 系统完全启动
        self.device_exit()
        self.device_boot_complete()
        if time.time() > end_time:
            assert False, "系统完全启动时间超过90秒！！！"
        # except Exception as e:
        #     err = "%s 重启出问题" % e
        #     assert False, err

    # def serial_no(self):
    #     print(device.serial)
    #     return device.serial

# if __name__ == '__main__':
#     pass
#     client_dev = ADBManage()
#     dev = client_dev.clientConnect()
#     client_dev.serial_no()
# # client_dev.rebootDevice()
# res = client_dev.sub_process_cmd("adb shell getprop sys.boot_completed", 0)
# print(res)
# client_dev.sub_process_cmd("adb reboot", 0)
# client_dev.sub_process_cmd("adb kill-server", 0)
# client_dev.sub_process_cmd("adb start-server", 0)
# while True:
#     res = client_dev.sub_process_cmd("adb devices", 0)
#     if dev.serial in res:
#         print(res)
#         boot_res = client_dev.sub_process_cmd("adb shell \"getprop sys.boot_completed\"", 0)
#         print(type(boot_res))
#         if str(1) in boot_res:
#             print(boot_res)
#             break
#         time.sleep(2)
# # dev.root()
# client_dev.sub_process_cmd("adb root", 0)
# rem_res = client_dev.sub_process_cmd("adb remount", 0)
# print(rem_res)
# dev.remount()
# push_res = client_dev.push_file("APK", "QQ_Music_new_version.apk")
# print(push_res)
# while True:
# res = client_dev.adb_shell_cmd("getprop sys.boot_completed", 0)
# inst_res = client_dev.install_app("QQ_Music_old_version.apk")
# print(inst_res)
# is_inst_res = client_dev.app_is_installed("com.tencent.qqmusic")
# print(is_inst_res)
# uninst_res = client_dev.uninstall_app("com.tencent.qqmusic")
# print(uninst_res)
# r_res = dev.root()
# re_res = dev.remount()
# print(re_res)

# client_dev.device_boot_complete()
