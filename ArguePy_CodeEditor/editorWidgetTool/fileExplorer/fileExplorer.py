from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTreeView, QWidget, QVBoxLayout, QFileSystemModel, QTreeWidgetItem

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
        # Crea il modello del file system
        self.model = QFileSystemModel()
        self.model.setRootPath(self.mainWindows.projectPath)
        self.model.setNameFilterDisables(False)

        # this set icon
        iconProvider = CustomFileIconProvider()
        # set the custom icon provider for the model
        self.model.setIconProvider(iconProvider)

        # Crea la vista a albero
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.mainWindows.projectPath))
        root_index = self.model.index(self.mainWindows.projectPath)
        self.tree.setExpanded(root_index, True)
        self.tree.setColumnWidth(0, 250)

        # Aggiungi la vista a albero al layout
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        self.setLayout(layout)

    def initConnection(self):
        """
        ITA:
            Questo metodo inizializza le connessioni tra i segnali e i metodi.
        ENG:
            This method initializes the connections between the signals and the methods.
        :return:
        """
        self.tree.clicked.connect(self.onTreeviewDoubleClicked)

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

