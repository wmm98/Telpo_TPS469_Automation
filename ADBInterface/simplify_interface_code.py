from Common import AssertResult, CommonFunction
import os
from Common.Log import MyLog, OutPutText
import re

# path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
ass_res = AssertResult.AssertOutput()
comm_func = CommonFunction.CommonData()
log = MyLog()
my_text = OutPutText()


class simplify_code:
    def __init__(self):
        pass

    def simplify_txt_file(self, cmd, comment):
        act = comm_func.send_shell_cmd(cmd)
        return ass_res.assert_text_file(comment, act)

    def simplify_text_exit(self, cmd, exp):
        act = comm_func.send_shell_cmd(cmd)
        return ass_res.assert_text_exit(exp, act)

    def simplify_text_not_exit(self, cmd, exp):
        act = comm_func.send_shell_cmd(cmd)
        return ass_res.assert_text_not_exit(exp, act)

    def simplify_text_exit_sub(self, cmd, exp):
        act = comm_func.send_sub_pro_cmd(cmd)
        return ass_res.assert_text_exit(exp, act)

    def simplify_no_return(self, cmd):
        act = comm_func.send_shell_cmd(cmd)
        # print(act)
        return ass_res.assert_no_return(act)

    def file_is_exit(self, path):
        if not os.path.exists(path):
            e = "%s 不存在， 请检查！！！"
            log.error(e)
            assert False, e

    def str_replace(self, info):
        return info.replace("\n", "").replace(" ", "")

    def print_log(self, res):
        print(res)
        log.info(res)

    def print_err_log(self, res):
        print(res)
        log.error(res)

    def deal_volume_info(self, volume_info):
        res = re.findall(r'.*?volume is (.*?) in range.*?', volume_info)
        self.print_log(res[0])
        return int(res[0])

    # def print_my_text(self, cmd, res):
    #     my_text.write_text(cmd)
    #     my_text.write_text(res)
