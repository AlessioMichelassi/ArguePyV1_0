import os
import shutil

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from arguePyResource.resource_rc import *


class treeViewOverride(QTreeView):
    textColor = "rgb(245, 245, 245)"
    backGroundColor = "rgb(30, 30, 30)"
    backGroundColorAlt = "rgb(21, 21, 21)"
    selectedColor = "rgba(100, 70, 70, 40)"
    selectionBorderColor = "rgb(100, 40, 40)"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIndentation(20)
        self.setSelectionMode(QTreeView.SelectionMode.SingleSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setAlternatingRowColors(False)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.initStyle()
        self.setFocusPolicy(Qt.StrongFocus)
        self.installEventFilter(self)

    def initStyle(self):
        # https://doc.qt.io/qt-5/stylesheet-examples.html
        # https://doc.qt.io/qt-5/stylesheet-reference.html
        # https://doc.qt.io/qt-5/stylesheet-syntax.html
        # this is useful for the tree view
        # https://joekuan.wordpress.com/2015/10/02/styling-qt-qtreeview-with-css/

        self.setStyleSheet(f"""
            QTreeView {{
                color: {self.textColor};
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
                image: url(:/resource/iconControlClose.png);
            }}
            QTreeView::branch:open:has-children {{
                border-image: none;
                image: url(:/resource/iconControlOpen.png);
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
        if event.source():
            QTreeView.dropEvent(self, event)
        else:
            ix = self.indexAt(event.pos())
            if not self.model().isDir(ix):
                ix = ix.parent()
            pathDir = self.model().filePath(ix)
            m = event.mimeData()
            if m.hasUrls():
                urlLocals = [url for url in m.urls() if url.isLocalFile()]
                accepted = False
                for urlLocal in urlLocals:
                    path = urlLocal.toLocalFile()
                    info = QFileInfo(path)
                    n_path = QDir(pathDir).filePath(info.fileName())
                    o_path = info.absoluteFilePath()
                    if n_path == o_path:
                        continue
                    if info.isDir():
                        QDir().rename(o_path, n_path)
                    else:
                        qfile = QFile(o_path)
                        if QFile(n_path).exists():
                            n_path += "(copy)"
                        qfile.rename(n_path)
                    accepted = True
                if accepted:
                    event.acceptProposedAction()

    def mouseDoubleClickEvent(self, event) -> None:
        event.ignore()

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            print(event.key())
            if event.key() == Qt.Key.Key_Delete:
                self.deleteSelected()
                return True
        return super().event(event)

    def deleteSelected(self):
        """
        ITA:
            Questo metodo viene chiamato quando viene premuto il tasto delete sulla tastiera.
            Il metodo si occupa di eliminare il file o la cartella selezionata.
        ENG:
            This method is called when the delete key is pressed on the keyboard.
            The method is responsible for deleting the selected file or folder.
        :return:
        """
        index = self.currentIndex()
        if index.isValid():
            path = self.model().filePath(index)
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)

