# click
import uiautomator2 as u2

d = u2.connect('192.168.5.231')

# click
d(text="Settings").click()

# long click
d(text="Settings").long_click()

# 等待元素的出现
d(text="Settings").wait(timeout=10.0)
d.implicitly_wait(10.0)