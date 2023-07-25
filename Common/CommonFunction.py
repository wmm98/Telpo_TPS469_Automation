from Conf.Config import *
from Common import ADBCommand
from Common import AssertResult
import time

adbFun = ADBCommand.ADBManage()
outPut = AssertResult.AssertOutput()

log = Log.MyLog()
conf = Config()


class CommonData:

    def __init__(self):
        pass

    def adb_root(self):
        return adbFun.open_root()

    def adb_remout(self):
        return adbFun.open_remount()

    def adb_reboot(self):
        adbFun.rebootDevice()
        # self.reconnect()

    def send_shell_cmd(self, cmd, waitTime=0):
        # 处理接收超时
        return adbFun.adb_shell_cmd(cmd, times=waitTime)

    def send_sub_pro_cmd(self, cmd, waitTime=0):
        # 处理接收超时
        return adbFun.sub_process_cmd(cmd, times=waitTime)

    def adb_install(self, path):
        return adbFun.install_app(path)

    def adb_uninstall(self, package):
        return adbFun.uninstall_app(package)

    def adb_app_is_installed(self, package):
        return adbFun.app_is_installed(package)

    def get_package_ver(self, package):
        return adbFun.get_package_ver_name(package)

    def adb_push(self, dire, apk, des="sdcard"):
        return adbFun.push_file(dire, apk, des)

    def adb_pull(self, file_name, org="sdcard"):
        return adbFun.pull_file(file_name, org)

    def adb_rm_file(self, file_name, des="sdcard"):
        return adbFun.adb_shell_cmd("rm %s/%s", (des, file_name))

    # def adb_boot_complete(self):
    #     adbFun.device_boot_complete()

    def adb_reboot_no_debug_auth(self):
        adbFun.reboot_no_debug_auth(wait_time=30)

    def adb_restart_devices(self):
        adbFun.power_restart_devices(wait=15)

    def adb_dev_exit(self):
        return adbFun.device_exit()

    def adb_dev_completed(self):
        return adbFun.device_boot_complete()

    #
    # def time_out(self, timeout=10):
    #     end_time = time.time() + timeout
    #     if time.time() > end_time:
    #         log.info("超时接收命令， 持续时间为：%s" % )


if __name__ == '__main__':
    adbFun.clientConnect()
    data = CommonData()
    data.adb_push("APK", "QQ_Music_old_version.apk")
