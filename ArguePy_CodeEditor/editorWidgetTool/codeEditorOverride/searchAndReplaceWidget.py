from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class searchAndReplaceWidget(QWidget):
    grpBox: QGroupBox
    mainLayout: QVBoxLayout

    # VARIABLES FOR SEARCH
    lblSearch: QLabel
    vSpacer: QSpacerItem
    chkCaseSensitive: QCheckBox
    chkWholeWord: QCheckBox
    btnUseRegex: QCheckBox

    txtSearch: QLineEdit
    btnSearch: QPushButton
    searchLayout: QVBoxLayout
    layoutSearchText: QHBoxLayout
    layoutSearchLabel: QHBoxLayout

    # VARIABLES FOR REPLACE
    lblReplace: QLabel
    txtReplace: QLineEdit
    btnReplace: QPushButton
    btnReplaceAll: QPushButton
    replaceLayout: QVBoxLayout
    layoutReplaceText: QHBoxLayout
    layoutReplaceLabel: QHBoxLayout

    foundWordsList = []

    def __init__(self, editor: 'pythonCodeEditor', parent=None):
        QWidget.__init__(self, parent)
        self.editor = editor
        self.initUI()
        self.initStyle()
        self.initConnections()
        self.setMaximumHeight(200)

    def initUI(self):
        """
        Inizializza l'interfaccia
        :return:
        """
        # mette i layout di search event replace in una group Box
        self.grpBox = QGroupBox("Search and Replace")

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.grpBox)
        # crea i layout per search event replace
        self.SearchAndReplaceLayout()

        self.grpBox.setLayout(self.layoutMain)
        self.grpBox.setMinimumWidth(self.editor.width() - 20)
        self.setLayout(self.mainLayout)

    def createSearchBox(self):
        """
        Crea il blocco per la ricerca del testo
        :return:
        """
        closeButton = QPushButton(QIcon('close.png'), 'X')
        closeButton.setFixedSize(10, 10)
        closeButton.setStyleSheet('''
                            QPushButton {
                                border: none;
                                background-color: transparent;
                            }
                            QPushButton:hover {
                                background-color: #f0f0f0;
                            }
                        ''')
        closeButton.clicked.connect(self.close)
        closeLayout = QHBoxLayout()
        closeLayout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        closeLayout.addStretch()
        closeLayout.setContentsMargins(0, 0, 0, 0)
        closeLayout.addWidget(closeButton)
        self.lblSearch = QLabel("Search")
        self.vSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.chkCaseSensitive = QCheckBox("case Sensitive")
        self.chkCaseSensitive.setToolTip("means that if you search for \"test\", it will not match \"Test\".")
        self.chkWholeWord = QCheckBox("Whole Word")
        self.chkWholeWord.setToolTip("means that if you search for \"test\", it will not match \"testing\".")

        self.btnUseRegex = QCheckBox("Regex")
        self.btnUseRegex.setDisabled(True)
        # create layout
        self.layoutSearchLabel = QHBoxLayout()
        self.layoutSearchLabel.addWidget(self.lblSearch)
        self.layoutSearchLabel.addSpacerItem(self.vSpacer)
        self.layoutSearchLabel.addWidget(self.chkCaseSensitive)
        self.layoutSearchLabel.addWidget(self.chkWholeWord)
        self.layoutSearchLabel.addWidget(self.btnUseRegex)

        self.txtSearch = QLineEdit()
        self.txtSearch.setPlaceholderText("Search")
        self.txtSearch.setFixedHeight(30)
        self.btnSearch = QPushButton("Search")
        self.btnSearch.setFixedWidth(80)
        self.btnSearch.setFixedHeight(30)
        self.btnPrev = QPushButton("Prev")
        self.btnPrev.setFixedWidth(50)
        self.btnPrev.setFixedHeight(30)
        self.btnNext = QPushButton("Next")
        self.btnNext.setFixedWidth(50)
        self.btnNext.setFixedHeight(30)
        self.layoutSearchText = QHBoxLayout()
        self.layoutSearchText.addWidget(self.txtSearch)
        self.layoutSearchText.addWidget(self.btnSearch)
        self.layoutSearchText.addWidget(self.btnPrev)
        self.layoutSearchText.addWidget(self.btnNext)
        self.layoutSearchText.setContentsMargins(0, 0, 0, 0)

        self.searchLayout = QVBoxLayout()
        self.searchLayout.addLayout(closeLayout)
        self.searchLayout.addLayout(self.layoutSearchLabel)
        self.searchLayout.addLayout(self.layoutSearchText)

    def createReplaceBox(self):
        self.lblReplace = QLabel("Replace")

        layoutReplaceLabel = QHBoxLayout()
        layoutReplaceLabel.addWidget(self.lblReplace)
        layoutReplaceLabel.addSpacerItem(self.vSpacer)

        self.txtReplace = QLineEdit()
        # il placeholder text deve essere italic

        self.txtReplace.setPlaceholderText("Replace")
        self.txtReplace.setFixedHeight(30)
        self.btnReplace = QPushButton("Replace")
        self.btnReplace.setFixedWidth(80)
        self.btnReplace.setFixedHeight(30)
        self.replaceAllButton = QPushButton("Replace All")
        self.replaceAllButton.setFixedHeight(30)
        self.layoutReplaceText = QHBoxLayout()
        self.layoutReplaceText.addWidget(self.txtReplace)
        self.layoutReplaceText.addWidget(self.btnReplace)
        self.layoutReplaceText.addWidget(self.replaceAllButton)
        self.replaceLayout = QVBoxLayout()
        self.replaceLayout.addLayout(layoutReplaceLabel)
        self.replaceLayout.addLayout(self.layoutReplaceText)

    def SearchAndReplaceLayout(self):
        self.createSearchBox()
        self.createReplaceBox()
        self.layoutMain = QVBoxLayout()
        self.layoutMain.addLayout(self.searchLayout)
        self.layoutMain.addLayout(self.replaceLayout)
        self.layoutMain.setContentsMargins(10, 10, 10, 10)

    def initStyle(self):
        self.setFont(QFont("Consolas", 8))
        backGroundColor = self.editor.configFontAndColor["backgroundColor"]
        textColor = self.editor.configFontAndColor["textColor"]
        grpBoxStyle = f"""
                        QGroupBox {{
                            background-color: {backGroundColor.name()};
                            color: {textColor.name()};
                            border: 1px solid {textColor.name()};
                            border-radius: 5px;
                            margin-top: 0.5em;
                        }}"""
        lblStyle = f"""
                    QLabel {{   
                        color: {textColor.name()};
                        font-size: 11px;
                    }}"""
        txtLineEditStyle = f"""
                            QLineEdit {{
                                background-color: {backGroundColor.name()};
                                color: {textColor.name()};
                                border: 1px solid {textColor.name()};
                                border-radius: 5px;
                                padding: 0 8px;
                                font-size: 12px;
                            }}
                QLineEdit::placeholder {{
                    color: {textColor.name()};
                    font-size: 10px;
                    font-style: italic;
                }}
        """
        allStyle = grpBoxStyle + lblStyle + txtLineEditStyle
        self.setStyleSheet(allStyle)

    def initConnections(self):
        self.txtSearch.textChanged.connect(self.onTxtSearchClicked)
        self.txtSearch.returnPressed.connect(self.search)
        self.btnSearch.clicked.connect(self.search)
        self.btnPrev.clicked.connect(self.searchPrev)
        self.btnNext.clicked.connect(self.searchNext)
        self.btnReplace.clicked.connect(self.replace)
        self.replaceAllButton.clicked.connect(self.replaceAll)

    def onTxtSearchClicked(self, text):
        if text:
            self.txtSearch.setPlaceholderText("")
        else:
            self.txtSearch.setPlaceholderText("Search")

    def search(self):
        txt = self.txtSearch.text()
        machCase = self.chkCaseSensitive.isChecked()
        matchWholeWord = self.chkWholeWord.isChecked()
        self.editor.onSearchText(txt, machCase, matchWholeWord)

    def searchPrev(self):
        """
        search for the previous word of the list
        :return:
        """
        txt = self.txtSearch.text()
        self.editor.onSearchPrevious(txt)

    def searchNext(self):
        """
        search for the next word of the list
        :return:
        """
        txt = self.txtSearch.text()
        self.editor.onSearchNext(txt)

    def replace(self):
        """
        replace the selected text with the text in the replace box
        onReplaceText(self, _type, text, newText):
        :return:
        """
        _type = "single"
        text = self.txtSearch.text()
        newText = self.txtReplace.text()
        print(_type, text, newText)
        self.editor.onReplaceText(_type, text, newText)

    def replaceAll(self):
        """
        replace all the text in the editor with the text in the replace box
        :return:
        """
        _type = "all"
        text = self.txtSearch.text()
        newText = self.txtReplace.text()
        self.editor.onReplaceText(_type, text, newText)

    def showEvent(self, event):
        self.txtSearch.setFocus()
        self.txtSearch.selectAll()
        super().showEvent(event)
