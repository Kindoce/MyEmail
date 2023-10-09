from PySide2.QtWidgets import QApplication
import myEmail
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = myEmail.MainWindow()
    MainWindow.ui.show()
    sys.exit(app.exec_())