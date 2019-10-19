import sys
sys.path.append("../..")  # 统一将包的搜索路径提升到项目根目录下
from Common.HTMLTestReportCN import HTMLTestRunner
from Common import Send_Email
from Common.Read_config import *
from Common.Log import *
from TestSuite.Run import *

timeslmp=datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S')
resultulr=ReadConfig().get_testsrite('resultulr')
saveurl=resultulr+timeslmp+'-Report.html'
usertestlisturl=ReadConfig().get_testsrite('usertestlisturl')
usercaseurl=ReadConfig().get_testsrite('usercaseurl')
suite=makesuite_by_testlist(usertestlisturl,usercaseurl)
sendemail=ReadConfig().get_email('send_email_after_run')



logging.info("================================== 测试开始 ==================================")
with open(saveurl, 'wb') as f:# 二进制写格式打开要生成的报告文件
    HTMLTestRunner(stream=f,title="WebApi Test",description="智能安全帽后台接口测试",tester="小胖").run(suite)
    f.close()

if sendemail == True:
    time.sleep(10)
    Send_Email.send_email(saveurl)
logging.info("================================== 测试结束 ==================================")
