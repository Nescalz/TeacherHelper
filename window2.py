from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class SYSWIN(QWidget):
    def __init__(self, name, ids):
        super().__init__()
        self.name = name
        self.id = ids
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
        self.info_label = QLabel(f"{self.name}\nЛичный ID: {self.id}\nКласс: 9A\nТелеграм: @Nescalz")
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
    window = SYSWIN("Иванов Иван Иванович", 12345678)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
