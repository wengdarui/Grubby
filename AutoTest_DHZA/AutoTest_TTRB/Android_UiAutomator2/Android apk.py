#-*- coding:utf-8 -*-

import time

import uiautomator2 as u2

from Common import Read_config, Method

cf=Read_config.ReadConfig()

#Android
device_ip = cf.get_Android_OPPO('device_ip')
app = u2.connect(device_ip)

# app.press('menu')
try:
    app.app_start('com.uwillbe.ubzy')
    time.sleep(15)
    if (app(text=u"全新升级").exists):
        print('开始app引导流程')
        Method.Login_guide()
        print('开始登录账号')
        Method.Login()
        print('登录成功点击下一步')
        Method.Login_nextstep()
    else:
        print('开始登录账号')
        Method.Login()
        time.sleep(5)
        if(app(text=u"修改密码").exists):
            print('登录成功')
        else:
            print('登录成功点击下一步')
            Method.Login_nextstep()
except Exception as e:
    Method.Take_screenshot()
    print('异常信息:%s'%e)
# finally:
#     time.sleep(10)
#     app.app_stop('com.uwillbe.ubzy')








# with app.session("com.uwillbe.ubzy") as sess:
#     sess(resourceId="com.uwillbe.ubzy:id/largeLabel").click()
#     print(sess.running())
#     sess = app.session("com.uwillbe.ubzy")
#     sess(resourceId="com.uwillbe.ubzy:id/largeLabel").click()
#     time.sleep(2)
#     app.double_click(0.621, 0.977)
#     time.sleep(2)
#     Take_screenshot.Take_screenshot()
#     app.open_notification()