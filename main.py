import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

class Main(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.filename = ""
        self.initUI()

    def initToolbar(self):
        self.toolbar = self.addToolBar("Options")

        self.newAction = QtGui.QAction(QtGui.QIcon("icons/new.png"), "New", self)
        self.newAction.setStatusTip("Create a New Document")
        self.newAction.setShortcut("Ctrl + N")
        self.newAction.triggered.connect(self.new)

        self.openAction = QtGui.QAction(QtGui.QIcon("icons/open.png"), "Open", self)
        self.openAction.setStatusTip("Open Document")
        self.openAction.setShortcut("Ctrl + O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QtGui.QAction(QtGui.QIcon("icons/save.png"), "Save", self)
        self.saveAction.setStatusTip("Save Document")
        self.saveAction.setShortcut("Ctrl + S")
        self.saveAction.triggered.connect(self.save)

        self.printAction = QtGui.QAction(QtGui.QIcon("icons/print.png"), "Print Document", self)
        self.printAction.setStatusTip("Print Document")
        self.printAction.setShortcut("Ctrl + P")
        self.printAction.triggered.connect(self.print)

        self.previewAction = QtGui.QAction(QtGui.QIcon("icons/preview.png"), "Page View", self)
        self.previewAction.setStatusTip("Print preview Document")
        self.previewAction.setShortcut("Ctrl + Shift + P")
        self.previewAction.triggered.connect(self.preview)

        self.toolbar.addSeparator()

        self.cutAction = QtGui.QAction(QtGui.QIcon("icons/cut.png"), "Cut to Clipboard", self)
        self.cutAction.setStatusTip("Delete and copy text to clipboard")
        self.cutAction.setShortcut("Ctrl + X")
        self.cutAction.triggered.connect(self.text.cut)

        self.copyAction = QtGui.QAction(QtGui.QIcon("icons/copy.png"), "Copy to clipboard", self)
        self.copyAction.setStatusTip("Copy text to Clipboard")
        self.copyAction.setShortcut("Ctrl + C")
        self.copyAction.triggered.connect(self.text.copy)

        self.pasteAction = QtGui.QAction(QtGui.QIcon("icons/paste.png"), "Paste from clipboard", self)
        self.pasteAction.setStatusTip("Paste text from clipboard")
        self.pasteAction.setShortcut("Ctrl + V")
        self.pasteAction.triggered.connect(self.text.paste)

        self.undoAction = QtGui.QAction(QtGui.QIcon("icons/undo.png"), "Undo last action", self)
        self.undoAction.setStatusTip("Undo last action")
        self.undoAction.setShortcut("Ctrl + Z")
        self.undoAction.triggered.connect(self.text.undo)

        self.redoAction = QtGui.QAction(QtGui.QIcon("icons/redo.png"), "Redo last undone action", self)
        self.redoAction.setStatusTip("Redo last undone action")
        self.redoAction.setShortcut("Ctrl + Y")
        self.redoAction.triggered.connect(self.text.redo)

        self.bulletAction = QtGui.QAction(QtGui.QIcon("icons/bullet.png"), "Insert bullet list", self)
        self.bulletAction.setStatusTip("Insert bullet list")
        self.bulletAction.setShortcut("Ctrl + Shift + B")
        self.bulletAction.triggered.connect(self.bulletList)

        self.numberedAction = QtGui.QAction(QtGui.QIcon("icons/number.png"), "Insert numbered list", self)
        self.numberedAction.setStatusTip("Insert numbered list")
        self.numberedAction.setShortcut("Ctrl + Shift + L")
        self.numberedAction.triggered.connect(self.numberList)
        
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)

        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)

        self.toolbar.addAction(self.bulletAction)
        self.toolbar.addAction(self.numberedAction)

        self.toolbar.addSeparator()
        # Next toolbar add below this one
        self.addToolBarBreak()
        
    def initFormatbar(self):
        fontBox = QtGui.QFontComboBox(self)
        fontBox.currentFontChanged.connect(self.fontFamily)

        fontSize = QtGui.QComboBox(self)
        fontSize.setEditable(True)

        # Minimum number of chars displayed
        fontSize.setMinimumContentsLength(3)
        fontSize.activated.connect(self.fontSize)

        # Normal font sizes
        fontSizes = ['6','7','8','9','10','11','12','13','14',
             '15','16','18','20','22','24','26','28',
             '32','36','40','44','48','54','60','66',
             '72','80','88','96']

        for i in fontSizes:
            fontSize.addItem(i)
        
        fontColor = QtGui.QAction(QtGui.QIcon("icons/font-color.png"), "Change font color", self)
        fontColor.triggered.connect(self.fontColor)

        backColor = QtGui.QAction(QtGui.QIcon("icons/highlight.png"), "Change background color", self)
        backColor.triggered.connect(self.highlight)

        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)
        self.formatbar.addSeparator()

        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)
        self.formatbar.addSeparator()

    def initMenubar(self):
        menubar = self.menuBar()

        file = menubar.addMenu("File")
        file.addAction(self.newAction)
        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.printAction)
        file.addAction(self.previewAction)

        edit = menubar.addMenu("Edit")
        edit.addAction(self.undoAction)
        edit.addAction(self.redoAction)
        edit.addAction(self.cutAction)
        edit.addAction(self.copyAction)
        edit.addAction(self.pasteAction)

        view = menubar.addMenu("View")
    
    def new(self):
        spawn = Main(self)
        spawn.show()

    def open(self):
        # get file name and only show wrt files
        self.filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', ".", "(*.wrt)")

        if self.filename:
            with open(self.filename, "rt") as file:
                self.text.setText(file.read())

    def save(self):
        # show dialog if not previously saved
        if not self.filename:
            self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')

        # Append extension
        if not self.filename.endswith(".wtr"):
            self.filename += ".wrt"

        # We store the contents of the file in html format
        with open(self.filename, "wt") as file:
            file.write(self.text.toHtml())

    def print(self):
        dialog = QtGui.QPrintDialog()

        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.text.document().print_(dialog.printer())

    def preview(self):
        preview = QtGui.QPrintPreviewDialog()

        # If a print is requested, open print dialog
        preview.paintRequested.connect(lambda p: self.text.print_(p))
        preview.exec_()

    def bulletList(self):
        cursor = self.text.textCursor()

        cursor.insertList(QtGui.QTextListFormat.ListDisc)
        
    def numberList(self):
        cursor = self.text.textCursor()

        cursor.insertList(QtGui.QTextListFormat.ListDecimal)

    def cursorPosition(self):
        cursor = self.text.textCursor()

        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.statusbar.showMessage("Line: {} | Column: {}".format(line, col))

    def fontFamily(self, font):
        self.text.setCurrentFont(font)

    def fontSize(self, size):
        self.text.setFontPointSize(int(size))

    def fontColor(self):
        color = QtGui.QColorDialog.getColor()
        self.text.setTextColor(color)

    def highlight(self):
        color = QtGui.QColorDialog.getColor()
        self.text.setTextBackgroundColor(color)

    def initUI(self):
        self.text = QtGui.QTextEdit(self)
        self.text.setTabStopWidth(33)
        self.text.cursorPositionChanged.connect(self.cursorPosition)
        self.setCentralWidget(self.text)

        self.initToolbar()
        self.initFormatbar()
        self.initMenubar()

        # Add Status bar
        self.statusbar = self.statusBar()

        self.setGeometry(100,100,1200,800)
        self.setWindowTitle("Text Editor")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))


def main():
    app = QtGui.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
