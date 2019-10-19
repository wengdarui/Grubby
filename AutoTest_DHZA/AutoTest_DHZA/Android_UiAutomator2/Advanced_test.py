import uiautomator2 as u2
import time
import datetime
import logging
from Android_UiAutomator2 import Method
from Common import Read_config


cf=Read_config.ReadConfig()

#Android
device_ip = cf.get_Android_OPPO('device_ip')
app = u2.connect(device_ip)


tap_ID=Method.tap_ID
tap_txt=Method.tap_text

try:
    app.app_start('com.uwillbe.ubzy')
    time.sleep(10)
    tap_txt(u"升学")
    time.sleep(2)
    app.drag(0.891, 0.767,0.943, 0.300 )
    app.drag(0.891, 0.767,0.943, 0.300 )
    app(resourceId="com.uwillbe.ubzy:id/iv_bg", className="android.widget.ImageView", instance=2).click()
    tap_txt(u"大学专业选择测评")
    tap_txt(u"开始测试")
    time.sleep(1)
    for i in  range(219):
        tap_ID('com.uwillbe.ubzy:id/tvSelection',0.4)

except Exception as e:
    Method.Take_screenshot()
    print('异常信息:%s'%e)