import os
import shutil
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ArguePyMainWindows.fileExplorer.treeViewOverride import treeViewOverride


class inputDialog(QDialog):
    lblText: QLabel
    txtQLine: QLineEdit

    def __init__(self, lblString, txtPlaceholder, position, parent=None):
        super().__init__(parent)
        self.lblName = lblString
        self.txtPlaceholder = txtPlaceholder
        self.initUI()
        self.initConnections()
        self.move(position)

    def initUI(self):
        self.lblText = QLabel(self.lblName)
        self.txtQLine = QLineEdit(self.txtPlaceholder)
        layout = QVBoxLayout()
        layout.addWidget(self.lblText)
        layout.addWidget(self.txtQLine)
        self.setLayout(layout)

    def initConnections(self):
        self.txtQLine.returnPressed.connect(self.returnPressed)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
            return None

    def returnPressed(self):
        self.accept()

    def getName(self):
        return self.txtQLine.text()

    def exec(self):
        super().exec()
        return self.txtQLine.text()


class FileExplorer(QWidget):
    model: QFileSystemModel
    tree: treeViewOverride
    projectPath: str = None

    def __init__(self, mainWindows, parent=None):
        super().__init__(parent)
        self.mainWindows = mainWindows
        self.initUI()

    def initUI(self):
        self.initModel()
        self.initTree()
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def initModel(self):
        """
        ITA:
            Questo metodo inizializza il modello del file system.
            setRootPath: imposta la root del file system
            setNameFilterDisables: abilita il filtro dei nomi dei file può tornare utile per mostrare solo
                                    i file con estensione .py o per tenere cartelle nascoste come env o .git
                                    __pyCache__
                                    model.setNameFilters(["*", "!__pycache__"])
                                    model.setNameFilterDisables(False)
            setReadOnly: abilita la scrittura del file system e permette di fare operazioni di spostamento e copia
                          senza questo non funziona il drag and drop dei file
        ENG:
            This method initializes the file system model.
            setRootPath: sets the root of the file system
            setNameFilterDisables: enables the file name filter can be useful to show only
                                    files with .py extension or to keep hidden folders like env or .git
                                    __pycache__
                                    model.setNameFilters(["*", "!__pycache__"])
                                    model.setNameFilterDisables(False)
            setReadOnly: enables the file system writing and allows to do operations of movement and copy
                            without this the drag and drop of files does not work
        :return:
        """
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        # read only false abilita la scrittura del file system e permette di fare operazioni di spostamento e copia
        self.model.setReadOnly(False)
        self.model.setNameFilters(["*", "!__pycache__"])
        self.model.setNameFilterDisables(True)

    def initTree(self):
        """
        ITA:
            Questo metodo inizializza la vista a albero.
            setModel: imposta il modello del file system
            setRootIndex: imposta la root dell'albero
            setColumnHidden: nasconde la colonna 1 e 2 che sono le colonne dei nomi dei file e delle dimensioni
            setSortingEnabled: abilita la possibilità di ordinare i file
            setAnimated: abilita l'animazione dei file
            setIndentation: imposta l'indentazione dei file
            setHeaderHidden: nasconde l'header
            setSelectionMode: imposta la modalità di selezione dei file
            setDragDropMode: imposta la modalità di drag and drop dei file
            setAlternatingRowColors: imposta l'alternanza dei colori delle righe
            setAcceptDrops: abilita il drag and drop
            setDropIndicatorShown: mostra l'indicatore del drag and drop
            initStyle: inizializza lo stile della vista a albero
        ENG:
            This method initializes the tree view.
            setModel: sets the file system model
            setRootIndex: sets the tree root
            setColumnHidden: hides column 1 and 2 which are the columns of the file names and sizes
            setSortingEnabled: enables the possibility of sorting the files
            setAnimated: enables the animation of the files
            setIndentation: sets the indentation of the files
            setHeaderHidden: hides the header
            setSelectionMode: sets the file selection mode
            setDragDropMode: sets the file drag and drop mode
            setAlternatingRowColors: sets the alternation of the row colors
            setAcceptDrops: enables drag and drop
            setDropIndicatorShown: shows the drag and drop indicator
            initStyle: initializes the style of the tree view
        :return:
        """
        self.tree = treeViewOverride()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath()))
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setIndentation(20)
        self.tree.setAnimated(True)

    def initConnections(self):
        """
        ITA:
            Questo metodo inizializza le connessioni tra i segnali e i metodi
        ENG:
            This method initializes the connections between the signals and the methods
        :return:
        """
        pass

    # ---------------------- FILE MANAGE ----------------------

    def getSelectedFile(self):
        """
        ITA:
            Questo metodo ritorna il file selezionato
        ENG:
            This method returns the selected file
        :return:
        """
        return self.tree.currentIndex().data()

    def getSelectedFilePath(self):
        """
        ITA:
            Questo metodo ritorna il path del file selezionato
        ENG:
            This method returns the path of the selected file
        :return:
        """
        return self.model.filePath(self.tree.currentIndex())

    def getSelectedFileDir(self):
        """
        ITA:
            Questo metodo ritorna la directory del file selezionato
        ENG:
            This method returns the directory of the selected file
        :return:
        """
        return self.model.filePath(self.tree.currentIndex())

    def getSelectedFileDirPath(self):
        """
        ITA:
            Questo metodo ritorna il path della directory del file selezionato
        ENG:
            This method returns the path of the directory of the selected file
        :return:
        """
        return self.model.filePath(self.tree.currentIndex())

    def renameItem(self, newName):
        """
        ITA:
            Questo metodo rinomina il file selezionato nell'explorer
        ENG:
            This method renames the selected file in the explorer
        :param newName: just insert the new name of the file
        :return: void
        """
        path = self.model.filePath(self.tree.currentIndex())
        if not path:
            return

        newPath = os.path.join(os.path.dirname(path), newName)
        os.rename(path, newPath)

    # ---------------------- PROJECT MANAGMENT ----------------------

    def setProject(self, projectDir):
        """
        ITA:
            Questo metodo imposta la directory del progetto
        ENG:
            This method sets the project directory
        :param projectDir:
        :return: void
        """
        self.tree.setRootIndex(self.model.index(projectDir))
        self.model.setRootPath(projectDir)
        self.projectPath = os.path.abspath(projectDir)

    def openProject(self):
        """
        ITA:
            Questo metodo apre un file dialog per selezionare un progetto
        ENG:
            This method opens a file dialog to select a project
        :return:
        """
        dirProject = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirProject:
            projectDir = self.model.index(dirProject)
            self.tree.setRootIndex(self.model.index(dirProject))
            self.model.setRootPath(dirProject)
            self.projectPath = os.path.abspath(dirProject)
            # se viene seleziona una cartella vuota
            # allora viene selezionata la root del progetto
            if not os.listdir(dirProject):
                # sceglie un nome per il progetto
                projectName, ok = QInputDialog.getText(self, "Choose a ProjectName", "name:", text="untitled",
                                                       flags=Qt.WindowTitleHint)
                if ok and projectName != "":
                    # crea una directory con il nome del progetto
                    os.mkdir(os.path.join(dirProject, projectName))
                    with open("arguePyResource/mainDefault.py", "r") as f:
                        data = f.read()
                    with open(os.path.join(dirProject, projectName, "main.py"), "w") as f:
                        f.write(data)
        else:
            self.mainWindows.close()

    def mouseDoubleClickEvent(self, event):
        event.ignore()
        self.mainWindows.tabWidget.addTabCode(self.getSelectedFilePath())

    # ---------------------- CONTEXT MENU ----------------------

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        newFileAction = contextMenu.addAction("Add File")
        newPyFileAction = contextMenu.addAction("Add Python File")
        newDirAction = contextMenu.addAction("Add Directory")
        renameAction = contextMenu.addAction("Rename")
        contextMenu.addSeparator()
        deleteAction = contextMenu.addAction("Delete")

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == newFileAction:
            self.addFile()
        elif action == newPyFileAction:
            self.addPyFile()
        elif action == newDirAction:
            self.addDir()
        elif action == renameAction:
            self.rename()
        elif action == deleteAction:
            self.delete()

    def addFile(self):
        """
        ITA:
            Questo metodo aggiunge un file vuoto nella directory selezionata
        ENG:
            This method adds an empty file in the selected directory
        :return:
        """
        filePath = self.getSelectedFileDirPath()
        position = self.mapToGlobal(self.rect().topLeft())
        dialog = inputDialog("File Name:", "untitled", position, parent=self)
        if dialog.exec():
            fileName = dialog.getName()
            with open(os.path.join(filePath, fileName), "w") as f:
                f.write("")

    def addPyFile(self):
        """
        ITA:
            Questo metodo aggiunge un file vuoto nella directory selezionata
        ENG:
            This method adds an empty file in the selected directory
        :return:
        """
        filePath = self.getSelectedFileDirPath()
        position = self.mapToGlobal(self.rect().topLeft())
        dialog = inputDialog("File Name:", "untitled", position, parent=self)
        if dialog.exec():
            fileName = dialog.getName()
            if not fileName.endswith(".py"):
                fileName += ".py"
            with open(os.path.join(filePath, fileName), "w") as f:
                f.write("")

    def addDir(self):
        """
        ITA:
            Questo metodo aggiunge una directory vuota nella directory selezionata
        ENG:
            This method adds an empty directory in the selected directory
        :return:
        """
        position = self.mapToGlobal(self.rect().topLeft())
        dialog = inputDialog("Directory Name:", "untitledDir", position, parent=self)
        if dialog.exec():
            dirName = dialog.getName()
            if dirName:
                # Crea la nuova directory
                ix = self.tree.currentIndex()
                path = self.model.filePath(ix)
                dirPath = os.path.join(path, dirName)
                if not os.path.exists(dirPath):
                    os.mkdir(dirPath)
        else:
            dialog.close()

    def rename(self):
        """
        ITA:
            Questo metodo rinomina il file selezionato
        ENG:
            This method renames the selected file
        :return:
        """
        position = self.mapToGlobal(self.rect().topLeft())
        oldName = self.model.fileName(self.tree.currentIndex())
        dialog = inputDialog("Rename:", oldName, position, parent=self)
        if dialog.exec():
            newName = dialog.getName()
            if newName:
                # Crea la nuova directory
                ix = self.tree.currentIndex()
                path = self.model.filePath(ix)
                newPath = os.path.join(os.path.dirname(path), newName)
                os.rename(path, newPath)

    def delete(self):
        """
        ITA:
            Questo metodo elimina il file selezionato
        ENG:
            This method deletes the selected file
        :return:
        """
        reply = QMessageBox.question(self, "Delete", "Are you sure?", QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            path = self.model.filePath(self.tree.currentIndex())
            if not path:
                return
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
