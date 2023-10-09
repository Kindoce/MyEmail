from socket import *
import base64
import time


class STMP:
    def __init__(self, send, pwd, recv, theme, art) -> None:
        self.msg = '\r\n' + art  # 邮件正文
        self.endmsg = '\r\n.\r\n'  # 邮件结束标识符
        self.mailserver = ("whu.edu.cn", 25)  # 邮箱服务器
        self.sender = send  # 发送者地址
        self.pwd = pwd  # 发送者密码
        self.recv = recv  # 接收者地址
        self.theme = theme  # 主题

    # 发送邮件
    def send(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect(self.mailserver)
        # Send HELO command and print server response.
        heloCommand = 'HELO Alice\r\n'
        clientSocket.send(heloCommand.encode())
        # login
        acc = 'AUTH LOGIN\r\n'
        clientSocket.send(acc.encode())
        acc = base64.b64encode(self.sender.encode()) + '\r\n'.encode()
        clientSocket.send(acc)
        pwd = base64.b64encode(self.pwd.encode()) + '\r\n'.encode()
        clientSocket.send(pwd)

        time.sleep(1)
        reavx = clientSocket.recv(1024)
        if '535 Error: authentication failed' in reavx.decode():
            return -1

        fromCommand = 'MAIL FROM:<' + self.sender + '>\r\n'
        clientSocket.send(fromCommand.encode())

        toCommand = 'RCPT TO:<' + self.recv + '>\r\n'
        clientSocket.send(toCommand.encode())

        dataCommand = "DATA\r\n"
        clientSocket.send(dataCommand.encode())

        clientSocket.send(('FROM: ' + self.sender + '\r\n').encode())
        clientSocket.send(('TO: ' + self.recv + '\r\n').encode())
        clientSocket.send(('Subject: ' + self.theme + '\r\n').encode())

        clientSocket.send(self.msg.encode())
        clientSocket.send(self.endmsg.encode())

        quitCommand = "QUIT\r\n"
        clientSocket.send(quitCommand.encode())
        time.sleep(1)
        recvx = clientSocket.recv(1024)
        if '250 Mail OK queued as' in recvx.decode():
            return 1
        # Fill in end
        clientSocket.close()
        return 0