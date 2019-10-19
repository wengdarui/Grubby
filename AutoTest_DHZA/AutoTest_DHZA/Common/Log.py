import logging
import datetime


timeslmp=datetime.datetime.now().strftime('%Y%m%d')
ulr="D:/Test/AutoTest_DHZA/AutoTest_DHZA/Result/"
saveurl=ulr+timeslmp+'-log.txt'

logging.basicConfig(level=logging.INFO,  # log level
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',  # log格式
                    datefmt='%Y-%m-%d %H:%M:%S',  # 日期格式
                    filename=saveurl, # 日志输出文件
                    filemode='a')  # 追加模式

if __name__ == '__main__':
    logging.info('小胖测试log')