from os.path import exists

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class commonMenu(QMenuBar):
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
        self.recentFilesMenu = QMenu('Recent Files', self)
        self.openSettingsFile()
        self.recentFilesMenu.triggered.connect(self.openRecentFiles)

        _save = QAction("Save", self)
        _save.setShortcut("Ctrl+S")
        _save.setStatusTip("Save the file")
        _save.triggered.connect(self.saveFile)
        _saveAs = QAction("Save As", self)
        _saveAs.setShortcut("Ctrl+Shift+S")
        _saveAs.setStatusTip("Save the file as")
        _saveAs.triggered.connect(self.saveFileAs)
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
        self.fileMenu.addAction(_exit)

    def createEditMenu(self):
        """
        create the edit commonMenu with undo, redo, copy, paste, delete
        :return:
        """
        _undo = QAction("Undo", self)
        _undo.setShortcut("Ctrl+Z")
        _undo.setStatusTip("Undo the last action")
        _redo = QAction("Redo", self)
        _redo.setShortcut("Ctrl+Shift+Z")
        _redo.setStatusTip("Redo the last action")
        _copy = QAction("Copy", self)
        _copy.setShortcut("Ctrl+C")
        _copy.setStatusTip("Copy the selected item")
        _copy.triggered.connect(self.copy)
        _paste = QAction("Paste", self)
        _paste.setShortcut("Ctrl+V")
        _paste.setStatusTip("Paste the copied item")
        _paste.triggered.connect(self.paste)
        _delete = QAction("Delete", self)
        _delete.setShortcut("Del")
        _delete.setStatusTip("Delete the selected item")
        _delete.triggered.connect(self.delete)
        _selectAll = QAction("Select All", self)
        _selectAll.setShortcut("Ctrl+A")
        _selectAll.setStatusTip("Select all the items")
        _selectAll.triggered.connect(self.selectAll)
        self.editMenu.addAction(_undo)
        self.editMenu.addAction(_redo)
        self.editMenu.addAction(_copy)
        self.editMenu.addAction(_paste)
        self.editMenu.addSeparator()
        self.editMenu.addAction(_delete)
        self.editMenu.addSeparator()
        self.editMenu.addAction(_selectAll)

    def createViewMenu(self):
        pass

    def createSettingsMenu(self):
        _loadSettings = QAction("Load Settings", self)
        _loadSettings.setStatusTip("Load settings")
        _loadSettings.triggered.connect(self.loadSettings)
        _saveSettings = QAction("Save Settings", self)
        _saveSettings.setStatusTip("Save settings")
        _saveSettings.triggered.connect(self.saveSettings)
        self.SettingsMenu.addAction(_loadSettings)
        self.SettingsMenu.addAction(_saveSettings)

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

    # ################################################
    #
    #       file commonMenu
    #
    #

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
            if len(self.recentFiles) == 0:
                self.recentFilesMenu.addAction("No recent files")
            else:
                for file in self.recentFiles:
                    self.recentFilesMenu.addAction(file)
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

        if exists("recentFiles.ini"):
            self.recentFiles.clear()
            with open("recentFiles.ini", "r") as file:
                self.recentFiles = file.readlines()
            if self.recentFiles:
                self.updateRecentFileMenu()
        else:
            self.recentFilesMenu.addAction("No recent files")
            self.saveSettingsFiles()

    def saveSettingsFiles(self):
        with open("recentFiles.ini", "w") as file:
            for _fileName in self.recentFiles:
                file.write(_fileName)

    def saveFile(self):
        self.mainWindows.onSaveProject()

    def saveFileAs(self):
        self.mainWindows.onSaveProjectAs()

    def exitApplication(self):
        self.saveSettings()
        self.saveRecentFiles()
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
        aboutDialog.setWindowTitle("About ArguePy")
        aboutDialog.setMinimumSize(600, 300)

        titleLabel = QLabel("Argue Py")
        titleLabel.setStyleSheet("font-size: 24px; font-weight: bold;")
        versionLabel = QLabel("Version 1.0")
        versionLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        authorLabel = QLabel("Author: Alessio Michelassi (2023)")
        authorLabel.setStyleSheet("font-size: 12px; font-weight: bold;")
        descriptionTxt = QTextEdit()
        descriptionTxt.setStyleSheet("font-size: 18px;")
        with open("ArguePy_CodeEditor/editorWidgetTool/commonMenu/AboutThisSoftware.txt",
                  "r", encoding="utf-8") as file:
            aboutTxt = file.read()
        descriptionTxt.setText(aboutTxt)
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
