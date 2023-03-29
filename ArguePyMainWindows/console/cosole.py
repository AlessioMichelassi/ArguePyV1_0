from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


# crea una consolle simile a bash o cmd

class Console(QWidget):
    console: QTextEdit
    style = ""
    consoleFont = QFont("Bitstream Vera Sans", 12)
    backgroundColor = QColor(10, 10, 10)
    textColor = QColor(240, 240, 243)
    textColorError = QColor(240, 10, 10)
    textColorWarning = QColor(221, 94, 48) # dark orange #255, 255, 0
    textColorSuccess = QColor(70, 220, 120) # pastel dark green #
    textColorInfo = QColor(90, 50, 128) # dark purple #0, 0, 128
    textColorDebug = QColor(140, 140, 255)

    def __init__(self, mainWidget, parent=None):
        super().__init__(parent)
        self.mainWidget = mainWidget
        self.initUI()

    def initUI(self):
        self.initConsole()
        self.initStyle()
        self.setMinimumHeight(200)

    def initConsole(self):
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        # fa il wrap del testo
        # self.console.setAcceptRichText(False)
        layout = QVBoxLayout()
        layout.addWidget(self.console)
        self.setLayout(layout)

    def initStyle(self):
        textColor = f"rgb{self.textColor.red()}, {self.textColor.green()}, {self.textColor.blue()}"
        backGroundColor = f"rgb{self.backgroundColor.red()}, {self.backgroundColor.green()}, {self.backgroundColor.blue()}"

        self.style = f"""
            QTextEdit {{
                font-family: {self.consoleFont.family()};
                font-size: {self.consoleFont.pointSize()}pt;
                font-weight: 1;
                color: {textColor};
                background-color: {backGroundColor};
                border: 1px solid {textColor};
                border-radius: 5px;
            }}
        """
        self.console.setStyleSheet(self.style)

    def clear(self):
        self.console.clear()

    def append(self, text, color=None):
        isBold = False
        isItalic = False
        if color is None:
            color = self.textColor
        elif isinstance(color, str):
            if color == "error":
                color = self.textColorError
            elif color == "warning":
                color = self.textColorWarning
            elif color == "success":
                color = self.textColorSuccess
            elif color == "info":
                color = self.textColorInfo
            elif color == "debug":
                color = self.textColorDebug
            elif color == "bold":
                isBold = True
                color = self.textColor
            elif color == "italic":
                isItalic = True
                color = self.textColor
            else:
                color = self.textColor
        self.console.setTextColor(color)
        if isBold:
            self.console.setFontWeight(QFont.Weight.Bold)
        if isItalic:
            self.console.setFontItalic(True)
        self.console.append(text)
        self.console.setFontWeight(QFont.Weight.Normal)
        self.console.setFontItalic(False)

    def appendError(self, text):
        # colora il testo in rosso
        self.console.setTextColor(QColor(255, 0, 0))
        self.console.append(text)
