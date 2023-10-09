from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtWidgets import QTextBrowser
import smtp, pop


class MainWindow:
    def __init__(self) -> None:
        self.ui = QUiLoader().load('uis/me.ui')
        self.icon = QIcon('img/Email.png')
        self.ui.setWindowIcon(self.icon)
        # 发件箱部分控件
        self.send = self.ui.lineEdit_3
        self.password = self.ui.lineEdit_4
        self.recv = self.ui.lineEdit
        self.theme = self.ui.lineEdit_2
        self.aiticle = self.ui.plainTextEdit
        self.warn = self.ui.label_8
        self.btnsend = self.ui.pushButton  # 发送按钮
        self.btnsend.clicked.connect(self.sendone)
        # 收件箱部分控件
        self.recacc = self.ui.lineEdit_5
        self.recpwd = self.ui.lineEdit_6
        self.recwarn = self.ui.label_9
        self.btnget = self.ui.pushButton_2  # 获取邮件按钮
        self.btnget.clicked.connect(self.getall)
        self.comboBox = self.ui.comboBox  # 邮件选择器
        self.textBrowser = self.ui.textBrowser  # 正文显示框
        self.textBrowser.setAcceptRichText(True)
        self.textBrowser.setOpenExternalLinks(True)
        self.comboBox.currentIndexChanged.connect(self.selectChange)
        self.btndel = self.ui.pushButton_4  # 邮件删除按钮
        self.btndel.clicked.connect(self.delemail)

    # 发送按钮按下后执行发送函数
    def sendone(self):
        send = self.send.text()
        pwd = self.password.text()
        recv = self.recv.text()
        theme = self.theme.text()
        art = self.aiticle.toPlainText()
        if send == '':
            self.warn.setText('发件人邮箱地址不能为空')
        elif pwd == '':
            self.warn.setText('发件人邮箱密码不能为空')
        elif recv == '':
            self.warn.setText('收件人邮箱地址不能为空')
        elif theme == '':
            self.warn.setText('主题不能为空')
        elif art == '':
            self.warn.setText('正文不能为空')
        else:
            self.warn.setText(' ')
            self.sendemail(send, pwd, recv, theme, art)

    def sendemail(self, send, pwd, recv, theme, art):
        smtp1 = smtp.STMP(send, pwd, recv, theme, art)
        check = smtp1.send()
        if check == 1:
            self.warn.setText('邮件发送成功')
        elif check == -1:
            self.warn.setText('账号或密码有误，请修改')
        else:
            self.warn.setText('未知错误')

    # 获取按钮按下后获取邮件
    def getall(self):
        acc = self.recacc.text()
        pwd = self.recpwd.text()
        if acc == '':
            self.recwarn.setText('邮箱地址不能为空')
        elif pwd == '':
            self.recwarn.setText('邮箱密码不能为空')
        else:
            self.getallemail(acc, pwd)

    def getallemail(self, acc, pwd):
        pop1 = pop.POP(acc, pwd)
        emailnum = pop1.getnum()
        if emailnum == -1:
            self.recwarn.setText('账号或密码有误，请修改')
            self.comboBox.clear()
            self.textBrowser.setText(' ')
        else:
            self.recwarn.setText('共找到' + str(emailnum) + '条邮件')
            self.comboBox.clear()
            self.comboBox.addItems([str(i) for i in range(1, emailnum + 1)])

    # 选择框改变后立即执行
    def selectChange(self):
        acc = self.recacc.text()
        pwd = self.recpwd.text()
        pop1 = pop.POP(acc, pwd)
        cnum = self.comboBox.currentText()
        if cnum != '':
            emailtext = pop1.recv(int(cnum))
            #self.textBrowser.setText(emailtext)
            self.textBrowser.setHtml(emailtext)

    # 删除邮件
    def delemail(self):
        acc = self.recacc.text()
        pwd = self.recpwd.text()
        cnum = self.comboBox.currentText()
        if acc == '':
            self.recwarn.setText('邮箱地址不能为空')
        elif pwd == '':
            self.recwarn.setText('邮箱密码不能为空')
        elif cnum == '':
            self.recwarn.setText('请先获取邮件')
        else:
            pop1 = pop.POP(acc, pwd)
            pop1.dele(int(cnum))
            self.recwarn.setText('第' + cnum + '封邮件已被删除，请重新获取邮件')
