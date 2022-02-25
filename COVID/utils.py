# 公用函数

import hashlib
import time


def md5(m):
    return hashlib.md5(m.encode()).hexdigest()


def getNowDataTime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
