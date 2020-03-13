# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 15:59
# @Author  : Skylor Tang
# @Email   : 
# @File    : redis_test.py
# @Software: PyCharm


import redis

r = redis.Redis(charset="utf-8", decode_responses=True)
r.set("name", "skylor")
r.expire("name", 2)  # 设置过期时间，秒为单位
import time
time.sleep(1)

print(r.get("name"))