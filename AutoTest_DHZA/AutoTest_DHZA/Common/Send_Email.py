import smtplib
import logging
from Common import Log
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  # 混合MIME格式，支持上传附件
from email.header import Header  # 用于使用中文邮件主题
from Common import Read_config

re=Read_config.ReadConfig()
fromemail=re.get_email('mail_user')
toemail=re.get_email('receiver_email')
emailhsot=re.get_email('mail_host')
emailport=re.get_email('mail_port')
smtpuser=re.get_email('sender_email')
smtppwd=re.get_email('mail_pass')

def send_email(report_file):
    msg = MIMEMultipart()  # 混合MIME格式
    msg.attach(MIMEText(open(report_file, encoding='utf-8').read(), 'html', 'utf-8'))  # 添加html格式邮件正文（会丢失css格式）

    msg['From'] = fromemail  # 发件人
    msg['To'] = toemail  # 收件人
    msg['Subject'] = Header('接口测试报告', 'utf-8')  # 中文邮件主题，指定utf-8编码

    att1 = MIMEText(open(report_file, 'rb').read(), 'base64', 'utf-8')  # 二进制格式打开
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename="APITest.html"'  # filename为邮件中附件显示的名字
    msg.attach(att1)

    try:
        smtp = smtplib.SMTP_SSL(emailhsot,emailport)  # smtp服务器地址 使用SSL模式
        smtp.login(smtpuser, smtppwd)  # 用户名和密码
        smtp.sendmail(fromemail,toemail, msg.as_string()) # 发送给另一个邮箱
        logging.info("邮件发送完成！")
    except Exception as e:
        logging.error(str(e))
    finally:
        smtp.quit()