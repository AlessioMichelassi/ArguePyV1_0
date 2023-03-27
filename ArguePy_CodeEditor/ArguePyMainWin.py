import os
import subprocess
import sys
from os.path import exists
import platform

from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from ArguePy_CodeEditor.editorWidgetTool.ConsoleWidget.cosole import Console
from ArguePy_CodeEditor.editorWidgetTool.arguePyWidget import ArguePyWidget
from ArguePy_CodeEditor.editorWidgetTool.commonMenu.commonMenu import commonMenu
from ArguePy_CodeEditor.editorWidgetTool.fileExplorer.fileExplorer import FileExplorer
from ArguePy_CodeEditor.editorWidgetTool.tabWidget import ArgueTabWidget
from ArguePy_CodeEditor.editorWidgetTool.resource import resource_rc
from time import time


class ArguePy(QMainWindow):
    console: Console
    arguePyTab: ArguePyWidget
    fileExplorer: FileExplorer
    commonMenu = commonMenu
    process: QProcess
    projectPath = "ArguePy_CodeEditor/editorWidgetTool/tempFolder"
    isProjectFound = False
    isCompiled = False
    version = "1.0.0"

    def __init__(self):
        super().__init__()
        self.initUI()
        self.initMenu()
        self.statusBar().showMessage('Ready')
        self.initConnection()
        self.process = QProcess(self)

    #  ------------------ INIT MAIN MAINDOW ------------------ #

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('rguePy')
        self.setWindowIcon(QIcon(":/resource/icon.png"))
        self.checkVersion()

    def checkVersion(self):
        # se il programma è compilato
        if getattr(sys, 'frozen', False):
            if not exists(self.projectPath):
                projectPath = os.path.dirname(sys.executable)
                # create a tempFolder called tmpProject
                if not os.path.exists(projectPath + "/tmpProject"):
                    os.mkdir(projectPath + "/tmpProject")
                self.projectPath = projectPath + "/tmpProject"
                self.isProjectFound = False
            else:
                self.isProjectFound = True
        else:
            if not exists(self.projectPath):
                projectPath = os.path.dirname(os.path.abspath(__file__))
                # create a tempFolder called tmpProject
                if not os.path.exists(projectPath + "/tmpProject"):
                    os.mkdir(projectPath + "/tmpProject")
                self.projectPath = projectPath + "/tmpProject"
                self.isProjectFound = False
            else:
                self.isProjectFound = True
        self.initMain()

    def initMain(self):
        self.fileExplorer = FileExplorer(self)
        self.arguePyTab = ArgueTabWidget(self)
        self.console = Console(self)
        self.console.append("Welcome to ArguePy!")
        if self.isCompiled:
            self.console.append(f"compiled version{self.version}\nsystemFound: {os.name} - platform: {sys.platform}")
            self.console.append(
                f"{platform.system()} - {platform.release()} - {platform.version()} - {platform.machine()}")
        elif not self.isCompiled:
            self.console.append(f"not compiled test{self.version}\nsystemFound: {os.name} - platform: {sys.platform}")
            self.console.append(
                f"{platform.system()} - {platform.release()} - {platform.version()} - {platform.machine()}")
        if not self.isProjectFound:
            self.console.append("Project path not found, creating a new one...")
            self.console.append(f"Project path: {self.projectPath}")
            self.console.append("Project path created!")
            self.console.append("please remember to create a new project or open an existing one")
        dockWidget = QDockWidget("", self)
        dockWidget.setWidget(self.console)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dockWidget)
        dockFileExplorer = QDockWidget("", self)

        dockFileExplorer.setWidget(self.fileExplorer)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dockFileExplorer)
        self.setCentralWidget(self.arguePyTab)

    def initMenu(self):
        self.commonMenu = commonMenu(self)
        self.setMenuBar(self.commonMenu)

    def initConnection(self):
        self.fileExplorer.fileClickedSignal.connect(self.onExploreDoubleClickedSignal)
        self.fileExplorer.fileRenameSignal.connect(self.onFileRenameSignal)

    #  ------------------ RUN THE CODE FUNCTION ------------------ #

    def runCode(self, code):
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
        if self.onSaveProject():
            currentFile = self.fileExplorer.getCurrentFile()
            self.console.append(f"Run File: {currentFile}")
            absProjectPath = os.path.abspath(self.projectPath)
            self.tryRun('python', currentFile, absProjectPath, 10)
        else:
            self.console.appendError("Project not saved!")

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
            self.process.setWorkingDirectory(workingDir)
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

    def getCode(self):
        return self.arguePyTab.getCode()

    #  ------------------ EVENT FUNCTIONS ------------------ #

    def onExploreDoubleClickedSignal(self, path):
        self.arguePyTab.showTab(path)

    def closeEvent(self, event):
        if not self.onSaveProject():
            event.ignore()
            return
        if self.process:
            self.process.kill()
        self.console.close()
        self.arguePyTab.close()
        self.fileExplorer.close()
        self.commonMenu.close()
        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            self.arguePyTab.onTabPressed()
        else:
            super().keyPressEvent(event)

    # ------------------ PROJECT FUNCTIONS ------------------ #

    def onNewProject(self):
        pass

    def onOpenProject(self):
        self.onNewProject()
        dirFolder = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirFolder:
            self.projectPath = dirFolder
            self.fileExplorer.setRootPath(dirFolder)
            self.fileExplorer.setRootIndex(self.projectPath)
            self.fileExplorer.setExpanded(self.projectPath, True)
            self.fileExplorer.setSortingEnabled(True)
            self.fileExplorer.setDragDropMode(QAbstractItemView.InternalMove)
            self.fileExplorer.setAcceptDrops(True)
            self.fileExplorer.setDropIndicatorShown(True)
            self.fileExplorer.setDragEnabled(True)

    def openProjectFileName(self, fileName):
        self.onNewProject()
        self.projectPath = fileName
        self.fileExplorer.setRootPath(fileName)
        self.fileExplorer.setRootIndex(self.projectPath)
        self.fileExplorer.setExpanded(self.projectPath, True)
        self.fileExplorer.setSortingEnabled(True)
        self.fileExplorer.setDragDropMode(QAbstractItemView.InternalMove)
        self.fileExplorer.setAcceptDrops(True)
        self.fileExplorer.setDropIndicatorShown(True)
        self.fileExplorer.setDragEnabled(True)

    def onSaveProject(self):
        success = True
        for i in range(self.arguePyTab.count()):
            if not self.arguePyTab.saveFile():
                success = False
        return success

    def onSaveProjectAs(self):
        pass

    def onFileRenameSignal(self, oldPath, newPath):
        self.arguePyTab.renameFile(oldPath, newPath)
