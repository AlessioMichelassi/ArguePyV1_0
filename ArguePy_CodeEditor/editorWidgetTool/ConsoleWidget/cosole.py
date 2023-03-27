from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# crea una consolle simile a bash o cmd

class Console(QWidget):
    console: QTextEdit
    style = ""
    consoleFont = QFont("Bitstream Vera Sans", 9)
    backgroundColor = QColor(10, 10, 10)
    textColor = QColor(240, 240, 243)
    textColorError = QColor(255, 0, 0)
    textColorWarning = QColor(255, 255, 0)
    textColorSuccess = QColor(0, 255, 0)
    textColorInfo = QColor(0, 255, 255)
    textColorDebug = QColor(0, 0, 255)

    def __init__(self, mainWidget, parent=None):
        super().__init__(parent)
        self.mainWidget = mainWidget
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Terminal Console')
        self.initConsole()
        self.initStyle()

    def initConsole(self):
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        # fa il wrap del testo
        self.console.setAcceptRichText(False)
        layout = QVBoxLayout()
        layout.addWidget(self.console)
        self.setLayout(layout)

    def initStyle(self):
        self.style = f"""
            QTextEdit {{
                font-family: {self.consoleFont.family()};
                font-size: {self.consoleFont.pointSize()}pt;
                font-weight: 0;
                color: rgb{self.textColor.getRgb()};
                background-color:  rgb{self.backgroundColor.getRgb()};
                border: 1px solid rgb{self.textColor.getRgb()};
                border-radius: 5px;
            }}
        """
        self.console.setStyleSheet(self.style)

    def clear(self):
        self.console.clear()

    def append(self, text):
        self.console.setTextColor(QColor(255, 255, 255))
        self.console.append(text)

    def appendError(self, text):
        # colora il testo in rosso
        self.console.setTextColor(QColor(255, 0, 0))
        self.console.append(text)
