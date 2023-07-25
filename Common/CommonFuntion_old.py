from Conf.Config import *
import allure
import xlrd
# from DealWithExcelData import ExcelData as xlsData    这样导入会缺失参数， 后续深研究
import time
import pyautogui

# from Common import DealWithExcelData
from Common import ADBCommand
from Common import AssertResult

# path_dir = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
# xlsData = DealWithExcelData.ExcelData()
adbFun = ADBCommand.ADBManage()

outPut = AssertResult.AssertOutput()

log = Log.MyLog()
conf = Config()


class DealCmdData():

    def __init__(self, ver, chip):
        self.ver = ver
        self.chip = chip

    # 加载弹窗
    def getAlert(self, text):
        # text = "\n " * 10 + '请观看视频' + " " * 100 + "\n " * 10
        pyautogui.alert(text=text, title="提示")

    def openRootAuth(self):
        # 还需要增加细节检查已经进入root权限
        try:
            global andriodVer
            global chipPlan
            andriodVer = self.ver
            chipPlan = self.chip
            if andriodVer == 9 and chipPlan == 'QualcommChip':
                commandList = ['adb root', 'adb disable-verity', 'adb reboot', 'adb root', 'adb remount']
                for cmd in commandList:
                    self.sendSubproCommand(cmd)
            elif chipPlan == "Rockchip":
                commandList = ['adb root', 'adb remount']
                for cmd in commandList:
                    result = self.sendSubproCommand(cmd)
                    time.sleep(2)
            print("root权限开启成功")
        except Exception as e:
            print("无法开启root权限！！！，请检查版本！！！")
            raise e

    # 暂时不用该方法
    def deviceRoot(self, device):
        # 开root权限
        device.root()

    def inputData(self, cleanData):
        if len(cleanData) != 0:

            # 处理异常，int转换可能出错
            try:
                runTime = 0
                for runTime in cleanData:
                    if runTime['RunTimes']:
                        runTime = runTime + (runTime['RunTimes'])

                caseLen = len(cleanData) - 1 + runTime

            except Exception as e:
                assert False, e

            caseNameInfo = "***************" + cleanData[0]['Case Name'] + "***************"
            log.info(caseNameInfo)
            print(caseNameInfo)

            for dataDict in cleanData:
                # 步骤执行次数累加
                commandSplit = self.xlsDataSplit(dataDict['Command'])
                atucalResult = self.getAttrCmd(commandSplit[0], commandSplit[1], dataDict)
                # 写入log
                self.strLog(dataDict, commandSplit[1], atucalResult)

                # print(result)
                ExpectDataSplit = self.xlsDataSplit(dataDict['CheckData'])
                expectResult = "预期结果：    %s" % ExpectDataSplit[1]
                if "ReturnFile" in ExpectDataSplit[1]:
                    print("请在output.txt或者控制台查看结果")
                log.info(expectResult)
                print(expectResult)
                self.getAttrExp(ExpectDataSplit[0], ExpectDataSplit[1], atucalResult, dataDict, caseLen)
        else:
            e = "@@@@@@@用例数据为空， 请检查excel数据，该用例是否为空或者放错excel了！！！"
            print(e)
            assert False, e

    def strLog(self, dataDict, command, actualResult):
        logStr = dataDict['Step'] + "  " + dataDict['Remark'] + "  " + command
        print(logStr)
        info = log.info(logStr)
        resultStr = "实际结果：    %s" % actualResult
        print(resultStr)
        log.info(resultStr)

    def xlsDataSplit(self, cleanStr):
        orignalData = cleanStr.split("::")
        dataFunc = orignalData[0].strip()
        dataCmd = orignalData[1].strip()
        return [dataFunc, dataCmd]

    def getAttrCmd(self, SplitFunc, SplitData, dataDict):
        # 发送命令后需要等待的时间
        waitToTime = dataDict['TimeToWait(s)']
        if waitToTime:
            waitTime = int(waitToTime)
        else:
            waitTime = 0

        # 反射机制
        Func = getattr(DealCmdData, SplitFunc)
        result = Func(self, SplitData, waitTime)
        return result

    def getAttrExp(self, SplitFunc, SplitData, actualResult, dataDict, caseLen):
        # 反射机制
        Func = getattr(outPut, SplitFunc)
        Func(SplitData, actualResult, dataDict, caseLen)

    def sendShellCommand(self, commandCmd, waitTime=0):
        # 不同方案、安卓版本发送的不同指令在这里做判断
        cmd = self.cmdForChip(commandCmd)
        # print(cmd)
        if cmd:
            ActualResult = adbFun.adbShellCommand(cmd)
        else:
            ActualResult = adbFun.adbShellCommand(commandCmd)

        if "Permission denied" in ActualResult:
            self.openRootAuth()
            ActualResult1 = adbFun.adbShellCommand(commandCmd)
            return ActualResult1
        return ActualResult

    # 不同芯片方案指令发送的兼容
    def cmdForChip(self, cmd):
        if 'SystemType' in cmd:
            if self.chip == 'Rockchip':
                if 'User' in cmd:
                    command = 'getprop | grep product.build.type'
                    return command
                elif 'Selinux' in cmd:
                    command = 'getenforce'
                    return command
        elif 'RootTest' in cmd:
            if self.chip == 'Rockchip':
                if 'root' in cmd:
                    command = 'adb root'
                    return command
                elif 'remount' in cmd:
                    command = 'adb remount'
                    return command

    def manualListenSee(self, cmd, waitTime=0):
        if "testMusic.mp3" in cmd:
            self.fileExit(cmd, "testMusic.mp3")
            text = "\n " * 10 + '请听音乐！！！ \n 请注意声音由小变大再变小， 请听和看！' + " " * 100 + "\n " * 10
        else:
            text = "\n " * 10 + '请看视频！！！ \n 请注意声音由小变大再变小， 请听和看！' + " " * 100 + "\n " * 10
            self.fileExit(cmd, "")

        command = cmd
        self.getAlert(text)
        ActualResult = adbFun.adbShellCommand(command)
        # 调整音量， 音频启动后再静音
        self.adjustVolumn()
        if "Permission denied" in ActualResult:
            self.openRootAuth()
            ActualResult1 = adbFun.adbShellCommand(command)
            # 等待10秒钟听音乐
            time.sleep(3)
            return ActualResult1
        time.sleep(4)
        return ActualResult

    def adjustVolumn(self):
        adbFun.adbShellCommand("input keyevent 164")
        time.sleep(1)
        for i in range(4):
            adbFun.adbShellCommand("input keyevent 24")
            time.sleep(1)
        for i in range(4):
            adbFun.adbShellCommand("input keyevent 25")
            time.sleep(1)

    def fileExit(self, cmd, MetaFile):
        if 'testMusic' in cmd:
            file = path_dir + '\Media\\Music\\' + MetaFile
        else:
            file = path_dir + '\Media\\Video\\' + MetaFile
        if os.path.exists(file):
            # push文件到设备/sdcard/testMusic.mp3
            returnInfo = adbFun.subprocessCommand("adb push %s /sdcard/" % file)
            if "testMusic.mp3" in returnInfo:
                log.info("成功push文件到设备/sdcard/！！！")
            else:
                e = "@@@@@没有push文件到设备/sdcard/,请检查设备情况！！！"
                log.error(e)
                assert False, e
        else:
            err = "Media文件夹没有testMusic.mp3，请检查！！！"
            print("err")
            log.error(err)
            assert False, err

    def sendSubproCommand(self, commandCmd, waitTime):
        # 不同方案、安卓版本发送的不同指令在这里做判断
        cmd = self.cmdForChip(commandCmd)
        if cmd:
            ActualResult = adbFun.subprocessCommand(cmd)
        else:
            ActualResult = adbFun.subprocessCommand(commandCmd)

        if "Permission denied" in ActualResult:
            self.openRootAuth()
            ActualResult1 = adbFun.subprocessCommand(commandCmd)
            return ActualResult1
        return ActualResult


if __name__ == '__main__':
    adbFun.clientConnect()
    data = DealCmdData(11, 'Rockchip')
    data.manualListenSee(
        'am start -n com.android.music/com.android.music.MediaPlaybackActivity -d /sdcard/testMusic.mp3')
    # cleanData = xlsData.getCaseData('Base_Feature_Test1', 'BaseFeature.xls')
    # cmdData = data.inputData(cleanData)
