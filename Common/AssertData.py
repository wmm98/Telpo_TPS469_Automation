import sys
from os import path
import re
from Common.Log import MyLog, OutPutText
from Conf.Config import *
import allure
from Common import ADBCommand

log = MyLog()
MyText = OutPutText()


class OutData:

    def __init__(self):
        pass

    def text_file(self, comment, result):
        # print(result)
        # log.info("")
        try:
            # self.log_act_exp(result, exp="output.txt")
            # self.logInfo()
            # log.info(result)
            meg = "执行成功"
            self.log_info(meg)
            self.outPut(comment, result)
            log.info(comment)
            log.info(result)
            return True
        except Exception as e:
            errMeg = "写入output.txt出错， 请检查！！！"
            self.log_err(errMeg)
            assert False, errMeg

    def deal_string(self, par):
        res = par.replace("\n", "").replace(" ", "")
        return res

    def text_exit(self, exp, act):
        self.log_act_exp(act, exp)
        if self.deal_string(exp) in self.deal_string(act):
            meg = "执行成功"
            self.log_info(meg)
            return True
        else:
            if "Verityalreadydisabledon" not in self.deal_string(act):
                errInfo = "@@@@执行失败！！！%s不存在！！！不存在！！！， 请检查！！！" % exp
                self.log_err(errInfo)
                assert False, errInfo

    def text_not_exit(self, exp, act):
        self.log_act_exp(act, exp)
        # com.android.music 情况特殊，特殊处理
        if "com.android.music" in act:
            pattern = re.compile('.*com.*music$')
            result = re.search(pattern, act)
            if result == None:
                meg = "执行成功"
                self.log_info(meg)
                return True
            else:
                meg = "@@@@执行失败, %s不应该存在！！！, 请再检查一遍！！！" % exp
                self.log_err(meg)
                assert False, meg
        else:
            if self.deal_string(exp) not in self.deal_string(act):
                meg = "%s不存在, 执行成功" % exp
                self.log_info(meg)
                return True
            else:
                meg = "@@@@%s存在！！！实行失败, 请检查命令，手动测试确认！！！" % exp
                self.log_err(meg)
                assert False, meg

    def package_not_exit(self, act):
        if len(act) == 0:
            meg = "执行成功"
            self.log_info(meg)
            return True
        else:
            meg = "@@@执行失败，应用（app）不应该存在！！！， 请检查！！！"
            self.log_err(meg)
            assert False, meg

    def no_return(self, act):
        # if "com.android.music" in act:
        #     pattern = re.compile('.*com.*music$')
        #     result = re.search(pattern, act)
        #     if result == None:
        #         meg = "执行成功"
        #         self.log_info(meg)
        #     else:
        #         meg = "@@@执行失败，不应该有输出， 请检查！！！"
        #         self.log_err(meg)
        #         assert False, meg
        # else:
        if len(act) == 0:
            meg = "执行成功"
            self.log_info(meg)
            return True
        else:
            err_meg = "@@@执行失败，不应该有输出， 请检查！！！"
            self.log_err(err_meg)
            assert False, err_meg

    def is_true(self, act):
        if act == True:
            meg = "执行成功"
            self.log_info(meg)
            return True
        else:
            err_meg = "@@@执行失败, 请检查！！！"
            self.log_err(err_meg)
            assert False

    def is_false(self, act):
        if act == False:
            meg = "执行成功"
            self.log_info(meg)
            return True
        else:
            err_meg = "@@@执行失败， 请检查！！！"
            self.log_err(err_meg)
            assert False, err_meg

    def compare(self, low, high):
        if not low < high:
            assert False
        else:
            return True

    def log_act_exp(self, act, exp):
        # *meg :实际结果， 预期结果
        log.info("实际结果： \n %s" % act)
        log.info("预期结果： \n %s" % exp)
        print("实际结果： \n %s" % act)
        print("预期结果： \n %s" % exp)

    def log_err(self, meg):
        log.error(meg)
        print(meg)

    def log_info(self, meg):
        log.info(meg)
        print(meg)

    def outPut(self, comment, res):
        if len(res) > 100:
            MyText.write_text("%s \n" % comment)
            MyText.write_text(comment)
        MyText.write_text(comment)
        MyText.write_text(res)
