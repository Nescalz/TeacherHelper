from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from sqlite3 import *
from random import randint
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from time import strftime
import json
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
connectdb.commit()
connectdb.close()


connectdb2 = connect("test.db")
cursor = connectdb2.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS test (
    id INTEGER,
    name TEXT NOT NULL,
    description text,
    teacher_id TEXT NOT NULL,
    student_id TEXT NOT NULL,
    test TEXT,
    otmetca INTEGER
            
)
''')
connectdb2.commit()
connectdb2.close()

connectdb3 = connect("student.db")
cursor = connectdb3.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    telegram_id TEXT UNIQUE NOT NULL,
    auth BOOLEAN,
    clas TEXT,
    history TEXT
)
''')
connectdb3.commit()
connectdb3.close()
#Пример заполниния тестов
# connectdb = connect("test.db")  # Подключение к базе данных
# cursor = connectdb.cursor()
# cursor.execute('''
#     INSERT INTO test (id, name, student_id, teacher_id, otmetca)
#     VALUES (?, ?, ?, ?, ?)
# ''', (1, "Тест для маленьких", 2, 91831411, 5))
# connectdb.commit()
# connectdb.close()

#Пример заполнения студентов
# connectdb = connect("student.db")  # Подключение к базе данных
# cursor = connectdb.cursor()
# cursor.execute('''
#     INSERT INTO students (name, id, teacher_id, telegram_id, auth, clas)
#     VALUES (?, ?, ?, ?, ?, ?)
# ''', ("Тайлер Дерден Алексанлрович", 2, 91831411, "@z", 1  , "1Б"))
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

# def otpravka_test(telegram_id, name):
#     connectdb = connect("test.db")
#     cursor = connectdb.cursor()
#     a = "0"
#     cursor.execute('SELECT * FROM test WHERE id = ?', (a,))
#     results = cursor.fetchall()
#     if results:
#         while results != False:
#             a += 1
#             cursor.execute('SELECT * FROM test WHERE id = ?', (a,))
#     else:
#         pass

#     cursor.execute(                                                    #
#                         'INSERT INTO test (id, name, telegram_id) VALUES (?, ?, ?)', # данный строки преднозначены для защиты от sql иньекции
#                         (a, name, telegram_id)            #
#                     )   
#     results = cursor.fetchall()
#     connectdb.commit()

app = QApplication([])

class MainW(QWidget):
    def __init__(self, user, id):
        super().__init__()
        self.name = user
        self.id = id
        self.initUI()

    def initUI(self):
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute('SELECT * FROM students WHERE auth = 1 AND teacher_id = ?', (self.id,))
        results = cursor.fetchall()
        if results: zvezda = "*"
        else: zvezda = ""

        self.setWindowTitle("Version 1")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon('image.png'))

        self.button1 = QPushButton(f"Заявки в класс{zvezda}")
        self.button2 = QPushButton("Задать тест")

        self.text1 = QLabel("Список учеников")
        self.text3 = QLabel(self.name)
        self.text4 = QLabel(f'ID: {self.id}')
        self.text5 = QLabel("Выберите класс")
        self.text6 = QLabel("для просмотра информации")

        self.classes = QListWidget()
        self.rabot = QListWidget()
        self.people = QListWidget()

        self.image_label = QLabel()
        self.image_label.setFixedSize(50, 50)
        self.load_avatar('avatar.svg')
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
        line2.addWidget(self.rabot)

        line23 = QHBoxLayout()
        line23.addStretch(1)
        line23.addWidget(self.text3)
        line23.addWidget(self.image_label)
        self.text3.setStyleSheet("color: black; text-decoration: bold;")
        self.text3.setFont(QFont("Times New Roman", 13))

        self.line4 = QVBoxLayout()
        self.line4.addLayout(line23)
        self.text4.setStyleSheet("color: blue; text-decoration: underline;")
        self.line4.addWidget(self.text4, alignment=Qt.AlignRight)
        self.line4.addStretch(1)
        self.create_pie_chart("default")
        self.line4.addWidget(self.canvas)
        self.line4.addWidget(self.button2)
              
        general_line.addLayout(line1)
        general_line.addLayout(line2)
        general_line.addLayout(self.line4)
        self.setLayout(general_line)
        self.button2.clicked.connect(self.testers)
        self.button1.clicked.connect(self.initUI2)
        self.classes.itemSelectionChanged.connect(self.check_selection)
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute('SELECT * FROM students WHERE auth = 0 AND teacher_id = ?', (self.id,))
        self.analogy_result = cursor.fetchall()
        self.student()
        self.clas()
    def testers(self):
        self.hide()
        self.make = testers(self.id, self.name)
        self.make.show()
    def load_avatar(self, image_path):
        pixmap = QPixmap(image_path)

        square_pixmap = pixmap.scaled(50, 50, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        mask = QBitmap(50, 50)
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, 50, 50)
        painter.end()
        
        square_pixmap.setMask(mask)
        self.image_label.setPixmap(square_pixmap)
    def check_selection(self):
        self.canvas.deleteLater()
        selected_items = self.classes.selectedItems()
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute('SELECT * FROM students WHERE auth = 0 AND clas = ?', (selected_items[0].text(),))
        self.analogy_result = cursor.fetchall() 
        self.student()
        self.create_pie_chart(selected_items[0].text())

    def clas(self):
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute('SELECT * FROM students WHERE auth = 0 AND teacher_id = ?', (self.id,))
        results = cursor.fetchall() 
        clases = []
        for result in results:
            a = result[5]
            if a not in clases:
                clases.append(a)
                self.classes.addItem(a)
        

    def student(self):
        self.people.clear()
        results = self.analogy_result

        
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
            self.full_name = full_name

            cursor_tests.execute('SELECT name, otmetca FROM test WHERE student_id = ?', (self.ids,))
            test_and_ochenky = {test[0]: test[1] for test in cursor_tests.fetchall()}

            klass = result[5] 
            self.add_student(itog, self.ids, telegram_user, test_and_ochenky, klass, full_name)

        connectdb.close()
        connectdb_tests.close()

    def create_pie_chart(self, xaas):
        if xaas == "default":

            figure = Figure()
            self.canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)
            self.canvas.setFixedSize(400, 400) 

            connectdb = connect("test.db")
            cursor = connectdb.cursor()
            cursor.execute('SELECT otmetca FROM test')
            results = cursor.fetchall()
            pyat = 0
            chetire = 0
            tri = 0
            dva = 0
            x = 0
            for result in results:
                x += 1
                a = result[0]
                if a == 5: pyat += 1
                elif a == 4: chetire += 1
                elif a == 3: tri += 1
                elif a == 2: dva += 1
            if pyat != 0:
                pyat = pyat/x
            if chetire != 0:
                chetire = chetire/x
            if tri != 0:
                tri = tri/x
            if dva != 0:
                dva = dva/x
            data = [pyat, chetire, tri, dva]
            if sum(data) == 0:
                data = [100]
                labels = ["Нет\nданных"]
            else:
                labels = ['5', '4', '3', '2']
            ax.pie(data, labels=labels, autopct='%1.1f%%')
            ax.set_title("Статистика класса")
        else:
            figure = Figure()
            self.canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)
            self.canvas.setFixedSize(400, 400) 
            pyat = 0
            chetire = 0
            tri = 0
            dva = 0
            x = 0
            connectdb = connect("test.db")
            cursor = connectdb.cursor()
            cursor.execute('SELECT otmetca, student_id FROM test')
            results = cursor.fetchall()
            connectdb2 = connect("student.db")
            cursor2 = connectdb2.cursor()
            cursor2.execute('SELECT id FROM students WHERE clas = ?', (xaas,))
            results2 = cursor2.fetchall()
            for result in results:
                for i in results2:
                    x1 = int(result[1])
                    x2 = int(i[0])
                    if x1 == x2:
                        x += 1
                        a = result[0]
                        if a == 5: pyat += 1
                        elif a == 4: chetire += 1
                        elif a == 3: tri += 1
                        elif a == 2: dva += 1
            if pyat != 0:
                pyat = pyat/x
            if chetire != 0:
                chetire = chetire/x
            if tri != 0:
                tri = tri/x
            if dva != 0:
                dva = dva/x
            data = [pyat, chetire, tri, dva]
            if sum(data) == 0:
                data = [100]
                labels = ["Нет\nданных"]
            else:
                labels = ['5', '4', '3', '2']
            ax.pie(data, labels=labels, autopct='%1.1f%%')
            ax.set_title("Статистика класса")
            self.line4.insertWidget(4, self.canvas)
    def add_student(self, name, ids, telegram_user, test_and_ochenky, klass, full_name):
        conte = QWidget()  
        conte_layout = QHBoxLayout(conte)
        conte_layout.setContentsMargins(5, 5, 5, 5)
        conte_layout.setSpacing(10)

        label = QLabel(name, conte)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        settings_button = QPushButton("Настройки", conte)
        settings_button.setFixedWidth(70)
        settings_button.clicked.connect(lambda: self.settings_clicked(name, ids, telegram_user, test_and_ochenky, klass, full_name))

        conte_layout.addWidget(label, stretch=1)
        conte_layout.addWidget(settings_button)

        item = QListWidgetItem(self.people)
        item.setSizeHint(conte.sizeHint())
        self.people.addItem(item)
        self.people.setItemWidget(item, conte)
    def settings_clicked(self, name, ids, telegram_user, test_and_ochenky, klass, full_name):
        self.sys_window = SYSWIN(self.people, full_name, ids, telegram_user, test_and_ochenky, klass)
        self.sys_window.setWindowModality(Qt.ApplicationModal)
        self.sys_window.show()
    def initUI2(self):
        self.notest_peole = QDialog(self)
        self.notest_peole.setWindowTitle("Добовление студентов")
        self.notest_peole.setWindowModality(Qt.ApplicationModal)  # Блокирует доступ к родительскому окну
        self.notest_peole.resize(600, 400)

        self.label = QListWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.label)
        self.notest_peole.setLayout(layout)
        self.amore_moregl()
        self.notest_peole.show()
    def amore_moregl(self):
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute('SELECT * FROM students WHERE auth = 1')
        results = cursor.fetchall() 
        connectdb.close()
        for result in results:
            name_amore = result[1]
            id_amore = result[0]
            self.idteacher_amore = result[2]
            self.tg_amore = result[3]
            self.clas_amore = result[5]
            self.amore_more(id_amore, name_amore)
    def amore_more(self, id_amore, name_amore):
        conte = QWidget()  
        conte_layout = QHBoxLayout(conte)
        conte_layout.setContentsMargins(5, 5, 5, 5)
        conte_layout.setSpacing(10)

        label = QLabel(name_amore, conte)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        settings_button = QPushButton("Инфо", conte)
        settings_button2 = QPushButton("Принять", conte)
        settings_button3 = QPushButton("Отказать", conte)
        settings_button.setFixedWidth(70)
        settings_button2.setFixedWidth(70)
        settings_button3.setFixedWidth(70)
        settings_button.clicked.connect(lambda: self.info(id_amore))
        settings_button2.clicked.connect(lambda: self.addStudent(id_amore))
        settings_button3.clicked.connect(lambda: self.exitStudent(id_amore))

        conte_layout.addWidget(label, stretch=1)
        conte_layout.addWidget(settings_button)
        conte_layout.addWidget(settings_button2)
        conte_layout.addWidget(settings_button3)

        item = QListWidgetItem(self.label)
        item.setSizeHint(conte.sizeHint())
        self.label.addItem(item)
        self.label.setItemWidget(item, conte)
    def info(self, id_amore):
        self.informations = QDialog(self)
        self.informations.setWindowTitle("Подробная информация")
        self.informations.setWindowModality(Qt.ApplicationModal)  # Блокирует доступ к родительскому окну
        self.informations.resize(342, 107)

        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute(f"SELECT * FROM students WHERE id = ?", (id_amore,))
        result = cursor.fetchall()
        self.label = QLabel(f"Имя: {result[0][1]}\nТелеграм: {result[0][3]}\nКласс: {result[0][5]}\nID: {result[0][0]}")
        layout = QVBoxLayout()

        layout.addWidget(self.label)
        self.informations.setLayout(layout)
        self.informations.show()
    def addStudent(self, id_amore):
        self.notest_peole.close()
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute(f'UPDATE students SET auth = 0 WHERE id = ?', (id_amore,))
        full_format = strftime("%d.%m.%Y %H:%M:%S - ")
        cursor.execute("SELECT history FROM students WHERE id = ?", (id_amore, ))
        res = cursor.fetchall()
        if res and res[0]:  # Если history уже содержит данные
            try:
                # Извлекаем строку из кортежа и парсим JSON
                history_list = json.loads(res[0])  # res[0] — это строка JSON
            except :
                # Если history не является валидным JSON, создаем новый список
                history_list = []
        else:  # Если history пустой
            history_list = []
        new_entry = {
            "date": strftime("%d.%m.%Y %H:%M:%S"),
            "event": "Пользователь принят в класс"
                }
        history_list.append(new_entry)
        cursor.execute(f"UPDATE students SET history = ? WHERE id = ?", (json.dumps(history_list, ensure_ascii=False), id_amore,))

        connectdb.commit()
        connectdb.close()
        self.initUI2()
    def exitStudent(self, id_amore):
        msg = QMessageBox()
        msg.setWindowModality(Qt.ApplicationModal)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Информация")
        msg.setText("Вы уверены, что хотите удалить заявку этого пользователя?")
        msg.setInformativeText("Удалять рекомендуется только в стучии несоответствий данных ученика к его реальной информации!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg.exec_()
        if response == QMessageBox.Yes:
            self.notest_peole.close()
            connectdb = connect("student.db")
            cursor = connectdb.cursor()
            cursor.execute(f"DELETE FROM students WHERE id = ?", (id_amore,))
            connectdb.commit()
            connectdb.close()
            self.initUI2()

class SYSWIN(QWidget):
    def __init__(self, people, name, ids, telegram_user, test_and_ochenky, klass):
        super().__init__()
        self.people = people
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
        self.colvo_ochenok = 0
        colvo_numochenok = 0
        self.dva = 0
        self.tri = 0
        self.chetire = 0
        self.paty = 0
        for k, v in self.test_and_ochenky.items(): 
            self.colvo_ochenok += 1
            colvo_numochenok += v
            if v == 2:
                self.dva += 1
            elif v == 3:
                self.tri += 1
            elif v == 4:
                self.chetire += 1
            elif v == 5:
                self.paty += 1
        if colvo_numochenok == 0:
            sred_result = 0
        else:
            sred_result = colvo_numochenok/self.colvo_ochenok
            sred_result = round(sred_result, 2)

        self.info_label = QLabel(f"{self.name}\nЛичный ID: {self.ids}\nКласс: {self.klass}\nТелеграм: {self.tg_user}")
        self.info_label.setAlignment(Qt.AlignLeft)
        self.info_label.setStyleSheet("font-size: 14px;")
        left_panel.addWidget(self.info_label)

        self.test_list = QListWidget()
        self.test_list.setStyleSheet("background-color: lightgray;")
        left_panel.addWidget(self.test_list)

        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel, 0, 1, 1, 1)

        self.stats_layout = QVBoxLayout()
        stats_label = QLabel("Статистика")
        stats_label.setAlignment(Qt.AlignCenter)
        self.stats_layout.addWidget(stats_label)

        canvas = self.create_pie_chart()
        self.stats_layout.addWidget(canvas)

        avg_score_label = QLabel(f"Средний балл: {sred_result}")
        avg_score_label.setAlignment(Qt.AlignCenter)
        self.stats_layout.addWidget(avg_score_label)
        right_panel.addLayout(self.stats_layout)

        self.action_layout = QHBoxLayout()
        self.exclude_button = QPushButton("Исключить ученика")
        self.exclude_button.clicked.connect(lambda: self.delete_student(self.ids))
        self.exclude_button.setStyleSheet("background-color: lightgray;")
        self.history_button = QPushButton("История")
        self.history_button.setStyleSheet("background-color: lightgray;")
        self.action_layout.addWidget(self.exclude_button)
        self.action_layout.addWidget(self.history_button)
        self.history_button.clicked.connect(lambda: self.history(self.ids))
        right_panel.addLayout(self.action_layout)
        for k, v in self.test_and_ochenky.items(): 
            self.addtests(k, v)
    def history(self, id):
        
        dial = QDialog()
        dial.setWindowTitle("История")
        dial.setWindowModality(Qt.ApplicationModal)
        dial.resize(645, 325)
        lists = QListWidget()
        label = QHBoxLayout()
        label.addWidget(lists)
        dial.setLayout(label)
        connectdb = connect("student.db")
        cursor = connectdb.cursor()
        cursor.execute("SELECT history FROM students WHERE id = ?", (id,))
        results = cursor.fetchall()
        for res in results:
            lists.addItem(res[0])
        dial.show()
        dial.exec_()
    def create_pie_chart(self):
        figure = Figure(figsize=(2, 2)) 
        canvas = FigureCanvas(figure)
        canvas.setFixedSize(400, 400) 
        ax = figure.add_subplot(111)
        if self.paty != 0:
            self.paty = self.paty / self.colvo_ochenok * 100
        else:
            self.paty = 0

        if self.tri != 0:
            self.tri = self.tri / self.colvo_ochenok * 100
        else:
            self.tri = 0

        if self.chetire != 0:   
            self.chetire = self.chetire / self.colvo_ochenok * 100
        else:
            self.chetire = 0

        if self.dva != 0:
            self.dva = self.dva / self.colvo_ochenok * 100
        else:
            self.dva = 0

        data = [self.paty, self.chetire, self.tri, self.dva]
        if sum(data) == 0: 
            data = [1]  
            labels = ['Нет данных']
        else:
            labels = ['5', '4', '3', '2']
        ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title("Оценки за тесты", fontsize=10)  

        return canvas
    def addtests(self, k, v):
        self.conte = QWidget()
        self.conte_layout = QHBoxLayout(self.conte)
        self.conte_layout.setContentsMargins(5, 5, 5, 5)
        self.conte_layout.setSpacing(10)

        label = QLabel(f"{k}        Оценка: {v}", self.conte)
        label.setWordWrap(True) 
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        settings_button = QPushButton("Просмотр", self.conte)
        settings_button.setFixedWidth(70) 


        settings_button.clicked.connect(lambda: self.prosmotr())


        self.conte_layout.addWidget(label, stretch=1)
        self.conte_layout.addWidget(settings_button)

        item = QListWidgetItem(self.test_list)
        item.setSizeHint(self.conte.sizeHint())
        self.test_list.addItem(item)
        self.test_list.setItemWidget(item, self.conte)
    def delete_student(self, ids):
        msg = QMessageBox()
        msg.setWindowModality(Qt.ApplicationModal)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Информация")
        msg.setText("Вы уверены, что хотите удалить пользователя?")
        msg.setInformativeText("После удаления ученик больше не будет состоять в вашем классе!")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        response = msg.exec_()
        if response == QMessageBox.Yes:
            connectdb = connect("student.db")
            cursor = connectdb.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (ids,))
            connectdb.commit()
            connectdb.close()
            self.close()
            msg = QMessageBox()
            msg.setWindowModality(Qt.ApplicationModal)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Информация")
            msg.setText("Ученик удален")
            msg.setInformativeText("Для показа статистики и корректного показа требуется перезапустить приложение!")
            msg.setStandardButtons(QMessageBox.Ok)
            response = msg.exec_()
        
    def prosmotr(self):
        pass
    

class testers(QWidget):
    def __init__(self, id, user):
        super().__init__()
        self.id = id
        self.user = user
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Меню тестов")
        self.resize(1000, 600)
        self.setWindowIcon(QIcon('image.png'))
        self.testline = QListWidget()
        self.classline = QListWidget()
        self.isk = QListWidget()

        but1 = QPushButton("Добавить тест")
        but2 = QPushButton("Запустить тест")
        nextbut = QPushButton("<< Назад")

        abel = QVBoxLayout()
        abel.addWidget(nextbut)
        abel.addWidget(self.testline)
        abel.addWidget(but1)
        abel2 = QVBoxLayout()
        abel2.addWidget(self.classline)
        abel3 = QVBoxLayout()
        abel3.addWidget(self.isk)
        abel3.addWidget(but2)
        abel_general = QHBoxLayout()
        abel_general.addLayout(abel)
        abel_general.addLayout(abel2)
        abel_general.addLayout(abel3)

        self.setLayout(abel_general)

        nextbut.clicked.connect(self.nextb)
        but1.clicked.connect(self.addTests)
        but2.clicked.connect(self.startTests)


    def nextb(self):
        self.hide()  
        self.close() 
        make = MainW(self.user, self.id)  
        make.show()
    def addTests(self):
        pass
    def startTests(self):
        pass
    def lineTests(self):
        conte = QWidget()  
        conte_layout = QHBoxLayout(conte)
        conte_layout.setContentsMargins(5, 5, 5, 5)
        conte_layout.setSpacing(10)

        label = QLabel(name, conte)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        settings_button = QPushButton("Настройки", conte)
        settings_button.setFixedWidth(70)
        settings_button.clicked.connect(lambda: self.settings_clicked(name, ids, telegram_user, test_and_ochenky, klass, full_name))

        conte_layout.addWidget(label, stretch=1)
        conte_layout.addWidget(settings_button)

        item = QListWidgetItem(self.people)
        item.setSizeHint(conte.sizeHint())
        self.people.addItem(item)
        self.people.setItemWidget(item, conte)
        


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
if __name__ == "__main__":
    main()
