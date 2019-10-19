import time
import uiautomator2 as u2
from Common import Read_config, Method

cf=Read_config.ReadConfig()

#获取参数配置
device_ip = cf.get_Android_Huawei('device_ip')
account = cf.get_Android_Huawei('account')
account_pwd = cf.get_Android_Huawei('account_pwd')
app = u2.connect(device_ip)

tap_ID = Method.tap_ID
tap_txt = Method.tap_text


try:
    app.app_start('com.tencent.mm')
    time.sleep(10)
    if (app(text=u"发现").exists):
        app(resourceId="com.tencent.mm:id/ddm", text=u"发现").click()
        print(11)
        app(resourceId="com.tencent.mm:id/jq", className="android.widget.ImageView", instance=1).click()


except Exception as e:
    Method.Take_screenshot()
    print('异常信息:%s'%e)

finally:
    time.sleep(5)
    app.app_stop('com.tencent.mm')