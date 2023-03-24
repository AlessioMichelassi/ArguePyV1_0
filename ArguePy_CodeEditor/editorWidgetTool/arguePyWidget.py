import os
import subprocess
import sys

from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QFileDialog, QMenu

from ArguePy_CodeEditor.editorWidgetTool.codeEditorOverride.EditorCodeMain import codeEditor
from ArguePy_CodeEditor.editorWidgetTool.codeEditorOverride.searchAndReplaceWidget import searchAndReplaceWidget
from ArguePy_CodeEditor.editorWidgetTool.ConsoleWidget.cosole import Console

"""
ITA: 
    ArguePy è un editor di codice python che permette di eseguire il codice. L'editor è contenuto nella
    variabile self.codeEditor e implementa varie funzionalità come la ricerca e la sostituzione, la
    colorazione del codice, la possibilità di eseguire il codice e di visualizzare il risultato in una console.
    
ENG:
    ArguePy is a python code editor that allows you to run the code. The editor is contained in the
    variable self.codeEditor and implements various features such as search and replace, code coloring,
    the ability to run the code and to view the result in a console.
"""


class ArguePyWidget(QWidget):
    colorList = []
    mainLayout = None
    fileName = "untitled"
    console = None

    def __init__(self, mainWidget, parent=None):
        super(ArguePyWidget, self).__init__(parent)
        self.mainWidget = mainWidget
        self.codeEditor = codeEditor(self)
        self.searchWidget = searchAndReplaceWidget(self.codeEditor)
        self.initUI()
        self.initConnection()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.codeEditor)
        self.mainLayout.addWidget(self.searchWidget)
        self.searchWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.mainLayout.setContentsMargins(10, 20, 10, 5)
        self.searchWidget.hide()
        self.setLayout(self.mainLayout)

    def initColorList(self):
        SyntaxHighlighter = self.codeEditor.pythonHighlighter
        self.colorList = [SyntaxHighlighter.keywordColor, SyntaxHighlighter.functionColor,
                          SyntaxHighlighter.builtInColor, SyntaxHighlighter.functionColor,
                          SyntaxHighlighter.selfColor, SyntaxHighlighter.classFunctionColor,
                          SyntaxHighlighter.methodColor, SyntaxHighlighter.braceColor,
                          SyntaxHighlighter.numberColor, SyntaxHighlighter.stringColor,
                          SyntaxHighlighter.commentColor, SyntaxHighlighter.comment2Color]

    def initConnection(self):
        pass

    def setCode(self, code):
        self.codeEditor.setPlainText(code)

    def getCode(self):
        return self.codeEditor.toPlainText()

    def clear(self):
        self.codeEditor.clear()

    def changeColor(self, color, name):
        txt = self.codeEditor.toPlainText()
        self.codeEditor.clear()
        self.pythonHighlighter.setColor(color, name)
        self.codeEditor.insertPlainText(txt)
        self.pythonHighlighter.highlightBlock(self.codeEditor.toPlainText())

    def onNew(self):
        """
        Questo metodo viene chiamato quando si clicca su new
        :return:
        """
        self.fileName = "untitled"
        self.codeEditor.clear()

    def onOpen(self):
        """
        Questo metodo carica il codice dal file con una qDialog
        :return:
        """

        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        if fileName:
            self.onNew()
            with open(fileName, "r") as file:
                self.codeEditor.setPlainText(file.read())
                self.fileName = fileName

    def onSave(self):
        """
        Questo metodo salva il codice nel file con una qDialog
        :return:
        """
        if self.fileName == "untitled":
            self.onSaveAs()
        else:
            with open(self.fileName, "w") as file:
                file.write(self.codeEditor.toPlainText())

    def onSaveAs(self):
        """
        Questo metodo salva il codice nel file con una qDialog
        :return:
        """
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Python Files (*.py)")
        if fileName:
            with open(fileName, "w") as file:
                file.write(self.codeEditor.toPlainText())

    def onPreferences(self):
        """
        Questo metodo mostra il widget per cambiare i colori
        :return:
        """
        pass

    def showContextMenu(self, position):
        """
        ITA:
            Questo metodo mostra il commonMenu contestuale e fa l'override dalla classe QPlaintexEdit
            del code editor.
        ENG:
            This method shows the context commonMenu and override the QPlaintexEdit class from the code editor.
        :param position:
        :return:
        """
        contexMenu = QMenu(self)
        actionCopy = contexMenu.addAction("Copy")
        actionCopyPlus = contexMenu.addAction("Copy Plus CTRL+Shift+C")
        actionPaste = contexMenu.addAction("Paste")
        actionPastePlus = contexMenu.addAction("Paste Plus CTRL+Shift+V")
        separator = contexMenu.addSeparator()
        actionRun = contexMenu.addAction("Run CTRL+R")

        action = contexMenu.exec_(self.codeEditor.mapToGlobal(position))
        if action == actionCopy:
            self.codeEditor.copy()
        elif action == actionCopyPlus:
            self.codeEditor.copyPlus()
        elif action == actionPaste:
            self.codeEditor.paste()
        elif action == actionPastePlus:
            self.codeEditor.pastePlus()
        elif action == actionRun:
            self.mainWidget.onRun()
