import os
from os.path import exists

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QPushButton, QFileDialog, QApplication

from ArguePy_CodeEditor.editorWidgetTool.arguePyWidget import ArguePyWidget


class TabPressEvent(QEvent):
    def __init__(self):
        super().__init__(QEvent.User)


class ArgueTabWidget(QTabWidget):
    fileNames = {0: "Untitled.py"}
    fileNameCounter = 0

    def __init__(self, mainWindow, parent=None):
        super(ArgueTabWidget, self).__init__(parent)
        self.mainWindow = mainWindow
        # Add a button to add a new tab
        newTabButton = QPushButton("+")
        newTabButton.clicked.connect(self.addEmptyTab)
        self.setCornerWidget(newTabButton, Qt.TopRightCorner)

    def addEmptyTab(self):
        """
        ITA:
            Quando si aggiunge un tab vuoto, viene creato un nuovo widget per l'editor di codice e
            ovviamente viene creato un nuovo file con un nome univoco.
        ENG:
            When adding an empty tab, a new widget for the code editor is created and of course a new file
            is created with a unique name.
        :return:
        """
        editorWidget = ArguePyWidget(self)
        newTab = QWidget()
        self.fileNames[self.fileNameCounter] = f"Untitled{self.fileNameCounter}.py"
        newTab.setObjectName(self.fileNames[self.fileNameCounter])
        layout = QVBoxLayout(newTab)
        layout.addWidget(editorWidget)
        self.addTab(newTab, self.fileNames[self.fileNameCounter].replace(".py", ""))
        self.setCurrentWidget(newTab)
        try:
            self.checkIfFileExists()
            self.fileNameCounter += 1
        except Exception as e:
            a = e
            return False

    def addCodeTab(self, path):
        """
        ITA:
            Quando si aggiunge un tab con del codice, viene creato un nuovo widget per l'editor di codice e
            ovviamente viene creato un nuovo file con un nome univoco.
        ENG:
            When adding a tab with code, a new widget for the code editor is created and of course a new file
            is created with a unique name.
        :return:
        """
        editorWidget = ArguePyWidget(self)
        newTab = QWidget()
        name = os.path.basename(path)
        code = ""
        with open(path, "r") as file:
            code = file.read()
        editorWidget.setCode(code)
        self.fileNames[self.fileNameCounter] = name
        newTab.setObjectName(name)
        layout = QVBoxLayout(newTab)
        layout.addWidget(editorWidget)
        self.addTab(newTab, name.replace(".py", ""))
        self.setCurrentWidget(newTab)

    def getCode(self):
        return self.currentWidget().layout().itemAt(0).widget().getCode()

    def setCode(self, code):
        self.currentWidget().layout().itemAt(0).widget().setCode(code)

    def onRun(self):
        self.mainWindow.runCode(self.getCode())

    def checkIfFileExists(self):
        """
        ITA:
            Questo metodo controlla se il file esiste già, se esiste già, allora viene aggiunto un numero
            alla fine del nome del file.
        ENG:
            This method checks if the file already exists, if it already exists, then a number is added
            at the end of the file name.
        :return:
        """
        path = self.mainWindow.projectPath
        # il nome del file sarà quindi: path + self.fileNames[self.currentIndex()]
        absFileName = os.path.join(path, self.fileNames[self.currentIndex()])
        if not exists(absFileName):
            with open(absFileName, "w") as file:
                file.write(self.getCode())
        else:
            with open(absFileName, "r") as file:
                code = file.read()
            self.setCode(code)

    def showTab(self, index):
        """
        ITA:
            Questo metodo viene chiamato quando si clicca su un file nella vista a albero.
        ENG:
            This method is called when you click on a file in the tree view.
        :param index:
        :return:
        """
        if isinstance(index, int):
            if self.count() <= index:
                self.addEmptyTab()
                self.setCurrentIndex(index)
            self.setCurrentIndex(index)
        elif isinstance(index, str):
            path = index
            name = os.path.basename(path)
            isTabFound = False
            for i in range(self.count()):
                if self.tabText(i) == name.replace(".py", ""):
                    self.setCurrentIndex(i)
                    isTabFound = True
                    return
            if not isTabFound:
                self.addCodeTab(path)

    def saveFile(self):
        """
        ITA:
            Questo metodo salva il file corrente.
        ENG:
            This method saves the current file.
        :return:
        """
        path = self.mainWindow.projectPath
        absFileName = os.path.join(path, self.fileNames[self.currentIndex()])
        try:
            with open(absFileName, "w") as file:
                file.write(self.getCode())
            return True
        except Exception as e:
            print(f"Warning: there was a problem saving the file {absFileName}")
            print(e)
            return False

    def onTabPressed(self):
        """
        ITA:
            Questo metodo viene chiamato quando si preme il tasto tab nella finestra principale e
            serve che venga intercettato nel editorCode.
        ENG:
            This method is called when the tab key is pressed in the main window and
            serves to be intercepted in the editorCode.
        :param event:
        :return:
        """
        tabPressEvent = TabPressEvent()
        QApplication.sendEvent(self.currentWidget().layout().itemAt(0).widget(), tabPressEvent)

    def getCurrentFile(self):
        return self.fileNames[self.currentIndex()]