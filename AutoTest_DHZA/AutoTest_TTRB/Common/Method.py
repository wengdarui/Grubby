import uiautomator2 as u2
import os
import time
import datetime
from Common import Read_config



cf=Read_config.ReadConfig()
#获取配置参数
device_ip = cf.get_Android_Huawei('device_ip')
account = cf.get_Android_Huawei('account')
account_pwd = cf.get_Android_Huawei('account_pwd')
app = u2.connect(device_ip)
timeslmp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
screenshot_url = os.path.dirname(os.path.dirname( os.path.abspath(__file__) ))
saveurl= screenshot_url+'/Test_file/Screenshot/'+timeslmp+'.jpg'

def tap_ID(id): #点击事件id
    app(resourceId=id).click()

def tap_text(text): #点击事件text
    app(text=text).click()

def Take_screenshot(): #截屏
    try:
        app.screenshot(saveurl)
    except Exception as jietu:
        return ('未成功截图%s'%jietu)

def Login(): #登录账号（判断时候有开启通知消息弹窗）
    if (app(text=u"立即开启").exists):
        tap_ID("com.uwillbe.ubzy:id/closeIv")
        tap_text(u"我的")
        tap_ID("com.uwillbe.ubzy:id/tv_login_or_register")
        tap_ID("com.uwillbe.ubzy:id/tv_login")
        time.sleep(1)
        app(resourceId='com.uwillbe.ubzy:id/et_phone_number').set_text(account)
        app(resourceId='com.uwillbe.ubzy:id/et_password').set_text(account_pwd)
        time.sleep(1)
        tap_ID("com.uwillbe.ubzy:id/tv_login")
    else:
        tap_text(u"我的")
        tap_ID("com.uwillbe.ubzy:id/tv_login_or_register")
        tap_ID("com.uwillbe.ubzy:id/tv_login")
        time.sleep(1)
        app(resourceId='com.uwillbe.ubzy:id/et_phone_number').set_text(account)
        app(resourceId='com.uwillbe.ubzy:id/et_password').set_text(account_pwd)
        time.sleep(1)
        tap_ID("com.uwillbe.ubzy:id/tv_login")

def Login_guide(): #滑动初始化向导
    for i in  range(len('全新升级')):
        app.drag(0.99, 0.734,0.004, 0.734 )
    tap_ID("com.uwillbe.ubzy:id/tv_experience_immediately")
    time.sleep(10)
    if (app(text=u"立即开启").exists):
        tap_ID("com.uwillbe.ubzy:id/closeIv")
        return("进入app")
    else:
        return("进入app")


def Login_nextstep(): #第一次登录成功后,app内引导
    tap_ID("com.uwillbe.ubzy:id/tv_next_1")
    time.sleep(1)
    tap_ID("com.uwillbe.ubzy:id/tv_next_2")
    time.sleep(1)
    tap_ID("com.uwillbe.ubzy:id/tv_next_3")
    time.sleep(1)
    tap_ID("com.uwillbe.ubzy:id/tv_complete")
    app.implicitly_wait(10.0)
    tap_text(u"我的")
    tap_ID("com.uwillbe.ubzy:id/tv_mine_complete")
