import os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTreeView, QWidget, QVBoxLayout, QFileSystemModel, QTreeWidgetItem, QMenu, QAction, \
    QInputDialog, QMessageBox

from ArguePy_CodeEditor.editorWidgetTool.fileExplorer.customIconProvider import CustomFileIconProvider


class FileExplorer(QWidget):
    model: QFileSystemModel
    tree: QTreeView
    fileClickedSignal = pyqtSignal(str, name="fileClicked")

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
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.mainWindows.projectPath))
        root_index = self.model.index(self.mainWindows.projectPath)
        self.tree.setExpanded(root_index, True)
        self.tree.setColumnWidth(0, 250)

    def initConnection(self):
        """
        ITA:
            Questo metodo inizializza le connessioni tra i segnali e i metodi.
        ENG:
            This method initializes the connections between the signals and the methods.
        :return:
        """
        self.tree.clicked.connect(self.onTreeviewDoubleClicked)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

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

        copyFileAction = QAction("copy")
        pasteFileAction = QAction("paste")
        renameFileAction = QAction("rename")
        deleteFileAction = QAction("delete")

        contextMenu.addAction(copyFileAction)
        contextMenu.addAction(pasteFileAction)
        contextMenu.addSeparator()
        contextMenu.addAction(renameFileAction)
        contextMenu.addSeparator()
        contextMenu.addAction(deleteFileAction)
        action = contextMenu.exec_(self.tree.viewport().mapToGlobal(pos))

        if action == copyFileAction:
            print("copy")
        elif action == pasteFileAction:
            print("paste")
        elif action == renameFileAction:
            self.onFileRename()
        elif action == deleteFileAction:
            print("delete")

    def onFileCopy(self):
        print("copy")

    def onFilePaste(self):
        print("paste")

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
            if os.path.exists(new_path):
                QMessageBox.warning(self, "Rinomina", f"Il file '{newName}' esiste già.")
                return
            os.rename(filePath, new_path)

    def onFileDelete(self):
        print("delete")