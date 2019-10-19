import requests
import time
import logging
from Common import Loging
logging.getLogger().setLevel(logging.INFO)


token=(Loging.login_3_3()[0])
txt='超不过喝喝酒哥回家看看家看看'

def upload():
    try:
        upload = requests.post(
          url='http://testapi.ubzyw.com/v1/rest/file/uploadOSS',
          data={},
          headers={'UB_UserAgent_deviceOS':'android','UB_UserAgent_appUserAuthToken':token},
          files={"Filedata":open("E:\\AutoTest_PY\\Datachecktest\\TestFile\\150947561hb4.jpg","rb")},
          )
        request=(upload.json())
        path =(request['data']['path'])
        logging.info('上传成功,地址:%s'%path)
    except Exception :
        logging.info('上传失败')
    else:
        try:
            save_upload = requests.post(
            url='http://testapi.ubzyw.com/v1/rest/advice/save',
            data={'typeId':'2','images':path,'content':txt},
            headers={'UB_UserAgent_deviceOS':'android','UB_UserAgent_appUserAuthToken':token}
              )
            request=(upload.json())
            print(request)
        except BaseException as error:
            logging.infologging.info('保存失败%s'%error )
            return path


def check_list():
    try:
        check_list = requests.post(
          url='http://testapi.ubzyw.com/v1/rest/advice/list',
          data={'prePage':'1','rows':1,'order':'desc'},
          headers={'UB_UserAgent_deviceOS':'android','UB_UserAgent_appUserAuthToken':token},
          )
        request=(check_list.json())
        list=(request.get('data'))
        content=(list['rows'][0]['content'])
        images=(list['rows'][0]['images'])
    except BaseException as error:
        logging.info('上传失败%s'%error )
    else:
        return content,images



if __name__ == '__main__':
    upload()
    check_list()