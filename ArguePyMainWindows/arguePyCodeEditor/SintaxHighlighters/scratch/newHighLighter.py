import contextlib
import importlib
import json
import random
import re
import ast

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *


class HighlightingRule:
    def __init__(self, pattern, _format):
        self.pattern = pattern
        self.format = _format


class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append(f'{node.module}.{alias.name}')


class PythonHighlighter(QSyntaxHighlighter):

    def __init__(self, document, parent=None):
        super(PythonHighlighter, self).__init__(parent)
        self.document = document
        self.highlightingRules = self.loadRules()

    @staticmethod
    def loadRules():
        rules = []
        with open("dictionary6.json", "r") as f:
            data = json.load(f)
        for key, value in data.items():
            classFormat = QTextCharFormat()
            classFormat.setFontWeight(QFont.Bold)
            color = value["color"].replace("rgb(", "").replace(")", "").split(",")
            classFormat.setForeground(QColor(int(color[0]), int(color[1]), int(color[2])))
            _pattern = value["regularExpressions"]
            if _pattern == "":
                _pattern = "\\b"
            keyword = json.loads(value["value"])
            if len(keyword) == 0:
                keyword = [""]
            for word in keyword:
                if word in ["=", "+", "-", "*", "/", "%", "**", "//", "&", "|", "^", "~", "<<", ">>", "<", ">", "+=",
                            "*=", "<=", ">=", "==", "!=", "<>", "(", ")", "[", "]", "{", "}", "@", ",", ":", ".",
                            "..."]:
                    pattern = QRegularExpression(f"{_pattern}'\{word}'{_pattern}")
                else:
                    pattern = QRegularExpression(f"{_pattern}{word}{_pattern}")
                if word == "":
                    pattern = QRegularExpression(f"""{_pattern}{_pattern}""")
                rule = HighlightingRule(pattern, classFormat)
                rules.append(rule)
        return rules

    def addRule(self, library, color):
        if library.endswith("*"):
            library = library.replace(".*", "")
        try:
            self.searchLibraryDefinition(library, color)
        except Exception as e:
            print(f"Failed to import {library}: {e}")

    def searchLibraryDefinition(self, library, color):
        module = importlib.import_module(library)
        keyword = set(dir(module))
        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(color)
        for word in keyword:
            pattern = QRegularExpression("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, classFormat)
            if rule not in self.highlightingRules:
                self.highlightingRules.append(rule)
        self.rehighlightBlock(self.currentBlock())

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegularExpression(rule.pattern)
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)


class codeEditor(QTextBrowser):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighter = PythonHighlighter(self.document(), self)
        self.setTabStopDistance(4)
        self.setPlainText("")

    def find_imports(self, code):
        try:
            parsed = ast.parse(code)
        except SyntaxError:
            return []

        visitor = ImportVisitor()
        visitor.visit(parsed)
        return visitor.imports

    def setPlainText(self, text):
        imports = self.find_imports(text)
        if imports:
            for import_ in imports:
                if import_.startswith('from '):
                    library_name = import_.split(' ')[1]
                else:
                    library_name = import_
                # crea un colore random
                color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.highlighter.addRule(library_name, color)
        super().setPlainText(text)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.editor = codeEditor()

        with open("/home/tedk/Desktop/testArgueFolder/project1/main.py", "r") as f:
            self.editor.setPlainText(f.read())
        self.setCentralWidget(self.editor)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec()
