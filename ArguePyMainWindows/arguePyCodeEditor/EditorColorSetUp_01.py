import sys

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from ArguePyMainWindows.arguePyCodeEditor.lineNumberWidget import LineNumberArea

"""
ITA:
    Questa classe è un widget che si occupa di gestire il colore e il font del codice.
ENG:
    This class is a widget that is responsible for managing the color and font of the code.
"""


class EditorColorSetUp(QPlainTextEdit):
    configFontAndColor = {
        "systemFont": QFont("Consolas", 12),
        "widgetFont": QFont("Consolas", 12),
        "LineNumbersFont": QFont("Consolas", 12),
        "backgroundColor": QColor(30, 31, 34),
        "textColor": QColor(167, 183, 198),
        "lineNumberColor": QColor(200, 200, 240, 255),
        "lineNumberBackgroundColor": QColor(30, 31, 34).darker(110),
        "indentationLineColor": QColor(255, 100, 100, 255),
        "indentationLineWidth": 1,
        "indentationWidth": 4,
        "indentationLinesList": [],
        "selectionColor": QColor(0, 122, 204),
        "selectionBackgroundColor": QColor(30, 31, 34).lighter(110),
        "caretColor": QColor(255, 255, 255),
        "caretBackgroundColor": QColor(255, 255, 255),
        "marginColor": QColor(255, 255, 255),
        "marginTextColor": QColor(255, 255, 255),
        "marginBackgroundColor": QColor(255, 255, 255),
    }
    lineNumberArea: LineNumberArea
    zoomLevel = 1.0
    lineSpacing = 1.2
    lineNumberAreaWidthScale = 1.3
    indentationWidthScale = 0.7
    indentationLinesList = []

    def __init__(self, mainWidget, parent=None):
        super(EditorColorSetUp, self).__init__(parent)
        self.mainWidget = mainWidget
        self.parent = parent
        self.zoomLevel = 1.0
        self.setFontAndColor(self.configFontAndColor)
        self.initLineNumberArea()

    def setFontAndColor(self, dictionary):
        self.configFontAndColor = dictionary
        self.setFont(self.configFontAndColor["widgetFont"])
        self.setStyleSheet("background-color: rgb({0}, {1}, {2}); color: rgb({3}, {4}, {5});".format(
            self.configFontAndColor["backgroundColor"].red(),
            self.configFontAndColor["backgroundColor"].green(),
            self.configFontAndColor["backgroundColor"].blue(),
            self.configFontAndColor["textColor"].red(),
            self.configFontAndColor["textColor"].green(),
            self.configFontAndColor["textColor"].blue(),
        ))

    # ----------------------------------  Zoom  ----------------------------------

    def wheelEvent(self, event):
        """
        ITA:
            Ridefinisce il metodo wheelEvent per permettere di usare la rotellina del mouse per lo zoom.
        ENG:
            Redefines the wheelEvent method to allow the use of the mouse wheel for zoom.
        :param event:
        :return:
        """
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn()
                self.configFontAndColor["LineNumbersFont"].setPointSize(
                    self.configFontAndColor["LineNumbersFont"].pointSize() + 1)
                self.zoomLevel += 0.1
            else:
                self.zoomOut()
                self.configFontAndColor["LineNumbersFont"].setPointSize(
                    self.configFontAndColor["LineNumbersFont"].pointSize() - 1)
                self.zoomLevel -= 0.1
        else:
            super().wheelEvent(event)

    # ----------------------------------  Line Number  ----------------------------------

    def paintEvent(self, e: QPaintEvent) -> None:
        super().paintEvent(e)
        painter = QPainter(self.viewport())
        # disegna una linea orizzontale per ogni riga di testo
        height = self.fontMetrics().height()
        for i in range(self.document().blockCount()):
            top = self.blockBoundingGeometry(self.document().findBlockByNumber(i)).translated(
                self.contentOffset()).top()
            color = QColor(20, 20, 40, 90)
            pen = QPen(color, 1)
            # long dash line
            pen.setStyle(Qt.PenStyle.DotLine)
            painter.setPen(pen)
            line = QLineF(0, int(top + height), int(self.width()), int(top + height))
            painter.drawLine(line)

    def initLineNumberArea(self):
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.setFont(
            self.configFontAndColor["LineNumbersFont"]
        )
        painter.setPen(self.configFontAndColor["lineNumberColor"])
        painter.fillRect(event.rect(), self.configFontAndColor["lineNumberBackgroundColor"])

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                rect = QRectF(0, top, self.lineNumberArea.width(), self.fontMetrics().height())
                painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        return 4 + self.fontMetrics().horizontalAdvance('9') * digits

    def resizeEvent(self, event):
        QPlainTextEdit.resizeEvent(self, event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = self.configFontAndColor["selectionBackgroundColor"]
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    # ----------------------------------  Indentation Line  ----------------------------------

    def searchIndentation(self):
        """
        Restituisce una lista linee QLine() che verrano poi disegnate per rappresentare l'indentazione.
        L'indentazione viene mostrata solo se la riga inizia con "def".
        Se le righe successive fanno parte della stessa funzione allora non viene mostrata la linea di indentazione,
        altrimenti no.
        """
        indentation = 0
        returnPressed = 0
        isFoundADef = False
        linesOfCode = self.toPlainText().splitlines()
        for row, line in enumerate(linesOfCode):
            # se la riga inizia con "def" allora aggiungiamo l'indentazione event la coordinata x
            if "def " in line and not isFoundADef:
                indentation = len(line) - len(line.lstrip())
                self.appendToLineIndentationList(indentation, row)
                isFoundADef = True
            # se la riga non inizia con "def" ma abbiamo già registrato l'indentazione
            elif line.startswith(" ") and isFoundADef:
                self.appendToLineIndentationList(indentation, row)

            # se la riga è vuota ma c'è già un'indentazione registrata
            elif line == "" and isFoundADef:
                if returnPressed == 0:
                    self.appendToLineIndentationList(indentation, row)
                    returnPressed += 1
                else:
                    self.indentationLinesList.pop()
                    returnPressed = 0
            if "def " in line and isFoundADef:
                # E' una nuova definizione
                self.indentationLinesList.pop()
                if self.indentationLinesList:
                    self.indentationLinesList.pop()
                self.appendToLineIndentationList(indentation, row)

    def appendToLineIndentationList(self, indentation, row):
        fontMetrics = QFontMetrics(self.configFontAndColor["font"])
        x = indentation * fontMetrics.averageCharWidth()
        self.indentationLinesList.append((row, indentation, x))

    def drawLine(self):
        """
        ITA:
            Disegna le linee di indentazione per le righe contenenti la keyword "def".
        ENG:
            Draws the indentation lines for the rows containing the "def" keyword.
        """
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(self.configFontAndColor["indentationLineColor"], 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,)
        pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(pen)

        for row, indentation, x in self.indentationLinesList:
            top = self.blockBoundingGeometry(self.document().findBlockByNumber(row)).translated(
                self.contentOffset()).top()
            bottom = top + self.blockBoundingRect(self.document().findBlockByNumber(row)).height()
            h = self.fontMetrics().height() * self.zoomLevel
            line = QLineF(int(x), int(bottom), int(x), int(bottom + h))
            painter.drawLine(line)
        painter.end()


# ----------------------------------  TEST  ----------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EditorColorSetUp(None)
    window.show()
    sys.exit(app.exec())
