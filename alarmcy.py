#_*_coding:utf-8_*_
import os
import re
import urllib
import socket
import shutil
import datetime
import httplib
import urllib2
from email.mime.text import MIMEText
import smtplib  


errstr = ''
url = r'http://qikan.cqvip.com/zk1/search.aspx?key=U%3Dok'


mailto_list=["22216138@qq.com"]
mail_host="smtp.qq.com" 
mail_port = "465"  
mail_user="22216138"  
mail_pass="Yige198001"
mail_postfix="qq.com" 
 
def send_mail(to_list,sub,content):  
    ''''' 
    to_list:发给谁
    sub:主题 
    content:内容 
    send_mail("aaa@126.com","sub","content") 
    '''  
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">" 
    print 'from user',me 
    msg = MIMEText(content)  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)
    try:  
        s = smtplib.SMTP_SSL(mail_host,mail_port)  
        s.login(mail_user,mail_pass) 
        s.sendmail(me, to_list, msg.as_string())  
        s.close()  
        return True  
    except Exception, e:  
        print 'mail fail reason ',str(e)  
        return False  


if __name__ == '__main__':  
    try:
      response = urllib2.urlopen(url,timeout=5)
    except urllib2.URLError as e:
      if hasattr(e, 'code'):
        errstr = str(e.code)
      elif hasattr(e, 'reason'):
        errstr = str(e.reason)
    if errstr:
        print 'url error is ',errstr
        if send_mail(mailto_list,"there is an error",errstr):  
                print "mail send success"  
        else:  
                print "mail send fail"
        










