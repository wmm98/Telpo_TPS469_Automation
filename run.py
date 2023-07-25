"""
运行用例集：
    python3 run.py

# '--allure_severities=critical, blocker'
# '--allure_stories=测试模块_demo1, 测试模块_demo2'
# '--allure_features=测试features'

"""
import sys

import pytest
from Common import Log
from Common import Shell
import subprocess
from Conf import Config
import os
import os.path
import time
import shutil
import datetime
from Common import DealAlert, ADBCommand

if __name__ == '__main__':
    # 初始化
    alert = DealAlert.AlertData()
    # 加载弹窗, 获取设备名称
    # alert.alertChip()
    alert.input_prompt()

    client = ADBCommand.ADBManage()
    # 连接上adb server
    client.adbDevices("adb devices")
    # 建立连接
    res = client.clientConnect()
    # 安卓版本
    client.checkAndrVer()
    # 第一次查看默认亮度
    alert.querry_default_brightness(res.serial)
    # alert.get_default_default_brightness()
    # 第一次查看默认设置的睡眠时间
    alert.querry_default_screen_off_time_out(res.serial)
    alert.device_serial_client(res)

    conf = Config.Config()
    log = Log.MyLog()
    shell = Shell.Shell()
    # 先进行登录

    log.info('initialize Config, path=' + conf.conf_path)

    # 获取报告地址
    xml_report_path = conf.xml_report_path
    html_report_path = conf.html_report_path

    # 清空XML文件夹然后重创文件夹
    # if os.path.exists(xml_report_path):
    #     shutil.rmtree(xml_report_path)h
    ##     log.error('Failed to execute case, check environment configuration!!')
    #     raise
    pro_path = conf.project_path + "\\Report\\environment.properties"
    # print(pro_path)

    env_path = pro_path
    # # 定义测试集
    allure_list = '--allure-features=TPS_469_TestBaseFeature-root,TPS_469_TestBaseFeature'
    # allure_story = '--allure-stories=pytest_de
    #     shutil.copy(env_path, xml_report_path)bug_story'
    # pytest -s --allure-features pytest_debug
    # pytest -s --allure-features pytest_debug --allure-stories pytest_debug_story

    # 运行选中的case
    args = ['-s', '-q', '--alluredir', xml_report_path, allure_list]
    # args = ['-s', '-q', '--alluredir', xml_report_path, allure_list, allure_story]

    # 如下参数不添加allure_list，会自动运行项目里面带有feature侦听器的的所有case
    # args = ['-s', '-q', '--alluredir', xml_report_path]
    log.info('Execution Testcases List：%s' % allure_list)
    curr_time = datetime.datetime.now()
    # print(curr_time)
    log.info('Execution Testcases start time: %s' % curr_time)
    pytest.main(args)
    cmd = 'allure generate %s -o %s --clean' % (xml_report_path, html_report_path)
    # 复制后的项目可手动清除或生成
    # allure generate xml -o html --clean

    try:
        shell.invoke(cmd)
        # print(cmd)
    except Exception:
        log.error('@@@执行失败， 请检查环境配置！！！')
        raise

    # allure生成报表，并启动程序
    # subprocess.call(cmd, shell=True)
    # subprocess.call('allure open -h 127.0.0.1 -p 9999 ./report/html', shell=True)

    # 打开报告
    end_time = datetime.datetime.now()
    print(end_time)
    testpreiod = end_time - curr_time
    print(testpreiod)
    log.info('Execution Testcases End time: %s' % end_time)
    log.info('Execution Testcases total time: %s' % testpreiod)
