# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5 import uic
from podcluch import Connection
from main import Widget2

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from form1 import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.connect=Connection()
        self.glav=Widget2()
        self.login = 0
        self.parol = 0
        self.ui.vxod.clicked.connect(self.auth)
        self.ui.reg.clicked.connect(self.reg)

    def auth(self):
        self.login = self.ui.lineEdit_2.text()
        self.parol = self.ui.parol.text()
        cursor = self.connect.cur
        cursor.execute(f"SELECT login, parol  FROM users WHERE login = '{self.login}' AND parol = '{self.parol}'")
        outpu = cursor.fetchone()
        print(outpu)
        if outpu != None:
            QMessageBox.information(self, "Сообщение", "Вход совершен")
            self.destroy()
            self.glav.show()
        else:
            QMessageBox.information(self, "Сообщение", "Пользователь не зарегестрирован")

    def reg(self):
        self.login = self.ui.lineEdit_2.text()
        self.parol = self.ui.parol.text()
        if not self.login or not self.parol:
            QMessageBox.warning(self,"Предупреждение", "Поля логин и пароль не должны быть пустыми")
            return
        else:
            self.connect.cur.execute(f"INSERT INTO users (login, parol) VALUES ('{self.login}', '{self.parol}')")
            self.connect.con.commit()
            QMessageBox.information(self,'Сообщение', 'пользователь зарегистрирован')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    app.exec()
