import os
import subprocess
import sys
import platform
from time import time

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ArguePyMainWindows.console.cosole import Console
from ArguePyMainWindows.fileExplorer.customTabWidget import CustomTabWidget
from ArguePyMainWindows.fileExplorer.fileExplorer import FileExplorer
from ArguePyMainWindows.settingsIni.settings import Settings
from ArguePyMainWindows.commonMenu.commonMenu import CommonMenu
from arguePyResource.resource_rc import *


class ArguePy(QMainWindow):
    settings: Settings
    menu: CommonMenu

    fileExplorer: FileExplorer
    tabWidget: CustomTabWidget
    console: Console

    # project Variables
    projectPath: str
    isCompiled = False
    version = "1.0.0"

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.initMainWindow()
        self.loadSettings()
        self.initUI()
        self.iniMenu()
        self.statusBar().showMessage("let's Argue")
        self.process = None
        self.welcomeMessage()

    def initUI(self):
        self.setWindowTitle('ArguePy')
        self.setWindowIcon(QIcon(":/resource/icon.png"))
        self.tabWidget = CustomTabWidget(self)
        self.setCentralWidget(self.tabWidget)

    def initMainWindow(self):
        self.fileExplorer = FileExplorer(self)
        leftDock = QDockWidget(self)
        leftDock.setWidget(self.fileExplorer)
        leftDock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, leftDock)
        bottomDock = QDockWidget(self)
        self.console = Console(self)
        bottomDock.setWidget(self.console)
        bottomDock.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable | QDockWidget.DockWidgetFeature.DockWidgetFloatable)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, bottomDock)

    def iniMenu(self):
        self.menu = CommonMenu(self)
        self.setMenuBar(self.menu)

    def welcomeMessage(self):
        self.console.append("Welcome to ArguePy!", "bold")
        if getattr(sys, 'frozen', False):
            self.console.append(f"compiled version{self.version}\n"
                                f"systemFound: {os.name} - platform: {sys.platform}", "info")
            self.console.append(
                f"{platform.system()} - {platform.release()} - {platform.version()} - {platform.machine()}")
        else:
            self.console.append(f"not compiled test {self.version}", "warning")
            self.console.append(f"systemFound: {os.name} - platform: {sys.platform}", "italic")
            self.console.append(
                f"{platform.system()} - {platform.release()} - {platform.version()} - {platform.machine()}", "info")

    # ------------------ SETTINGS ------------------

    def loadSettings(self):
        self.settings = Settings("settings.ini")
        self.settings.load()
        if self.settings.get("lastProject") is not None:
            self.fileExplorer.setProject(self.settings.get("lastProject"))
        else:
            self.fileExplorer.openProject()
        self.projectPath = self.settings.get("lastProject")

    def saveSettings(self):
        lastProject = self.settings.get("lastProject")
        if (
                lastProject is not None
                and lastProject != self.fileExplorer.projectPath
                or lastProject is None):
            self.settings.set("lastProject", self.fileExplorer.projectPath)
        self.settings.save()

    def closeEvent(self, event):
        self.saveSettings()
        self.close()

    # ------------------ RUN PROJECT ------------------
    def runCode(self, filePath):
        """
        ITA:
            Questo metodo esegue il codice scritto dall'utente utilizzando un QProcess, ovvero un processo
            che viene eseguito in un thread separato. Il processo viene eseguito con il comando python
            e il file temporaneo che viene creato con il codice scritto dall'utente.
        ENG:
            This method runs the code written by the user using a QProcess, that is a process
            that is executed in a separate thread. The process is executed with the python command
            and the temporary file that is created with the code written by the user.
        :return:
        """
        self.console.clear()

        self.console.append(f"file path: {filePath}")
        absProjectPath = os.path.abspath(filePath)
        # su linux è python3
        if os.name == "posix":
            self.tryRun('python3', filePath, absProjectPath, 10)
            #
        elif os.name == "nt":
            self.tryRun('python', filePath, absProjectPath, 10)
        else:
            self.console.appendError(f"OS not supported {os.name}")

    def onProcessOutput(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.console.append(output)

    def onProcessError(self):
        error = self.process.readAllStandardError().data().decode()
        self.console.appendError(error)

    def onProcessFinished(self):
        exit_code = self.process.exitCode()
        if exit_code == 0:
            self.console.append("Process finished successfully")
        else:
            self.console.appendError(f"Process finished with exit code {exit_code}")

    def tryRun(self, program, arguments, workingDir, timeout=10):
        """
        ITA:
            Esegue il codice scritto dall'utente utilizzando un QProcess, ovvero un processo
            che viene eseguito in un thread separato. Il processo viene eseguito con il comando python
            e il file temporaneo che viene creato con il codice scritto dall'utente.
        ENG:
            Runs the code written by the user using a QProcess, that is a process
            that is executed in a separate thread. The process is executed with the python command
            and the temporary file that is created with the code written by the user.
        :param program:
        :param arguments:
        :param workingDir:
        :param timeout:
        :return:
        """
        try:
            # Esegue il file Python utilizzando subprocess
            # Crea un processo QProcess per eseguire il codice
            self.process = QProcess(self)
            self.process.setProgram(program)
            self.process.setArguments([arguments])
            # to do: controllare se funziona anche con windows!
            _workingDir = os.path.dirname(os.path.abspath(workingDir))
            self.process.setWorkingDirectory(_workingDir)
            # Connette i segnali del processo per catturare l'output
            self.process.readyReadStandardOutput.connect(self.onProcessOutput)
            self.process.readyReadStandardError.connect(self.onProcessError)
            self.process.finished.connect(self.onProcessFinished)
            start_time = time()
            # Esegue il processo
            self.process.start()
            self.process.waitForFinished()
            end_time = time()
            elapsed_time = end_time - start_time
            # Aggiungi il tempo di esecuzione all'output
            self.console.append(f"Elapsed time: {elapsed_time:.2f} seconds")
        except subprocess.TimeoutExpired:
            self.console.append(f"subprocess.TimeoutExpired: {subprocess.TimeoutExpired}")

    # ------------------ PROJECT  MANAGMENT ------------------

    def onNewProject(self):
        self.tabWidget.closeAllTab()
        self.fileExplorer.openProject()

    def onOpenProject(self):
        self.tabWidget.closeAllTab()
        self.fileExplorer.openProject()

    def onSavedProject(self):
        self.tabWidget.saveAllFile()

    def onSavedAsProject(self):
        self.fileExplorer.saveAsProject()

    def onCloseProject(self):
        self.tabWidget.closeAllTab()
