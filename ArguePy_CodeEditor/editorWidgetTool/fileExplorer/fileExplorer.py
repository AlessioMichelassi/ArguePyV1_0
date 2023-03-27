import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTreeView, QWidget, QVBoxLayout, QFileSystemModel, QTreeWidgetItem, QMenu, QAction, \
    QInputDialog, QMessageBox, QAbstractItemView

from ArguePy_CodeEditor.editorWidgetTool.fileExplorer.customIconProvider import CustomFileIconProvider
from ArguePy_CodeEditor.editorWidgetTool.fileExplorer.treeViewOverride import treeViewOverride


class FileExplorer(QWidget):
    model: QFileSystemModel
    tree: treeViewOverride
    fileClickedSignal = pyqtSignal(str, name="fileClicked")
    currentPath = ""
    currentFile = ""
    fileRenameSignal = pyqtSignal(str, str, name="fileRenamed")

    def __init__(self, mainWindows, parent=None):
        super().__init__(parent)
        self.mainWindows = mainWindows
        self.initUI()
        self.initConnection()

    def initUI(self):
        # Create the file system model
        self.initModel()

        # Create the tree view
        self.initTreeView()
        self.initDragAndDrop()
        # Aggiungi la vista a albero al layout
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def initModel(self):
        """
        ITA:
            Questo metodo inizializza il modello del file system.
        ENG:
            This method initializes the file system model.
        :return:
        """
        self.model = QFileSystemModel()
        self.model.setRootPath(self.mainWindows.projectPath)
        self.model.setNameFilterDisables(False)

        # this set icon for all file
        iconProvider = CustomFileIconProvider()
        # set the custom icon provider for the model
        self.model.setIconProvider(iconProvider)

    def initTreeView(self):
        """
        ITA:
            Questo metodo inizializza la vista a albero.
        ENG:
            This method initializes the tree view.
        :return:
        """
        self.tree = treeViewOverride()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.mainWindows.projectPath))
        root_index = self.model.index(self.mainWindows.projectPath)
        self.tree.setExpanded(root_index, True)
        self.tree.setColumnWidth(0, 250)

    def initDragAndDrop(self):
        """
        ITA:
            Questo metodo inizializza il drag and drop.
        ENG:
            This method initializes the drag and drop.
        :return:
        """
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        self.tree.setDefaultDropAction(Qt.DropAction.CopyAction)
        self.tree.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def initConnection(self):
        """
        ITA:
            Questo metodo inizializza le connessioni tra i segnali e i metodi.
        ENG:
            This method initializes the connections between the signals and the methods.
        :return:
        """
        self.tree.clicked.connect(self.onTreeviewClicked)
        self.tree.doubleClicked.connect(self.onTreeviewDoubleClicked)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def onTreeviewClicked(self, index: QModelIndex):
        """
        ITA:
            Questo metodo viene chiamato quando si fa click su un file nella vista a albero.
            Non fa praticamente niente a parte settare la path del file cliccato in modo che possa essere usata
            da altri metodi tipo per creare nuovi file o per creare directory
        ENG:
            This method is called when you click on a file in the tree view.
            It does not do anything except set the path of the clicked file so that it can be used
            by other methods like to create new files or to create directories
        """
        file_info = self.model.fileInfo(index)
        if not file_info.isFile() or not file_info.isReadable():
            # Il file non può essere letto o non è un file regolare, non fare nulla
            return
        file_path = self.model.filePath(index)
        self.currentFile = file_path
        diPath = os.path.dirname(file_path)
        self.currentPath = diPath

    def onTreeviewDoubleClicked(self, index: QModelIndex):
        """
        ITA:
            Questo metodo viene chiamato quando si fa doppio click su un file nella vista a albero.
        ENG:
            This method is called when you double click on a file in the tree view.
        """
        file_info = self.model.fileInfo(index)
        if not file_info.isFile() or not file_info.isReadable():
            # Il file non può essere letto o non è un file regolare, non fare nulla
            return
        file_path = self.model.filePath(index)
        try:
            with open(file_path, "r") as file:
                content = file.read()
        except UnicodeDecodeError:
            # Il file non è in formato testo, non fare nulla
            return

        self.fileClickedSignal.emit(file_path)

    def showContextMenu(self, pos):
        """
        ITA:
            Questo metodo mostra il menu contestuale.
        ENG:
            This method shows the context menu.
        :param pos:
        :return:
        """
        contextMenu = QMenu(self)
        newFileAction = QAction("new file")
        newDirAction = QAction("new directory")
        copyFileAction = QAction("copy")
        pasteFileAction = QAction("paste")
        renameFileAction = QAction("rename")
        deleteFileAction = QAction("delete")

        contextMenu.addAction(newFileAction)
        contextMenu.addAction(newDirAction)
        contextMenu.addSeparator()
        contextMenu.addAction(copyFileAction)
        contextMenu.addAction(pasteFileAction)
        contextMenu.addSeparator()
        contextMenu.addAction(renameFileAction)
        contextMenu.addSeparator()
        contextMenu.addAction(deleteFileAction)
        action = contextMenu.exec_(self.mapToGlobal(pos))

        if action == newFileAction:
            self.onFileNew()
        elif action == newDirAction:
            self.onDirNew()
        elif action == copyFileAction:
            self.onFileCopy()
        elif action == pasteFileAction:
            self.onFilePaste()
        elif action == renameFileAction:
            self.onFileRename()
        elif action == deleteFileAction:
            self.onFileDelete()

    def getCurrentFile(self):
        """
        ITA:
            Questo metodo ritorna il file corrente.
        ENG:
            This method returns the current file.
        :return:
        """
        return self.currentFile

    def onFileNew(self):
        """
        ITA:
            Crea un nuovo file e lo mette nella posizione selezionata nella vista a albero.
        ENG:
            Create a new file and put it in the selected position in the tree view.
        :return:
        """
        nameDialog = QInputDialog()
        nameDialog.setInputMode(QInputDialog.InputMode.TextInput)
        nameDialog.setLabelText("File name:")
        nameDialog.setWindowTitle("New file")
        nameDialog.exec_()
        if nameDialog.result() == QInputDialog.DialogCode.Accepted:
            # create a new file in the current directory
            index = self.tree.currentIndex()
            if not index.isValid():
                return
            fileName = nameDialog.textValue()
            newFilePath = os.path.join(self.currentPath, fileName)
            if not os.path.exists(newFilePath):
                with open(newFilePath, "w") as file:
                    file.write("")

    def onDirNew(self):
        nameDialog = QInputDialog()
        nameDialog.setInputMode(QInputDialog.InputMode.TextInput)
        nameDialog.setLabelText("Directory name:")
        nameDialog.setWindowTitle("New directory")
        nameDialog.exec_()
        if nameDialog.result() == QInputDialog.DialogCode.Accepted:
            # create a new file in the current directory
            index = self.tree.currentIndex()
            if not index.isValid():
                return
            filePath = self.model.filePath(index)
            dirName = nameDialog.textValue()
            newFilePath = os.path.join(self.currentPath, dirName)
            if not os.path.exists(newFilePath):
                os.mkdir(newFilePath)

    def onFileCopy(self):
        # copia il file selezionato in memoria
        index = self.model.index(self.tree.currentIndex().row(), 0, self.tree.currentIndex().parent())
        if not index.isValid():
            return
        filePath = self.model.filePath(index)
        self.mainWindows.clipboard = filePath

    def onFilePaste(self):
        pass

    def onFileRename(self):
        index = self.model.index(self.tree.currentIndex().row(), 0, self.tree.currentIndex().parent())
        if not index.isValid():
            return
        filePath = self.model.filePath(index)
        dirPath = os.path.dirname(filePath)
        oldName = os.path.basename(filePath)
        newName, ok = QInputDialog.getText(self, "Rename", "new Name:", text=oldName)
        if ok and newName:
            new_path = os.path.join(dirPath, newName)
            self.fileRenameSignal.emit(oldName, new_path)
            if os.path.exists(new_path):
                QMessageBox.warning(self, "Rinomina", f"Il file '{newName}' esiste già.")
                return
            os.rename(filePath, new_path)

    def onFileDelete(self):
        index = self.model.index(self.tree.currentIndex().row(), 0, self.tree.currentIndex().parent())
        if not index.isValid():
            return
        filePath = self.model.filePath(index)
        # se il path di una directory
        if os.path.isdir(filePath):
            self.deleteDir(filePath)
        else:
            self.deleteFile(filePath)

    def deleteDir(self, dirPath):
        for file in os.listdir(dirPath):
            filePath = os.path.join(dirPath, file)
            if os.path.isdir(filePath):
                self.deleteDir(filePath)
            else:
                self.deleteFile(filePath)
        if os.path.exists(dirPath):
            os.rmdir(dirPath)
        self.model.remove(self.tree.currentIndex())

    def deleteFile(self, filePath):
        os.remove(filePath)
        self.model.remove(self.tree.currentIndex())

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            # Handle the dropped file(s)
            # ...

        event.acceptProposedAction()