import os

from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ArguePyMainWindows.arguePyCodeEditor.arguePyWidget import ArguePyWidget


class CustomTabWidget(QTabWidget):
    tabLabel: QLabel
    tabCloseBtn: QPushButton

    def __init__(self, mainWindow, parent=None):
        super().__init__(parent)
        self.mainWindow = mainWindow
        self.setTabsClosable(True)
        self.initUI()
        self.initConnection()

    def initUI(self):
        pass

    def initConnection(self):
        self.tabCloseRequested.connect(self.closeTab)

    def closeTab(self, index):
        currentTab = self.currentWidget()
        if currentTab is not None:
            currentTab.saveFile()
        self.removeTab(index)

    def setName(self, name):
        self.tabLabel.setText(name)

    def getName(self):
        return self.tabLabel.text()

    def addTabCode(self, path):
        self.tabLabel = QLabel("Tab 1")
        self.tabCloseBtn = QPushButton("  \uf00d")
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(self.tabLabel)
        tabLayout.addWidget(self.tabCloseBtn)
        codeEditor, name = self.createEditor(path)
        tabLayout.addWidget(codeEditor)
        self.addTab(codeEditor, name.replace(".py", ""))

    def createEditor(self, path):
        codeEditor = ArguePyWidget(self)
        name = os.path.basename(path)
        self.setName(name)
        code = ""
        with open(path, "r") as file:
            code = file.read()
        codeEditor.setCode(code)
        codeEditor.fileName = os.path.abspath(path)
        return codeEditor, name

    def getCode(self):
        # se non ci sono tab aperti non ritorna codice
        if self.count() > 0:
            currentTab = self.currentWidget()
            if currentTab is not None:
                return self.mainWindow.fileExplorer.getSelectedFilePath()

    def saveFile(self):
        """
        ITA:
            Questo metodo salva il file corrente.
        ENG:
            This method saves the current file.
        :return:
        """
        currentTab = self.currentWidget()
        if currentTab is not None:
            codeEditor = self.currentWidget().findChild(ArguePyWidget)
            codeEditor.saveFile()
            return True

    def onRun(self):
        """
        ITA:
            Questo metodo esegue il file corrente.
        ENG:
            This method executes the current file.
        :return:
        """
        self.mainWindow.runCode(self.getCode())
