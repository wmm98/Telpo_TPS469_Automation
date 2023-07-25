import sys
from os import path
import re

from Common.Log import MyLog, OutPutText
from Conf.Config import *
import allure
from Common import AssertData

assert_res = AssertData.OutData()
log = MyLog()
MyText = OutPutText()


# 断言判断类
class AssertOutput:

    def __init__(self):
        pass

    def assert_text_file(self, comment, res):
        return assert_res.text_file(comment, res)

    def assert_text_exit(self, exp, act):
        return assert_res.text_exit(exp, act)

    def assert_text_not_exit(self, exp, act):
        return assert_res.text_not_exit(exp, act)

    def assert_package_not_exit(self, act):
        return assert_res.package_not_exit(act)

    def assert_no_return(self, act):
        return assert_res.no_return(act)

    def assert_is_true(self, act):
        return assert_res.is_true(act)

    def assert_is_false(self, act):
        return assert_res.is_false(act)

    def compare_(self, low, high):
        return assert_res.compare(low, high)

