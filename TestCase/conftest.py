"""

# @allure.feature # 用于定义被测试的功能，被测产品的需求点
# @allure.story # 用于定义被测功能的用户场景，即子功能点
# @allure.severity #用于定义用例优先级
# @allure.issue #用于定义问题表识，关联标识已有的问题，可为一个url链接地址
# @allure.testcase #用于用例标识，关联标识用例，可为一个url链接地址

# @allure.attach # 用于向测试报告中输入一些附加的信息，通常是一些测试数据信息
# @pytest.allure.step # 用于将一些通用的函数作为测试步骤输出到报告，调用此函数的地方会向报告中输出步骤
# allure.environment(environment=env) #用于定义environment

"""
import sys
import time

import os
from ADBInterface import CommonADB
from ADBInterface.RK import RKChip
import allure
import pytest

# from Conf import Config
# conf = Config.Config()

comm_adb = CommonADB.CommonInterface()
rk_comm_adb = RKChip.RKInterface()


@pytest.fixture()
def wake_and_unlock_screen():
    # 获取默认的睡眠时间
    comm_adb.set_screen_sleep(2147483647)
    rk_comm_adb.screen_wake()
    rk_comm_adb.unlock_screen()
    yield
    comm_adb.set_screen_sleep(2147483647)
    #
    # print(res)
    # comm_adb.screen_sleep()
    # 亮屏
    rk_comm_adb.screen_wake()
    # 解锁
    rk_comm_adb.unlock_screen()


@pytest.fixture()
def sleep_and_lock_screeen():
    rk_comm_adb.screen_sleep()


@pytest.fixture()
def sleep_screen():
    rk_comm_adb.screen_sleep()
    yield
    print("")


@pytest.fixture()
def back_to_desktop():
    print("")
    yield
    # RK原生
    # comm_adb.start_activity("com.android.launcher3/.Launcher")
    # 按home键
    comm_adb.click_home_btn()
    comm_adb.click_home_btn()


@pytest.fixture()
def recovery_default_brightness():
    print("")
    yield
    # 第一次运行的时候为默认
    comm_adb.modify_brightness(comm_adb.get_default_brightness())


@pytest.fixture()
def stop_gallery_3d_app():
    comm_adb.pre_pro_force_stop_process("com.android.gallery3d/com.android.gallery3d.app.MovieActivity")
    comm_adb.force_stop_process("com.android.music")
    yield
    # comm_adb.start_activity("com.telpo.tpui/com.telpo.tpui.MainActivity")
    print("")
