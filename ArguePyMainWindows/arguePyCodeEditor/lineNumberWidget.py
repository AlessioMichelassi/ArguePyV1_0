from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self.codeEditor = editor

    def sizeHint(self) -> QSize:
        return QSize()

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)