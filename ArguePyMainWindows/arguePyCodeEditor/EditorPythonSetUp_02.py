import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ArguePyMainWindows.arguePyCodeEditor.EditorColorSetUp_01 import EditorColorSetUp

from ArguePyMainWindows.arguePyCodeEditor.SintaxHighlighters.pyHighLighter import pythonHighLighter

"""
ITA:
    Questa classe è un widget che si occupa di gestire il syntaxHighlighter del codice e il completer
ENG:
    This class is a widget that is responsible for managing the syntaxHighlighter of the code and the completer.
"""
python_keywords = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue',
    'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in',
    'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield',
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr',
    'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval',
    'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
    'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list', 'locals', 'map',
    'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property',
    'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str',
    'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__', 'NotImplemented', 'Ellipsis',
    '__debug__', 'BaseException', 'Exception',
]

specials = ["__init__", "__str__", "__repr__", "__len__", "__getitem__", "__setitem__", "__delitem__", "__iter__",
            "__next__", "__eq__", "__ne__", "__lt__", "__le__", "__gt__", "__ge__", "__add__", "__sub__", "__mul__",
            "__truediv__", "__floordiv__", "__mod__", "__pow__", "__radd__", "__rsub__"]

python_keywords.extend(specials)


class EditorPythonSetUp(EditorColorSetUp):
    completer: QCompleter
    pythonHighlighter: pythonHighLighter

    def __init__(self, mainWidget, parent=None):
        super(EditorPythonSetUp, self).__init__(mainWidget, parent)
        self.mainWidget = mainWidget
        self.parent = parent
        self.pythonHighlighter = pythonHighLighter(self.document(), self)
        self.initCompleter()

    # ---------------------------------- COMPLETER ----------------------------------

    @staticmethod
    def levenshteinDistance(a, b):
        """
        ITA:
        Calcola la distanza di Levenshtein tra due stringhe. Ovvero il numero minimo di operazioni
        necessarie per trasformare una stringa nell'altra.
        Le operazioni possibili sono:
        - Inserimento di un carattere
        - Cancellazione di un carattere
        - Sostituzione di un carattere
        ENG:
        Calculates the Levenshtein distance between two strings. That is, the minimum number of
        operations needed to transform one string into the other.
        The operations allowed are:
        - Insertion of a character
        - Deletion of a character
        - Substitution of a character
        :param a: stringa 1
        :param b:   stringa 2
        :return:
        """
        if a == b:
            return 0
        if len(a) < len(b):
            a, b = b, a

        previous_row = range(len(b) + 1)
        for i, c1 in enumerate(a):
            current_row = [i + 1]
            for j, c2 in enumerate(b):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def closestWords(self, input_word, word_list, max_distance=None, top_n=None):
        """
        ITA:
            Restituisce una lista di parole che hanno una distanza di Levenshtein minore o uguale a max_distance
            rispetto alla parola input_word.
        ENG:
            Returns a list of words that have a Levenshtein distance less than or equal to max_distance
            from the input_word.
        :param input_word:
        :param word_list:
        :param max_distance:
        :param top_n:
        :return:
        """
        word_distances = [(word, self.levenshteinDistance(input_word, word)) for word in word_list]

        if max_distance is not None:
            word_distances = [(word, distance) for word, distance in word_distances if distance <= max_distance]

        word_distances.sort(key=lambda x: x[1])

        if top_n is not None:
            word_distances = word_distances[:top_n]

        return [word for word, _ in word_distances]

    def initCompleter(self):
        """
        Inizializza il completer
        :return:
        """
        self.completer = QCompleter(python_keywords, self)
        self.completer.setWidget(self)
        # PopupCompletion mostra la lista dei completamenti
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)

    def addWordToCompleter(self, word):
        """
        ITA:
            Aggiunge una parola al completer
        ENG:
            Adds a word to the completer
        :param word:
        :return:
        """
        self.completer.model().addWord(word)

    def removeWordFromCompleter(self, word):
        """
        ITA:
            Rimuove una parola dal completer
        ENG:
            Removes a word from the completer
        :param word:
        :return:
        """
        self.completer.model().removeWord(word)

    def returnListOfWords(self):
        """
        ITA:
            Ritorna una lista di tutte le parole presenti nel completer
        ENG:
            Returns a list of all the words present in the completer
        :return:
        """
        return self.completer.model().words

    def insertCompletion(self, completion):
        """
        ITA:
            Inserisce il completamento nella posizione corretta. Per trovare la posizione,
            si scorre la stringa a partire dalla posizione del cursore fino a trovare
            l'ultimo carattere. Quindi si inserisce il completamento
            dopo tale carattere.
        ENG:
            Inserts the completion in the correct position. To find the position,
            the string is scrolled from the cursor position until the last character is found.
            Then the completion is inserted after that character.
        :param completion:
        :return:
        """
        if self.completer.widget() != self:
            return
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.MoveOperation.Right)
        tc.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.KeepAnchor, extra)
        tc.insertText(completion)
        self.setTextCursor(tc)

    def updateCompleterPopupItemsOld(self, completion_prefix):
        self.completer.setCompletionPrefix(completion_prefix)
        self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

    def updateCompleterPopupItems(self, completion_prefix):
        # sourcery skip: skip-sorted-list-construction
        # Trova i suggerimenti basati sul prefisso
        prefix_matches = [word for word in python_keywords if word.startswith(completion_prefix)]

        # Cerca le parole più vicine
        closest_words = self.closestWords(completion_prefix, python_keywords, max_distance=3, top_n=10)

        # Combina i suggerimenti basati sul prefisso con le parole più vicine
        combined_words = list(set(prefix_matches + closest_words))
        combined_words.sort()

        # Aggiorna il modello del completer con le parole combinate
        model = QStringListModel()
        model.setStringList(combined_words)
        self.completer.setModel(model)

        self.completer.setCompletionPrefix(completion_prefix)
        self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

    def textUnderCursor(self):
        """
        Ritorna il testo sotto il cursore, ovvero il testo che si sta scrivendo
        :return:
        """
        cursor = self.textCursor()
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        return cursor.selectedText()

    # ---------------------------------- KEY EVENT ----------------------------------

    def event(self, event):
        if event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab and not self.completer.popup().isVisible():
                if self.textCursor().hasSelection():  # se una parte del testo è selezionata
                    self.indentSelectedText()
                else:
                    self.insertPlainText("    ")
                return True
            # se viene premuto shift + tab fa l'indent alla rovescia
            elif event.key() == Qt.Key.Key_Backtab and not self.completer.popup().isVisible():
                self.unIndentSelectedText()
                return True
        return super().event(event)

    def keyPressEvent(self, event):
        if self.handleCompleterKeyPressEvent(event):
            return
        # Auto completamento delle parentesi
        if event.key() in [Qt.Key.Key_BraceLeft, Qt.Key.Key_BracketLeft, Qt.Key.Key_ParenLeft, Qt.Key.Key_QuoteDbl,
                           Qt.Key.Key_Apostrophe]:
            self.parenthesesAutoComplete(event)
        elif event.key() == Qt.Key.Key_Return:
            if not self.completer.popup().isVisible():  # Aggiungi questa riga
                self.insertNewLine()
        # se viene premuto il tasto #
        elif event.key() == Qt.Key.Key_NumberSign:
            if self.textCursor().hasSelection():
                self.commentBlock()
            else:
                super().keyPressEvent(event)
        else:
            super(EditorPythonSetUp, self).keyPressEvent(event)

        current_char = self.textUnderCursor()
        if not self.is_valid_completion_char(current_char):
            self.completer.popup().hide()

    def is_valid_completion_char(self, char):
        return char.isalnum() or char == '_' or char == '.'

    def handleCompleterKeyPressEvent(self, event):
        if self.completer.popup().isVisible():
            if event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Escape):
                event.ignore()
                return True

            if event.key() in [Qt.Key.Key_Tab, Qt.Key.Key_Return]:
                completition = self.completer.currentCompletion()
                # se scrivo Fa event poi tab viene scritto Faalse...
                self.insertPlainText(completition[len(self.completer.completionPrefix()) + 1:])
                self.completer.popup().hide()
                return True

            elif event.key() == Qt.Key.Key_Backtab:
                self.completer.setCurrentRow(self.completer.currentRow() - 1)
                return True
        elif self.completer.popup().isHidden():
            # se viene premuto spazio o invio il pop up non deve comparire
            # if key is space or enter the popup should not appear
            if event.key() in [Qt.Key.Key_Space, Qt.Key.Key_Return]:
                self.completer.popup().hide()
                return False
        completion_prefix = self.textUnderCursor()
        if completion_prefix != self.completer.completionPrefix():
            self.updateCompleterPopupItems(completion_prefix)

        if len(completion_prefix) > 0:
            self.completer.setWidget(self)
            rect = self.cursorRect()
            rect.setWidth(self.completer.popup().sizeHintForColumn(0)
                          + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(rect)
        else:
            self.completer.popup().hide()
        return False

    def parenthesesAutoComplete(self, event):
        """
        Questa funzione si occupa di inserire le parentesi corrispondenti
        Se proviamo a scrive una parentesi event non è segnato nessun testo crea la parentsesi corrispondente event sponsta
        il cursore al centro. Se invece sotto sottolieiamo una porzione di testo, event clicchiamo su una parentesi di
        apertura inserisce automaticamente la parentesi di chiusura event sposta il cursore alla fine del testo selezionato
        :param event:
        :return:
        """
        matching = {Qt.Key.Key_BraceLeft: "}", Qt.Key.Key_BracketLeft: "]",
                    Qt.Key.Key_ParenLeft: ")", Qt.Key.Key_QuoteDbl: "\"", Qt.Key.Key_Apostrophe: "'"}
        if selectedText := self.textCursor().selectedText():
            self.insertPlainText(f"{event.text()}{selectedText}{matching[event.key()]}")
            # sposta il cursore alla fine del testo selezionato
            self.moveCursor(QTextCursor.MoveOperation.EndOfBlock)
            # se non è segnato nessun testo crea la parentesi corrispondente
            # event sposta il cursore al centro
        elif not selectedText:
            self.insertPlainText(f"{event.text()}{matching[event.key()]}")
            self.moveCursor(QTextCursor.MoveOperation.Left)

    def indentSelectedText(self):
        """
        Indenta il testo selezionato
        :return:
        """
        text = self.textCursor().selectedText()
        lines = text.splitlines()
        for i in range(len(lines)):
            lines[i] = f"    {lines[i]}\n"
        self.insertPlainText("".join(lines))

    def searchIndentationInFirstLineOfSelection(self, text):
        """
        Quando viene premuto shift + tab se l'utente ha selezionato la prima linea
        solo parzialmente, l'indentazione non risulterebbe corretta. Questa funzione
        cerca l'indentazione della prima linea ritorna il testo completo indentato.
        :param text:
        :return:
        """
        endPosition = self.textCursor().selectionEnd()
        cursor = self.textCursor()
        newStartPosition = cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        startPosition = cursor.selectionStart()
        # crea una nuova selezione che va dall'inizio della prima riga
        # alla fine della selezione corrente
        cursor.setPosition(startPosition)
        cursor.setPosition(endPosition, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)
        text = self.textCursor().selectedText()
        return text

    def unIndentSelectedText(self):
        """
        Sposta a sinistra il testo selezionato di quattro spazi
        """
        text = self.searchIndentationInFirstLineOfSelection(self.textCursor().selectedText())
        # rimuove i primi quattro caratteri di ogni riga
        lines = text.splitlines()
        for i in range(len(lines)):
            if lines[i][:4] == "    ":
                lines[i] = f"{lines[i][4:]}\n"
        self.insertPlainText("".join(lines))

    def insertNewLineOld(self):
        """
        :return:
        """
        previousLine = self.textCursor().block().previous().text()

        indentation = ""
        # calcola il numero di spazi all'inizio della righa
        indentationNumber = len(self.textCursor().block().text()) - len(self.textCursor().block().text().lstrip())
        indentation = " " * indentationNumber
        # se l'ultimo carattere della riga è : allora aggiunge un'altra indentazione
        # se la riga non è vuota
        if len(self.textCursor().block().text()) > 0:
            if self.textCursor().block().text()[-1] == ":":
                indentation += "    "
            self.insertPlainText(f"\n{indentation}")
        else:
            self.insertPlainText("\n")

    def insertNewLine(self):
        """
        ITA:
            NewLine mette il cursore a capo della riga successiva.
            Ci sono in alcuni casi in cui il testo deve essere indentato:
            Se la riga precedente ha un indentazione, l'indentazione deve essere copiata
            Se la riga precedente termina con : allora l'indentazione deve essere aumentata di 4 spazi a meno che il cursore non sia a inizio riga
            il che vuol videre che si sta spostando la riga alla riga successiva e quindi la riga precedente non deve essere indentata.
            Se la riga precedente è vuota allora l'indentazione non deve essere copiata.
        ENG:
            NewLine puts the cursor on the next line.
            There are some cases in which the text must be indented:
            If the previous line has an indentation, the indentation must be copied
            If the previous line ends with: then the indentation must be increased by 4 spaces unless the cursor is at the beginning of the line
            which means that you are moving the line to the next line and therefore the previous line should not be indented.
            If the previous line is empty then the indentation should not be copied.
        :return:
        """
        previousLine = self.textCursor().block().previous().text()
        indentation = ""
        # calcola il numero di spazi all'inizio della righa
        indentationNumber = len(self.textCursor().block().text()) - len(self.textCursor().block().text().lstrip())
        indentation = " " * indentationNumber
        # se l'ultimo carattere della riga è : allora aggiunge un'altra indentazione
        # a meno che il caratteri non si trovi a inizio riga
        if len(self.textCursor().block().text()) > 0 and not self.textCursor().atBlockStart():
            if self.textCursor().block().text()[-1] == ":":
                indentation += "    "
            self.insertPlainText(f"\n{indentation}")
        # se il cursore è a inizio riga, la riga non è vuota, copia l'indentazione della riga attuale
        elif len(self.textCursor().block().text()) > 0:
            self.insertPlainText(f"\n{indentation}")
        # se il cursore è a inizio riga e la riga precedente non è vuota, copia l'indentazione della riga precedente
        elif self.textCursor().atBlockStart() and len(previousLine) > 0:
            indentationNumber = len(previousLine) - len(previousLine.lstrip())
            indentation = " " * indentationNumber
            self.insertPlainText(f"\n{indentation}")
        else:
            self.insertPlainText("\n")

    def commentBlock(self):
        """
        ITA:
            Se viene premuto # event il testo è selezionato, commenta il testo selezionato
        ENG:
            If # is pressed and the text is selected, comment the selected text
        """
        text = self.searchIndentationInFirstLineOfSelection(self.textCursor().selectedText())
        lines = text.splitlines()
        for i in range(len(lines)):
            if lines[i].startswith("    "):
                lines[i] = f"    # {lines[i][4:]}\n"
            else:
                lines[i] = f"# {lines[i]}\n"
        self.insertPlainText("".join(lines))


# ----------------------------------  TEST  ----------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditorPythonSetUp(None)
    window.show()
    sys.exit(app.exec())
