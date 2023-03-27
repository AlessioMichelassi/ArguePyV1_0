import os

from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent, QDragLeaveEvent
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeView


class treeViewOverride(QTreeView):
    backGroundColor = "rgb(30, 30, 30)"
    backGroundColorAlt = "rgb(21, 21, 21)"
    selectedColor = "rgba(100, 70, 70, 40)"
    selectionBorderColor = "rgb(100, 40, 40)"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlternatingRowColors(False)
        self.setAcceptDrops(True)
        self.initStyle()

    def initStyle(self):
        # https://doc.qt.io/qt-5/stylesheet-examples.html
        # https://doc.qt.io/qt-5/stylesheet-reference.html
        # https://doc.qt.io/qt-5/stylesheet-syntax.html
        # this is useful for the tree view
        # https://joekuan.wordpress.com/2015/10/02/styling-qt-qtreeview-with-css/

        self.setStyleSheet(f"""
            QTreeView {{
                border: 1px solid rgb(0, 0, 0);
                border-radius: 5px;
                background-color: {self.backGroundColor};
                alternate-background-color: {self.backGroundColorAlt};
            }}
            QTreeView::item:selected {{
                background-color: {self.selectedColor};
                border: 1px solid {self.selectionBorderColor};
                border-radius: 5px;
                
            }}
            QTreeView::item:selected:active {{
                background-color: {self.selectedColor};
                border: 1px solid {self.selectionBorderColor};
                border-radius: 5px;
            }}
            QTreeView::item:selected:!active {{
                background-color: {self.selectedColor};
                border: 1px solid {self.selectionBorderColor};
                border-radius: 5px;
            }}
            QTreeView::branch {{
                background: {self.backGroundColor};
            }}
            QTreeView::branch:closed:has-children {{
                border-image: none;
                image: url(ArguePy_CodeEditor/editorWidgetTool/fileExplorer/icon/control.png);
            }}
            QTreeView::branch:open:has-children {{
                border-image: none;
                image: url(ArguePy_CodeEditor/editorWidgetTool/fileExplorer/icon/control-270.png);
            }}
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """
        ITA:
            Questo metodo viene chiamato quando un oggetto viene trascinato sopra la vista a albero.
            In pratica quello che succede è che viene controllato se l'oggetto trascinato è un file locale perchè
            se non lo è non è possibile spostarlo.
        ENG:
            This method is called when an object is dragged over the tree view.
            Basically what happens is that it is checked if the dragged object is a local file because
            if it is not it is not possible to move it.
        :param event:
        :return:
        """
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        """
        ITA:
            Il metodo dragMoveEvent che viene chiamato quando si sta spostando un elemento all'interno dell'albero.
        ENG:
            The dragMoveEvent method that is called when an element is being moved within the tree.
        :param event:
        :return:
        """
        if self.indexAt(event.pos()).isValid():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        """
        ITA:
            Il metodo dragLeaveEvent che viene chiamato quando si lascia l'area di trascinamento.
        ENG:
            The dragLeaveEvent method that is called when you leave the drag area.
        :param event:
        :return:
        """
        event.accept()

    def dropEvent(self, event: QDropEvent):
        """
        ITA:
            Il metodo dropEvent che viene chiamato quando si lascia rilascia l'oggetto trascinato sull'albero.
        ENG:
            The dropEvent method that is called when you release the dragged object on the tree.
        :param event:
        :return:
        """
        event.acceptProposedAction()
        pos = event.pos()
        index = self.indexAt(pos)
        if index.isValid():
            dirPath = self.model().filePath(index)
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    filePath = url.toLocalFile()
                    # Sposta il file nella nuova posizione
                    self.moveFile(filePath, dirPath)
        event.accept()

    def moveFile(self, filePath, dirPath):
        newFilePath = os.path.join(dirPath, os.path.basename(filePath))
        os.rename(filePath, newFilePath)
