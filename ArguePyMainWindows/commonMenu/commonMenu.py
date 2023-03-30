import sys
import time
from os.path import exists

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ArguePyMainWindows.settingsIni.settings import Settings


class CommonMenu(QMenuBar):
    fileMenu: QMenu
    recentFilesMenu: QMenu
    editMenu: QMenu
    viewMenu: QMenu
    SettingsMenu: QMenu
    helpMenu: QMenu
    mainWindows: 'ArguePy'
    recentFiles: list

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainWindows = self.parent()
        self.settings = Settings("settings.ini")
        self.recentFiles = []
        self.createMenu()
        self.createFileMenu()
        self.createEditMenu()
        self.createViewMenu()
        self.createSettingsMenu()
        self.createHelpMenu()

    # ################################################
    #
    #       create commonMenu
    #
    #

    def createMenu(self):
        self.fileMenu = self.addMenu("&File")
        self.editMenu = self.addMenu("&Edit")
        self.viewMenu = self.addMenu("&View")
        self.SettingsMenu = self.addMenu("&Settings")
        self.helpMenu = self.addMenu("&Help")

    def createFileMenu(self):
        """
        create the file commonMenu with New, open, openRecent, save, saveAs, exit
        :return:
        """
        _new = QAction("New", self)
        _new.setShortcut("Ctrl+N")
        _new.setStatusTip("Create a new file")
        _new.triggered.connect(self.newFile)
        _open = QAction("Open", self)
        _open.setShortcut("Ctrl+O")
        _open.setStatusTip("Open a file")
        _open.triggered.connect(self.openFile)

        # recent files
        self.recentFilesMenu = QMenu(self)
        self.recentFilesMenu.setTitle("Open Recent")
        self.openSettingsFile()

        _save = QAction("Save", self)
        _save.setShortcut("Ctrl+S")
        _save.setStatusTip("Save the file")
        _save.triggered.connect(self.saveFile)
        _saveAs = QAction("Save As", self)
        _saveAs.setShortcut("Ctrl+Shift+S")
        _saveAs.setStatusTip("Save the file as")
        _saveAs.triggered.connect(self.saveFileAs)
        _closeProject = QAction("Close Project", self)
        _closeProject.setShortcut("Ctrl+Shift+W")
        _closeProject.setStatusTip("Close current project")
        _closeProject.triggered.connect(self.closeProject)
        _exit = QAction("Exit", self)
        _exit.setShortcut("Ctrl+Q")
        _exit.setStatusTip("Exit the application")
        _exit.triggered.connect(self.exitApplication)
        self.fileMenu.addAction(_new)
        self.fileMenu.addAction(_open)
        self.fileMenu.addSeparator()

        # recent files
        self.fileMenu.addMenu(self.recentFilesMenu)
        self.updateRecentFileMenu()

        self.fileMenu.addAction(_save)
        self.fileMenu.addAction(_saveAs)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(_closeProject)
        self.fileMenu.addSeparator()

        self.fileMenu.addAction(_exit)

    def createEditMenu(self):
        """
        create the edit commonMenu with undo, redo, copy, paste, delete
        :return:
        """
        _undo = self.createAction(
            "Undo", "Ctrl+Z", "Undo the last action"
        )
        _redo = self.createAction(
            "Redo", "Ctrl+Shift+Z", "Redo the last action"
        )
        _copy = self.createAction(
            "Copy", "Ctrl+C", "Copy the selected item"
        )
        _copy.triggered.connect(self.copy)
        _paste = self.createAction(
            "Paste", "Ctrl+V", "Paste the copied item"
        )
        _paste.triggered.connect(self.paste)
        _delete = self.createAction(
            "Delete", "Del", "Delete the selected item"
        )
        _delete.triggered.connect(self.delete)
        _selectAll = self.createAction(
            "Select All", "Ctrl+A", "Select all the items"
        )
        _selectAll.triggered.connect(self.selectAll)
        self.editMenu.addAction(_undo)
        self.editMenu.addAction(_redo)
        self.editMenu.addAction(_copy)
        self.editMenu.addAction(_paste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(_delete)
        self.editMenu.addSeparator()
        self.editMenu.addAction(_selectAll)

    def createAction(self, actionName, shortCut, statusTip):
        result = QAction(actionName, self)
        result.setShortcut(shortCut)
        result.setStatusTip(statusTip)
        return result

    def createViewMenu(self):
        pass

    def createSettingsMenu(self):
        pass

    def createHelpMenu(self):
        _help = QAction("Help", self)
        _help.setStatusTip("Help")
        _help.triggered.connect(self.help)
        _about = QAction("About", self)
        _about.setStatusTip("About")
        _about.triggered.connect(self.about)
        _aboutQt = QAction("About Qt", self)
        _aboutQt.setStatusTip("About Qt")
        _aboutQt.triggered.connect(self.aboutQt)
        self.helpMenu.addAction(_help)
        self.helpMenu.addAction(_about)
        self.helpMenu.addAction(_aboutQt)

    #       file commonMenu

    def newFile(self):
        self.mainWindows.onNewProject()

    def openFile(self):
        self.mainWindows.onOpenProject()

    def openRecentFiles(self, action):
        # sourcery skip: use-named-expression
        fileName = action.text()  # ottiene il nome del file dall'action
        self.mainWindows.onOpenProjectFile(fileName)
        if fileName not in self.recentFiles:
            self.recentFiles.append(fileName)
            self.saveSettingsFiles()
            self.openSettingsFile()

    def updateRecentFileMenu(self):
        if self.recentFiles:
            self.recentFilesMenu.clear()
            for file in self.recentFiles.split(","):
                self.recentFilesMenu.addAction(file)
        else:
            self.recentFilesMenu.clear()
            self.recentFilesMenu.addAction("No recent files")

        self.recentFilesMenu.addSeparator()
        self.recentFilesMenu.addAction("Clear recent files").triggered.connect(self.clearRecentFiles)

    def clearRecentFiles(self):
        self.recentFiles = []
        self.saveSettingsFiles()
        self.openSettingsFile()

    def openSettingsFile(self):
        """
            ITA: Apre la lista dei file recenti
            ENG: Open the recent files list
        :return:
        """
        self.settings.load()
        self.recentFiles = self.settings.get("recentFiles")
        if self.recentFiles:
            self.updateRecentFileMenu()
        else:
            self.recentFilesMenu.addAction("No recent files")
            self.saveSettingsFiles()

    def saveSettingsFiles(self):
        if self.recentFiles:
            if len(self.recentFiles) > 10:
                self.recentFiles.pop(0)
            self.settings.set("recentFiles", self.recentFiles)
            self.settings.save()

    def saveFile(self):
        self.mainWindows.onSaveProject()

    def saveFileAs(self):
        self.mainWindows.onSaveProjectAs()

    def closeProject(self):
        self.mainWindows.onCloseProject()

    def exitApplication(self):
        self.saveSettings()
        self.mainWindows.close()

    # ################################################
    #
    #       edit commonMenu
    #
    #

    def undo(self):
        pass

    def redo(self):
        pass

    def cut(self):
        pass

    def copy(self):
        pass

    def paste(self):
        pass

    def delete(self):
        pass

    def selectAll(self):
        pass

    def find(self):
        pass

    def replace(self):
        pass

    # ################################################
    #
    #       view commonMenu
    #
    #

    def zoomIn(self):
        pass

    def zoomOut(self):
        pass

    def zoomReset(self):
        pass

    def zoomFit(self):
        pass

    def zoomFitWidth(self):
        pass

    def zoomFitHeight(self):
        pass

    def zoomFitPage(self):
        pass

    def zoomFitPageWidth(self):
        pass

    def zoomFitPageHeight(self):
        pass

    def zoomFitSelection(self):
        pass

    def zoomFitSelectionWidth(self):
        pass

    def zoomFitSelectionHeight(self):
        pass

    def zoomFitSelectionPage(self):
        pass

    def zoomFitSelectionPageWidth(self):
        pass

    def zoomFitSelectionPageHeight(self):
        pass

    def zoomFitWindow(self):
        pass

    # ################################################
    #
    #       settings commonMenu
    #
    #

    def settings(self):
        pass

    def preferences(self):
        pass

    def loadSettings(self):
        self.mainWindows.loadSettings()

    def saveSettings(self):
        self.mainWindows.saveSettings()

    # ################################################
    #
    #       help commonMenu
    #
    #

    def help(self):
        pass

    def about(self):
        aboutDialog = QDialog(self)
        aboutDialog.setWindowTitle("bout ArguePy")
        aboutDialog.setMinimumSize(600, 500)

        titleLabel = QLabel("Argue Py")
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        versionLabel = QLabel("Version 1.0")
        versionLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        authorLabel = QLabel("Author: Alessio Michelassi (2023)")
        authorLabel.setStyleSheet("font-size: 12px; font-weight: bold;")
        descriptionTxt = QTextEdit()
        descriptionTxt.setStyleSheet("font-size: 18px;")
        about_file = QFile(':/resource/AboutThisSoftware.txt')
        about_file.open(QIODevice.ReadOnly | QIODevice.Text)
        about_txt = bytes(about_file.readAll()).decode('utf-8')
        about_file.close()
        descriptionTxt.setText(about_txt)
        descriptionTxt.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(titleLabel)
        layout.addWidget(versionLabel)
        layout.addWidget(descriptionTxt)
        aboutDialog.setLayout(layout)

        # Visualizzazione della finestra di dialogo
        aboutDialog.exec_()

    def aboutQt(self):
        """
            ITA: Mostra la finestra di About Qt
            ENG: Show the About Qt window
        :return:
        """
        QMessageBox.aboutQt(self.mainWindows, "About Qt")
