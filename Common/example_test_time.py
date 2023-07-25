import datetime
import time
from ppadb.client import Client as AdbClient

client = AdbClient(host="127.0.0.1", port=5037)  # Default is "127.0.0.1" and 5037
dev = client.devices()[0]
cmd = "date +%Y\"-\"%m\"-\"%d\" \"%H\":\"%M\":\"%S\".\"%N"


# 北京时间精确到毫秒

print("当前网络时间：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
print("安卓系统时间：", dev.shell(cmd)[:-4])


time.sleep(1)
print("\n" + "间间隔1秒之后")
print("当前网络时间：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
print("安卓系统时间：", dev.shell(cmd)[:-4])

time.sleep(1)
print("\n" + "间间隔1秒之后")
print("当前网络时间：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
print("安卓系统时间：", dev.shell(cmd)[:-4])