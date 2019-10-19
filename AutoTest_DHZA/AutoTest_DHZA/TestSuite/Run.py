import datetime
import logging
import time
import unittest
from Common.Read_config import *


timeslmp=datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S')
resultulr=ReadConfig().get_testsrite('resultulr')
usercaseurl=ReadConfig().get_testsrite('usercaseurl')
usertestlisturl=ReadConfig().get_testsrite('usertestlisturl')
saveurl=resultulr+timeslmp+'-Report.html'
sendemail=ReadConfig().get_email('send_email_after_run')



def discover(caseurl):
    return unittest.defaultTestLoader.discover(caseurl)

def collect(caseurl):   # 由于使用discover() 组装的TestSuite是按文件夹目录多级嵌套的，我们把所有用例取出，放到一个无嵌套的TestSuite中，方便之后操作
    suite = unittest.TestSuite()

    def _collect(tests):   # 递归，如果下级元素还是TestSuite则继续往下找
        if isinstance(tests, unittest.TestSuite):
            if tests.countTestCases() != 0:
                for i in tests:
                    _collect(i)
        else:
            suite.addTest(tests)  # 如果下级元素是TestCase，则添加到TestSuite中

    _collect(discover(caseurl))
    return suite

def collect_only():   # 仅列出所用用例
    t0 = time.time()
    i = 0
    for case in makesuite_by_testlist(usertestlisturl):
        i += 1
        print("{}.{}".format(str(i), case.id()))
    print("----------------------------------------------------------------------")
    print("Collect {} tests is {:.3f}s".format(str(i),time.time()-t0))


def makesuite_by_testlist(usertestlisturl,caseurl):  # test_list_file配置在config/config.py中
    with open(usertestlisturl) as f:
        testlist = f.readlines()

    testlist = [i.strip() for i in testlist if not i.startswith("#")]   # 去掉每行结尾的"/n"和 #号开头的行
    suite = unittest.TestSuite()
    all_cases = collect(caseurl)  # 所有用例
    for case in testlist:   # 从所有用例中匹配用例方法名
        for acase in all_cases:
            if case == acase._testMethodName :
             suite.addTest(acase)
    return suite



# print(makesuite_by_testlist(usertestlisturl))