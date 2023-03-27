import os

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFileIconProvider


class CustomFileIconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo == QFileIconProvider.File:
            # get the file name and extension
            fileName = self.fileInfo(fileInfo).fileName()
            extension = self.fileInfo(fileInfo).suffix()

            # check for extension and return the appropriate icon
            if extension == 'py':
                return QIcon(os.path.abspath('ArguePy_CodeEditor/editorWidgetTool/fileExplorer/icon/script.png'))
            elif extension == 'txt':
                return QPixmap('ArguePy_CodeEditor/editorWidgetTool/fileExplorer/icon/script--pencil.png')
            elif extension == 'csv':
                return QPixmap('ArguePy_CodeEditor/editorWidgetTool/fileExplorer/icon/script-excel.png')
        # se è una cartella
        elif fileInfo == QFileIconProvider.Folder:
            return QIcon(os.path.abspath('ArguePy_CodeEditor/editorWidgetTool/fileExplorer/icon/folder-horizontal-open.png'))
        # for all other file types, use the default icon provider
        return super().icon(fileInfo)
