from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from sqlite3 import *
from random import randint
import os

if not os.path.exists(os.path.join(os.path.join(os.path.expanduser("~"), "Documents"), "tests")):
    os.makedirs(os.path.join(os.path.join(os.path.expanduser("~"), "Documents"), "tests"))
else:
    pass

os.chdir(os.path.dirname(os.path.abspath(__file__)))
connectdb = connect("database.db")
cursor = connectdb.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.resize(756, 488)
        self.setWindowIcon(QIcon('image.png'))

        self.general_text = QLabel("Добро пожаловать!\nВойдите в систему")
        self.general_text.setFont(QFont('Regular', 24))

        self.login = QLineEdit(self)
        self.login.setPlaceholderText("Введите логин")
        self.login.setFixedSize(300, 20)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Введите пароль")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedSize(300, 20)

        self.button_login = QPushButton("Войти")
        self.button_login.setFont(QFont('Regular', 14))

        self.button_register = QPushButton("Регистрация")
        self.button_register.setFont(QFont('Regular', 14))

        self.general_layout = QVBoxLayout()
        self.general_layout.addWidget(self.general_text, alignment=Qt.AlignHCenter)
        self.general_layout.addWidget(self.login, alignment=Qt.AlignHCenter)
        self.general_layout.addWidget(self.password, alignment=Qt.AlignHCenter)

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.button_login, alignment=Qt.AlignHCenter)
        self.button_layout.addWidget(self.button_register, alignment=Qt.AlignHCenter)

        self.general_layout.addSpacing(200)
        self.general_layout.addLayout(self.button_layout)

        self.setLayout(self.general_layout)

        self.button_register.clicked.connect(self.start_reg)
        self.button_login.clicked.connect(self.login_star)

    def start_reg(self):
        self.general_text.setText("Если вы тут первый раз\nПройдите верификацию")
        self.setWindowTitle("Register")
        self.login.setPlaceholderText("Придумайте логин")
        self.password.setPlaceholderText("Придумайте пароль")
        self.button_login.setText("Вернуться назад")

        self.button_login.clicked.disconnect()
        self.button_login.clicked.connect(self.back_to_login)

        self.button_register.clicked.disconnect()
        self.button_register.clicked.connect(self.register)

    def back_to_login(self):
        self.general_text.setText("Добро пожаловать!\nВойдите в систему")
        self.setWindowTitle("Login")
        self.login.setPlaceholderText("Введите логин")
        self.password.setPlaceholderText("Введите пароль")
        self.button_login.setText("Войти")

        self.button_login.clicked.disconnect()
        self.button_login.clicked.connect(self.login_star)

        self.button_register.clicked.disconnect()
        self.button_register.clicked.connect(self.start_reg)

    def register(self):
        if self.login.text() and self.password.text():
            randomid = randint(10000000, 99999999) #89 999 999 возможных комбинаций id
            cursor.execute("SELECT username FROM users WHERE username = ?", (self.login.text(),))
            res = cursor.fetchone()
            if res:
                msgwarning = QMessageBox()
                msgwarning.setIcon(QMessageBox.Critical)
                msgwarning.setText("Ошибка!")
                msgwarning.setInformativeText('Такой логин уже существует, пожалуйста, выберете новый.')
                msgwarning.setWindowTitle("Error")
                msgwarning.setStandardButtons(QMessageBox.Ok) 
                msgwarning.exec_()
            else:
                cursor.execute("SELECT id FROM users WHERE id = ?", (randomid,))
                res = cursor.fetchone()
                if res:
                    while res:         
                        randomid = randint(10000000, 99999999)
                        cursor.execute("SELECT id FROM users WHERE id = ?", (randomid,))
                        res = cursor.fetchone()
                else:
                    cursor.execute(                                                    #
                        'INSERT INTO Users (id, username, password) VALUES (?, ?, ?)', # данный строки преднозначены для защиты от sql иньекции
                        (randomid, self.login.text(), self.password.text())            #
                    )                                                                  #
                    connectdb.commit()
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)  
                    msg.setWindowTitle("Информация")  
                    msg.setText("Вы зарегистрированы!")  
                    msg.setInformativeText("Нажмите ОК и войдите в систему.")  
                    msg.setStandardButtons(QMessageBox.Ok) 
                    msg.exec_()
                    self.login.setText("")
                    self.password.setText("")
                    self.back_to_login()
        else:
            msgwarning = QMessageBox()
            msgwarning.setIcon(QMessageBox.Critical)
            msgwarning.setText("Ошибка!")
            msgwarning.setInformativeText('Код ошибки №1. (Программа неможет обработать данные)')
            msgwarning.setWindowTitle("Error")
            msgwarning.exec_()
    def login_star(self):
        connectdb = connect("database.db")
        cursor = connectdb.cursor()
        cursor.execute('SELECT * FROM Users WHERE username == ? AND password == ?', (self.login.text(), self.password.text(),))
        results = cursor.fetchall()
        ad = bool(results)
        if ad:
            msgwarning = QMessageBox()
            msgwarning.setIcon(QMessageBox.Information)
            msgwarning.setText("Добрый день,")
            msgwarning.setFont(QFont("Times", 12, QFont.Bold))
            msgwarning.setInformativeText(f'{results[0][1]}')
            msgwarning.setWindowTitle("")
            msgwarning.setStandardButtons(QMessageBox.Ok) 
            msgwarning.exec_()

            self.general_windows()
        else:    
            msgwarning = QMessageBox()
            msgwarning.setIcon(QMessageBox.Critical)
            msgwarning.setText("Ошибка!")
            msgwarning.setInformativeText('Логин или пароль введены неверно!')
            msgwarning.setWindowTitle("Error")
            msgwarning.setStandardButtons(QMessageBox.Ok) 
            msgwarning.exec_()
    def general_windows(self):
        pass

       
def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
    connectdb.commit()
    connectdb.close()
