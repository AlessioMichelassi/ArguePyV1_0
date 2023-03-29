from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ArguePyMainWindows.arguePyCodeEditor.EditorPythonSetUp_02 import EditorPythonSetUp

"""
ITA:
    Questa classe è QPlainTextEdit con varie funzionalità aggiuntive in modo da poter essere usato come
    editor di codice python. La prima versione era quasi 1500 linee di codice, quindi ho deciso di dividere
    il codice in più classi per renderlo più leggibile e mantenibile. Questa classe è la classe principale
    che contiene tutte le altre classi e funzionalità.
    
ENG:
    This class is QPlainTextEdit with various additional features in order to be used as a python code editor.
    The first version was almost 1500 lines of code, so I decided to divide the code into more classes to make
    it more readable and maintainable. This class is the main class that contains all the other classes and features.
"""


class codeEditor(EditorPythonSetUp):
    searchResult = []
    searchIndex = 0

    def __init__(self, mainWidget, parent=None):
        super(codeEditor, self).__init__(parent)
        self.mainWidget = mainWidget
        self.parent = parent
        self.initUI()
        self.initConnection()
        self.initColorList()

    def initUI(self):
        self.setTabStopDistance(4)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.setTabChangesFocus(True)
        self.setCenterOnScroll(True)
        self.setUndoRedoEnabled(True)
        # setta l'altezza del testo doppia rispetto alla font size
        self.setCursorWidth(3)

    def initConnection(self):
        pass

    def initColorList(self):
        pass

    def contextMenuEvent(self, event):
        """
        ITA:
            Questo metodo serve per sovrascrivere il commonMenu contestuale di QPlainTextEdit.
        ENG:
            This method is used to override the context commonMenu of QPlainTextEdit.
        :param event:
        :return:
        """
        self.mainWidget.showContextMenu(event.pos())

    # ---------------------------- SEARCH WIDGET ----------------------------

    def onSearch(self):
        """
        ITA:
            Apre il widget per la ricerca quando viene premuto il tasto cerca
        ENG:
            Opens the search widget when the search button is pressed
        :return:
        """
        self.mainWidget.searchWidget.show()

    def onSearchText(self, text, caseSensitive=False, wholeWords=False):
        """
        Quando viene premuto il tasto cerca, cerca il testo. Nel caso in cui
        sia selezionato caseSensitive o wholeWords, cerca il testo in base a
        questi parametri.
        :param text:
        :param caseSensitive:
        :param wholeWords:
        :return:
        """
        # posiziona il cursore all'inizio del testo
        self.moveCursor(QTextCursor.MoveOperation.Start)
        # Il Flag di ricerca è un intero che può essere combinato con l'operatore |

        flags = QTextDocument.FindFlag(0)
        if caseSensitive:
            print("caseSensitive")
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if wholeWords:
            print("wholeWords")
            flags |= QTextDocument.FindFlag.FindWholeWords

        # Cerca tutte le occorrenze della parola
        self.searchResult = []
        cursor = self.textCursor()
        while not cursor.isNull():
            cursor = self.document().find(text, cursor, flags)
            if not cursor.isNull():
                self.searchResult.append(cursor.selectionStart())
        # Se sono state trovate occorrenze, evidenzia la prima
        if self.searchResult:
            self.searchIndex = 0
            self.highlightCurrentSearchResult(text)

    def highlightCurrentSearchResult(self, text):
        # Rimuovi l'evidenziazione dalle precedenti occorrenze
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)

        # Evidenzia la nuova occorrenza
        if len(self.searchResult) > 0:
            cursor.setPosition(self.searchResult[self.searchIndex])
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(text))
            self.setTextCursor(cursor)

    def onSearchNext(self, text):
        """
        Quando viene premuto il tasto cerca successivo
        :return:
        """
        if self.searchResult:
            self.searchIndex += 1
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)
            cursor.setPosition(self.searchResult[self.searchIndex])
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(text))
            self.setTextCursor(cursor)

    def onSearchPrevious(self, text):
        """
        Quando viene premuto il tasto cerca precedente
        :return:
        """
        if self.searchResult:
            self.searchIndex -= 1
            cursor = self.textCursor()
            cursor.clearSelection()
            self.setTextCursor(cursor)
            cursor.setPosition(self.searchResult[self.searchIndex])
            cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, len(text))
            self.setTextCursor(cursor)

    def onReplaceText(self, _type, text, newText):
        """
        Sostituisce il testo selezionato con il nuovo testo
        :param text:
        :param newText:
        :return:
        """
        if _type == "single":
            if not self.textCursor().hasSelection():
                self.find(text)
            self.textCursor().insertText(newText)
        elif _type == "all":
            if not self.searchResult:
                self.onSearchText(text)
            if self.searchResult:
                self.replaceAll(text, newText)

    def replaceAll(self, text, newText):
        """
        Sostituisce tutte le occorrenze del testo con il nuovo testo
        :param text:
        :param newText:
        :return:
        """
        while self.find(text):
            self.textCursor().insertText(newText)


