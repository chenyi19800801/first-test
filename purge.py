#_*_coding:utf-8_*_
import os
import re
import urllib
import socket
import shutil
import datetime
import webbrowser
import urllib2
# 通过正则表达式找到svn日志中哪些行需要purge

url_purge = 'http://lib.cqvip.com'                 #配置需要purge的主站，可能需要修改

log_file = r'D:\python\test\svnlog\svnlog.txt'       #配置svn日志路径
pattern_purge = '^Modified.*(gif|jpg|jpeg|png|bmp|swf|htm|html|shtml|css|js|xml)$' #配置哪些文件需要purge
dns_ip1 = '113.31.19.41'                             #配置目标ip1
dns_ip2 = '113.31.19.40'                             #配置目标ip2
hosts_path = r'C:\Windows\system32\drivers\etc'      #配置hosts目录

# 通过正则表达式找到svn日志中哪些行需要purge
def is_purge(line):
    m = re.search(pattern_purge,line)
    if m is not None:
        return line
    else:
        return None 

# 修改hosts中的dns配置为指向一个特定ip
def change_dns(dns_ip):
    f = open(hosts_path+r'\hosts','r')
    lines = f.readlines()
    f.close()
    r =  range(len(lines))
    #把没有备份掉的dns映射备份掉，避免重复映射
    for i in r:
            if  re.search(url_purge[7:]+'$',lines[i]):
                if  not re.search('^#',lines[i]):
                    lines[i] = '#' + lines[i]
    f = open('C:\Windows\system32\drivers\etc\hosts','w')
    #f = open('D:\hosts','w')
    f.writelines(lines)
    f.write('\n'+dns_ip+' '+url_purge[7:])
    f.close


# 备份hosts文件
def bakup_hosts():
    shutil.copyfile(hosts_path+r'\hosts',hosts_path+r'\hosts_bakcy')


# 恢复hosts文件
def recover_hosts():
    os.remove(hosts_path+r'\hosts')
    os.rename(hosts_path+r'\hosts_bakcy',hosts_path+r'\hosts')


# 读取purge的url列表，依次访问，并记录关键的访问日志
def visit():
    f = open('reform.log','r')
    lines = f.readlines()
    r =  range(len(lines))
    result=socket.getaddrinfo(url_purge[7:],None)
    remoteIP = result[0][4][0]        # DNS分析出当前purge的实际IP，用于打印日志
    wf = open('purge.log','a')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i in r:
        wf.write('purge_url = ' +lines[i])
        wf.write('remoteIP = ' + remoteIP +'           '+now+ '\n')
        req = urllib2.Request(lines[i])
        req.add_header('User-agent', 'Mozilla 5.10')
        try:
            f_respose = urllib2.urlopen(req).read()
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                f_respose = 'there is a URLError. Error code:' + str(e.code)+ '\n'
            elif hasattr(e, 'reason'):
                f_respose = 'there is a URLError. Error Reason:' + str(e.reason)+ '\n'         
        #f_respose = urllib.urlopen(lines[i]).read()
        wf.write(f_respose)
        #webbrowser.open(lines[i])
    wf.close()

if __name__ == "__main__":
    # 读取svnlog.txt，存储为多行的数组
    f = open(log_file,'r')
    lines = f.readlines()
    f.close()
    r =  range(len(lines))

    for i in r:
            if not is_purge(lines[i]):
                lines[i] = ''

    # 写中间日志表reform.log，存储了purge的url列表
    wf = open('reform.log','w')
    for line in lines:
        if  not line == '':
            index = line.find(r'/trunk')
            line = url_purge+r'/purge'+line[index+6:] 
            wf.write(line)
    wf.close() 

    if os.path.isfile(r'purge.log'):
        os.remove('purge.log')

    bakup_hosts()
    change_dns(dns_ip1)
    visit()
    recover_hosts()

    bakup_hosts()
    change_dns(dns_ip2)
    visit()
    recover_hosts()

