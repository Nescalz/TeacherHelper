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
        self.user = None
        self.id = None
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
                #проверка на возможный логин
                if res:
                    #Проверка на возможный id
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
            self.user = results[0][1]
            self.id = results[0][0]
            msgwarning = QMessageBox()
            msgwarning.setIcon(QMessageBox.Information)
            msgwarning.setText("Добрый день,")
            msgwarning.setFont(QFont("Times", 12, QFont.Bold))
            msgwarning.setInformativeText(f'{self.user}')
            msgwarning.setWindowTitle("")
            msgwarning.setStandardButtons(QMessageBox.Ok) 
            msgwarning.exec_()
            self.close()

            self.make = MainW(self.user, self.id)

            self.make.show()
        else:    
            msgwarning = QMessageBox()
            msgwarning.setIcon(QMessageBox.Critical)
            msgwarning.setText("Ошибка!")
            msgwarning.setInformativeText('Логин или пароль введены неверно!')
            msgwarning.setWindowTitle("Error")
            msgwarning.setStandardButtons(QMessageBox.Ok) 
            msgwarning.exec_()
        

class MainW(QWidget):
    def __init__(self, user, id):
        super().__init__()
        self.user = user
        self.id = id
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Version 1")
        self.resize(1115, 800)
        self.setWindowIcon(QIcon('image.png'))

        self.button1 = QPushButton("Заявки в класс")
        self.button2 = QPushButton("Задать тест")

        self.text1 = QLabel("Список учеников")
        self.text2 = QLabel("Статистика класса")
        self.text3 = QLabel(self.user)
        self.text4 = QLabel(f'ID: {self.id}')
        self.text5 = QLabel("Выбирите класс")
        self.text6 = QLabel("для просмотра информации")

        self.classes = QListWidget()
        self.classes2 = QListWidget()
        
        self.people = QListWidget()
        self.rabot = QListWidget()
        
        self.image_label = QLabel(self)
        self.pixmap = QPixmap("avatar.png")
        self.image_label.setPixmap(self.pixmap)
        

        general_line = QHBoxLayout()

        line1 = QVBoxLayout()
        self.text1.setFont(QFont("Times New Roman", 12))
        line1.addWidget(self.text1, alignment=Qt.AlignHCenter)
        line1.addWidget(self.people)
        line1.addWidget(self.button1)
        line2 = QVBoxLayout()
        self.text5.setFont(QFont("Times New Roman", 12))
        line2.addWidget(self.text5, alignment=Qt.AlignHCenter)
        self.text6.setFont(QFont("Times New Roman", 10))
        line2.addWidget(self.text6, alignment=Qt.AlignHCenter)
        line2.addWidget(self.classes)
        line2.addWidget(self.classes2)

        line23 = QHBoxLayout()
        line23.addWidget(self.image_label)
        line23.addWidget(self.text3)

        line3 = QVBoxLayout()
        line3.addWidget(self.rabot)
        line4 = QVBoxLayout()
        line4.addLayout(line23)

        self.text4.setStyleSheet("color: blue; text-decoration: underline;")
        line4.addWidget(self.text4, alignment=Qt.AlignHCenter)
        self.clipboard = QApplication.clipboard()
        
        self.text4.mousePressEvent = self.clipboard.setText(str(self.id))
        line4.addStretch(1)
        line4.addWidget(self.button2)
        general_line.addLayout(line1)
        general_line.addLayout(line2)
        general_line.addLayout(line3)
        general_line.addLayout(line4)
        self.setLayout(general_line)
       
def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
    connectdb.commit()
    connectdb.close()
