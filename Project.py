from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from sqlite3 import *
from random import randint
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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

connectdb = connect("test.db")
cursor = connectdb.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS test (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    student_id TEXT UNIQUE NOT NULL,
    otmetca INTEGER NOT NULL
)
''')
connectdb.commit()
connectdb.close()

connectdb = connect("student.db")
cursor = connectdb.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    telegram_id TEXT UNIQUE NOT NULL,
    auth BOOLEAN,
    clas TEXT
)
''')
connectdb.commit()
connectdb.close()
#Пример заполниния тестов
# connectdb = connect("test.db")  # Подключение к базе данных
# cursor = connectdb.cursor()
# cursor.execute('''
#     INSERT INTO test (id, name, student_id, teacher_id, otmetca)
#     VALUES (?, ?, ?, ?, ?)
# ''', (1, "Тест для маленьких", 1, 91831411, 2))
# connectdb.commit()
# connectdb.close()

#Пример заполнения студентов
# connectdb = connect("student.db")  # Подключение к базе данных
# cursor = connectdb.cursor()
# cursor.execute('''
#     INSERT INTO students (name, id, teacher_id, telegram_id, auth, clas)
#     VALUES (?, ?, ?, ?, ?, ?)
# ''', ("Тайлер Дерден Алексанлрович", 1, 91831411, "@Nescalz", 0 **(1 - Требуется принять ученика учителем, 0 - Ученик уже находится под надзором учителя)** , "1Б"))
# connectdb.commit()
# connectdb.close()

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
#запросы - отправки
def zapros_test(name, telegram_id):
    connectdb = connect("test.db")
    cursor = connectdb.cursor()
    cursor.execute('SELECT * FROM test WHERE name == ? AND telegram_id == ?', (name, telegram_id,))
    results = cursor.fetchall()
    if results:
        print(results)

    else:
        print("пользователь не найден")
    connectdb.close()

def otpravka_test(telegram_id, name):
    connectdb = connect("test.db")
    cursor = connectdb.cursor()
    a = "0"
    cursor.execute('SELECT * FROM test WHERE id == ?'(a,))
    results = cursor.fetchall()
    if results:
        while results != False:
            a += 1
            cursor.execute('SELECT * FROM test WHERE id == ?'(a,))
    else:
        pass

    cursor.execute(                                                    #
                        'INSERT INTO test (id, name, telegram_id) VALUES (?, ?, ?)', # данный строки преднозначены для защиты от sql иньекции
                        (a, name, telegram_id)            #
                    )   
    results = cursor.fetchall()
    connectdb.commit()
    connectdb.close()

app = QApplication([])

class MainW(QWidget):
    def __init__(self, user, id):
        super().__init__()
        self.user = user
        self.id = id
        self.initUI()

    def initUI(self):
        #проверка на новый запрос от ученика ДЛЯ ПОКАЗА НОВОГО!!!
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute('SELECT * FROM students WHERE auth = 1 AND teacher_id = ?', (self.id,))
        results = cursor.fetchall()
        if results: zvezda = "*"
        else: zvezda = ""

        self.setWindowTitle("Version 1")
        self.resize(1244, 800)
        self.setWindowIcon(QIcon('image.png'))

        self.button1 = QPushButton(f"Заявки в класс{zvezda}")
        self.button2 = QPushButton("Задать тест")

        self.text1 = QLabel("Список учеников")
        self.text2 = QLabel("Статистика класса")
        self.text3 = QLabel(self.user)
        self.text4 = QLabel(f'ID: {self.id}')
        self.text5 = QLabel("Выберите класс")
        self.text6 = QLabel("для просмотра информации")

        self.classes = QListWidget()
        self.rabot = QListWidget()
        self.people = QListWidget()

        self.image_label = QLabel(self)
        self.pixmap = QPixmap("avatar.png")
        self.image_label.setPixmap(self.pixmap)

        # Линия с общей структурой
        general_line = QHBoxLayout()

        # Лайаут 1: Список учеников
        line1 = QVBoxLayout()
        self.text1.setFont(QFont("Times New Roman", 12))
        line1.addWidget(self.text1, alignment=Qt.AlignHCenter)
        line1.addWidget(self.people)
        line1.addWidget(self.button1)

        # Лайаут 2: Список классов и работ
        line2 = QVBoxLayout()
        self.text5.setFont(QFont("Times New Roman", 12))
        line2.addWidget(self.text5, alignment=Qt.AlignHCenter)
        self.text6.setFont(QFont("Times New Roman", 10))
        line2.addWidget(self.text6, alignment=Qt.AlignHCenter)
        line2.addWidget(self.classes)
        line2.addWidget(self.rabot)

        # Лайаут с изображением и именем пользователя
        line23 = QHBoxLayout()
        line23.addWidget(self.image_label)
        self.text3.setStyleSheet("color: black; text-decoration: bold;")
        self.text3.setFont(QFont("Times New Roman", 13))
        line23.addWidget(self.text3)

        # Лайаут 3: Статистика с диаграммой
        line3 = QVBoxLayout()
        line3.addWidget(self.text2, alignment=Qt.AlignHCenter)
        self.canvas = self.create_pie_chart()
        line3.addWidget(self.canvas)

        # Лайаут 4: Пользовательская информация
        line4 = QVBoxLayout()
        line4.addLayout(line23)
        self.text4.setStyleSheet("color: blue; text-decoration: underline;")
        line4.addWidget(self.text4, alignment=Qt.AlignHCenter)
        line4.addStretch(1)
        line4.addWidget(self.button2)
              
        # Компоновка всех частей
        general_line.addLayout(line1)
        general_line.addLayout(line2)
        general_line.addLayout(line3)
        general_line.addLayout(line4)
        self.setLayout(general_line)
        self.student()
    def student(self):
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute('SELECT * FROM students WHERE auth = 0 AND teacher_id = ?', (self.id,))
        results = cursor.fetchall() 

        
        connectdb_tests = connect("test.db")
        cursor_tests = connectdb_tests.cursor()

        for result in results:
            full_name = result[1]  
            parts = full_name.split()
            if len(parts) >= 2:  
                last_name = parts[0]
                initials = ''.join(f'{name[0]}.' for name in parts[1:])
                itog = f'{last_name} {initials}'
            else:
                itog = full_name
            self.ids = result[0]
            telegram_user = result[3]

            cursor_tests.execute('SELECT name, otmetca FROM test WHERE student_id = ?', (self.ids,))
            test_and_ochenky = {test[0]: test[1] for test in cursor_tests.fetchall()}

            klass = result[5] 
            self.add_student(itog, self.ids, telegram_user, test_and_ochenky, klass)

        connectdb.close()
        connectdb_tests.close()

    def create_pie_chart(self):
        """Создание круговой диаграммы для отображения статистики класса."""
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        #делать
        data = [40, 30, 20, 10]
        labels = ['5', '4', '3', '2']
        ax.pie(data, labels=labels, autopct='%1.1f%%')
        ax.set_title("Статистика класса")
        return canvas

    def add_student(self, name, ids, telegram_user, test_and_ochenky, klass):
        self.conte = QWidget()
        self.conte_layout = QHBoxLayout(self.conte)
        self.conte_layout.setContentsMargins(5, 5, 5, 5)
        self.conte_layout.setSpacing(10)


        label = QLabel(name, self.conte)
        label.setWordWrap(True) 
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        settings_button = QPushButton("Настройки", self.conte)
        settings_button.setFixedWidth(70) 


        settings_button.clicked.connect(lambda: self.settings_clicked(name, ids, telegram_user, test_and_ochenky, klass))


        self.conte_layout.addWidget(label, stretch=1)
        self.conte_layout.addWidget(settings_button)

        item = QListWidgetItem(self.people)
        item.setSizeHint(self.conte.sizeHint())
        self.people.addItem(item)
        self.people.setItemWidget(item, self.conte)

    def delete_student(self, ids):
        msg = QMessageBox()
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)  
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Информация")
        msg.setText("Вы уверены, что хотите удалить пользователя?")
        msg.setInformativeText("После удаления ученик больше не будет состоять в вашем классе!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No) 
        response = msg.exec_()
        if response == QMessageBox.Yes:
            for i in range(self.people.count()):
                item = self.people.item(i)
                widget = self.people.itemWidget(item)
                if widget == self.conte:
                    self.people.takeItem(i)
                    break
            connectdb = connect("student.db")
            cursor = connectdb.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (ids,))
            connectdb.commit()
            connectdb.close()
        elif response == QMessageBox.No:
            pass
    def settings_clicked(self, name, ids, telegram_user, test_and_ochenky, klass):   
        self.sys_window = SYSWIN(name, ids, telegram_user, test_and_ochenky, klass)  
        self.sys_window.setWindowFlags(Qt.WindowStaysOnTopHint)  
        self.sys_window.show()

class SYSWIN(QWidget):
    def __init__(self, name, ids, telegram_user, test_and_ochenky, klass):
        super().__init__()
        self.name = name
        self.ids = ids
        self.tg_user = telegram_user
        self.test_and_ochenky = test_and_ochenky
        self.klass = klass
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Static")
        self.resize(756, 488)
        self.setWindowIcon(QIcon('image.png'))

        # Main Layout
        main_layout = QGridLayout(self)

        # Left Panel: Student Info and Test Scores
        left_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, 0, 0, 1, 1)

        # Student Info
        self.info_label = QLabel(f"{self.name}\nЛичный ID: {self.ids}\nКласс: {self.klass}\nТелеграм: {self.tg_user}")
        self.info_label.setAlignment(Qt.AlignLeft)
        self.info_label.setStyleSheet("font-size: 14px;")
        left_panel.addWidget(self.info_label)

        # Test Scores List
        self.test_list = QListWidget()
        self.test_list.addItem("Тест №1  Оценка: 4")
        self.test_list.setStyleSheet("background-color: lightgray;")
        left_panel.addWidget(self.test_list)

        # Right Panel: Stats and Actions
        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel, 0, 1, 1, 1)

        # Stats
        self.stats_layout = QVBoxLayout()
        stats_label = QLabel("Статистика")
        stats_label.setAlignment(Qt.AlignCenter)
        self.stats_layout.addWidget(stats_label)

        # Pie Chart
        canvas = self.create_pie_chart()
        self.stats_layout.addWidget(canvas)

        # Average Score
        avg_score_label = QLabel("Средний балл: 4.8")
        avg_score_label.setAlignment(Qt.AlignCenter)
        self.stats_layout.addWidget(avg_score_label)
        right_panel.addLayout(self.stats_layout)

        # Action Buttons
        self.action_layout = QHBoxLayout()
        self.exclude_button = QPushButton("Исключить ученика")
        self.exclude_button.clicked.connect(lambda: MainW.delete_student(self, self.ids))
        self.exclude_button.setStyleSheet("background-color: lightgray;")
        self.history_button = QPushButton("История")
        self.history_button.setStyleSheet("background-color: lightgray;")
        self.action_layout.addWidget(self.exclude_button)
        self.action_layout.addWidget(self.history_button)
        right_panel.addLayout(self.action_layout)

    def create_pie_chart(self):
        # Создаём фигуру и канвас для диаграммы
        figure = Figure(figsize=(2, 2))  # Размер фигуры уменьшен (2x2 дюйма)
        canvas = FigureCanvas(figure)
        canvas.setFixedSize(400, 400)  # Устанавливаем фиксированный размер для канваса
        ax = figure.add_subplot(111)

        # Данные для диаграммы
        data = [40, 30, 20, 10]  # Проценты
        labels = ['5', '4', '3', '2']  # Оценки
        ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title("Оценки за тесты", fontsize=10)  # Уменьшаем размер шрифта заголовка

        return canvas

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
if __name__ == "__main__":
    main()
    connectdb.commit()
    connectdb.close()
