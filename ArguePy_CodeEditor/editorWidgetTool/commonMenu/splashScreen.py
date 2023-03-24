import os
import sys
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QSplashScreen, QProgressBar
from ArguePy_CodeEditor.editorWidgetTool.resource import resource_rc

class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        pixmap = QPixmap(":/resource/logo.png")
        self.setPixmap(pixmap)
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10, pixmap.height() - 20, pixmap.width() - 20, 10)
        self.progress.move(10,10)
        self.progress.setMaximum(40)

    def progressLoop(self):
        for i in range(40):
            time.sleep(0.1)
            self.progress.setValue(i)
            self.repaint() # Aggiorna l'interfaccia grafica durante il loop