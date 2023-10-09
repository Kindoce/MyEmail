from socket import *
from flanker import mime
import time
import re


class POP:
    def __init__(self, acc, pwd) -> None:
        self.mailserver = ("whu.edu.cn", 110)
        self.acc = 'user ' + acc + '\r\n'
        self.pwd = 'pass ' + pwd + '\r\n'

    # 获取邮件数目
    def getnum(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(self.mailserver)
        user = self.acc.encode()
        pwd = self.pwd.encode()
        clientSocket.send(user)
        clientSocket.send(pwd)
        time.sleep(1)
        recv = clientSocket.recv(1024)
        if '-ERR Unable to log on' in recv.decode():
            clientSocket.close()
            return -1
        else:
            num = re.findall(r'(\d*) message', recv.decode())
            clientSocket.close()
            return int(num[0])

    # 接收指定邮件
    def recv(self, i):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(self.mailserver)
        user = self.acc.encode()
        pwd = self.pwd.encode()
        clientSocket.send(user)
        clientSocket.send(pwd)
        time.sleep(1)
        recv1 = clientSocket.recv(1024)
        clientSocket.send(('retr ' + str(i) + '\r\n').encode())
        time.sleep(1)
        recv1 = clientSocket.recv(65536)
        try:
            recv1 = recv1.decode()
            clientSocket.close()
            recv = self.anal(recv1)
            return recv
        except:
            return 'Unable to decode'

    # 删除指定邮件
    def dele(self, i):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(self.mailserver)
        user = self.acc.encode()
        pwd = self.pwd.encode()
        clientSocket.send(user)
        clientSocket.send(pwd)

        clientSocket.send(('dele ' + str(i) + '\r\n').encode())
        time.sleep(1)
        clientSocket.send('QUIT\r\n'.encode())
        time.sleep(1)
        clientSocket.close()

    # 解析邮件
    def anal(self, recv):
        recv1 = recv[recv.index('\n') + 1:]
        rtstr = ''
        try:
            eml = mime.from_string(recv1)
            subject = eml.subject
            eml_header_from = eml.headers.get('From')
            eml_header_to = eml.headers.get('To')
            eml_header_cc = eml.headers.get('Cc')
            eml_time = eml.headers.get('Date')
            eml_body = self.contentEml(eml)
            if subject is not None:
                rtstr = '<p>主题：' + subject + '</p>'
            if eml_header_from is not None:
                rtstr += '<p>发件人：' + eml_header_from + '</p>'
            if eml_header_to is not None:
                rtstr += '<p>收件人：' + eml_header_to + '<p>'
            if eml_header_cc is not None:
                rtstr += '<p抄送人：' + eml_header_cc + '</p>'
            if eml_time is not None:
                rtstr += '<p>发送时间：' + eml_time + '</p>'
            if eml_body is not None:
                rtstr += '<p>正文：</p>' + eml_body
        except:
            rtstr = '<p>邮件解析异常 </p>' + recv1
        return rtstr

    # 获取邮件主体部分
    def contentEml(self, eml):
        if eml.content_type.is_singlepart():
            eml_body = eml.body
        else:
            eml_body = ''
            for part in eml.parts:
                if part.content_type.is_multipart():
                    eml_body = self.contentEml(part)
                else:
                    if part.content_type.main == 'text':
                        eml_body = part.body
        return eml_body
