import contextlib
import importlib
import json
import random
import re
import ast

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

operation = ["=", "+", "-", "*", "/", "%", "**", "//", "&", "|", "^", "~", "<<", ">>", "<", ">", "+=",
             "*=", "<=", ">=", "==", "!=", "<>", "(", ")", "[", "]", "{", "}", "@", ",", ":", ".",
             "..."]


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
        self.rehighlight()

    def loadRules(self):
        rules = []
        with open("/home/tedk/PycharmProjects/ArguePyV1_0/ArguePyMainWindows/arguePyCodeEditor/SintaxHighlighters/dictionary6.json", "r") as f:
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
                if word in [operation]:
                    pattern, rule = self.findPatternRule(word, "operation")
                elif word == "":
                    pattern = QRegularExpression(f"""{_pattern}{_pattern}""")
                else:
                    pattern = QRegularExpression(f"{_pattern}{word}{_pattern}")
                rule = HighlightingRule(pattern, classFormat)
                rules.append(rule)
        print(rules)
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
        keyword = dir(module)
        classFormat = QTextCharFormat()
        classFormat.setFontWeight(QFont.Bold)
        classFormat.setForeground(color)
        for word in keyword:
            pattern = QRegularExpression("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, classFormat)
            if rule not in self.highlightingRules:
                self.highlightingRules.append(rule)
        self.rehighlight()

    def findPatternRule(self, word, _type):
        if _type == "operation":
            classFormat = QTextCharFormat()
            classFormat.setFontWeight(QFont.Bold)
            classFormat.setForeground(QColor(250, 250, 250))
            pattern = QRegularExpression(f"\\b'\{word}'\\b")
            rule = HighlightingRule(pattern, classFormat)
            return pattern, rule

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegularExpression(rule.pattern)
            iterator = expression.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)
