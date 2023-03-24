from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# crea una consolle simile a bash o cmd

class Console(QWidget):
    console: QTextEdit

    def __init__(self, mainWidget, parent=None):
        super().__init__(parent)
        mainWidget = mainWidget
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Terminal Console')
        self.setFont(QFont("Consolas", 10))
        self.initConsole()

    def initConsole(self):
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        # fa il wrap del testo
        self.console.setAcceptRichText(False)
        layout = QVBoxLayout()
        layout.addWidget(self.console)
        self.setLayout(layout)

    def clear(self):
        self.console.clear()

    def append(self, text):
        self.console.setTextColor(QColor(255, 255, 255))
        self.console.append(text)

    def appendError(self, text):
        # colora il testo in rosso
        self.console.setTextColor(QColor(255, 0, 0))
        self.console.append(text)
