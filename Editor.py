#!/usr/local/bin/env python3.5
# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import QFile, Qt, QTextStream
from PyQt5.QtGui import (QFont, QIcon, QKeySequence)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMenuBar,
                             QMessageBox, QStyleFactory, QTextEdit)

import dependencies.pytib as pytib
from dependencies import highlighter
from dependencies.pytib.common import open_file

this_dir = os.path.split(__file__)[0]
lists_path = os.path.join(this_dir, 'ཚིག་གི་མཐོ་རིམ།')
file_new_path = os.path.join(this_dir, 'ཉེར་མཁོ་ཡིག་ཆ།', 'འབྲི་དེབ་སྙི་ཆས་ལ་མཁོ་བ།', 'imgs', 'filenew.png')
file_open_path = os.path.join(this_dir, 'ཉེར་མཁོ་ཡིག་ཆ།', 'འབྲི་དེབ་སྙི་ཆས་ལ་མཁོ་བ།', 'imgs', 'fileopen.png')
file_save_path = os.path.join(this_dir, 'ཉེར་མཁོ་ཡིག་ཆ།', 'འབྲི་དེབ་སྙི་ཆས་ལ་མཁོ་བ།', 'imgs', 'filesave.png')
edit_undo_path = os.path.join(this_dir, 'ཉེར་མཁོ་ཡིག་ཆ།', 'འབྲི་དེབ་སྙི་ཆས་ལ་མཁོ་བ།', 'imgs', 'editundo.png')
edit_redo_path = os.path.join(this_dir, 'ཉེར་མཁོ་ཡིག་ཆ།', 'འབྲི་དེབ་སྙི་ཆས་ལ་མཁོ་བ།', 'imgs', 'editredo.png')
segment_path = os.path.join(this_dir, 'ཉེར་མཁོ་ཡིག་ཆ།', 'འབྲི་དེབ་སྙི་ཆས་ལ་མཁོ་བ།', 'imgs', 'segment.png')


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

# Editor
    def setupEditor(self):
        font = QFont()
        font.setFamily('Noto Sans Tibetan')
        font.setFixedPitch(True)
        font.setPointSize(18)

        self.editor = QTextEdit()
        self.editor.setFont(font)

        self.highlighter = highlighter.Highlighter(
            self.editor.document(), self.levelLists)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createToolbar(self):
        self.toolbar = self.addToolBar("toolbar")
        self.toolbar.addAction(self.newFileAction)
        self.toolbar.addAction(self.openFileAction)
        self.toolbar.addAction(self.saveFileAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.segmentAction)

    def createMenus(self):
        self.menu = self.menuBar()
        # File
        fileMenu = self.menu.addMenu("&File")
        fileMenu.addAction(self.newFileAction)
        fileMenu.addAction(self.openFileAction)
        fileMenu.addAction(self.saveFileAction)
        fileMenu.addAction(self.actionQuit)
        # Edit
        editMenu = self.menu.addMenu("&Edit")
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addAction("About &Qt", QApplication.instance().aboutQt)
        # Tools
        self.viewMenu = self.menu.addMenu("&View")
        self.viewMenu.addAction(self.segmentAction)
        self.viewMenu.addAction(
            "&Spellchecker", QApplication.instance().aboutQt)
        self.viewMenu.addAction("&Highlighter", self.about)
        # Settings
        settingsMenu = self.menu.addMenu("&Help")
        settingsMenu.addAction("&Highlighter", self.about)

        self.menuBarRight = QMenuBar(self.menu)
        self.menu.setCornerWidget(self.menuBarRight, Qt.TopRightCorner)

    def initUI(self):
        self.createActions()
        self.createMenus()
        self.createToolbar()
        self.loadLists()
        self.setupEditor()
        self.createStatusBar()
        self.setCentralWidget(self.editor)
        self.setWindowTitle("TibEdit")
        self.setWindowIcon(QIcon("tab1.png"))
        self.setWindowState(Qt.WindowMaximized)
        self.resize(1200, 480)

# Actions
    def about(self):
        QMessageBox.about(self, "About PyTib Editor",
                          "rules using regular expressions.</p>")

    def newFile(self):
        self.editor.clear()

    def openFile(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
                                                  "UTF-8 files (*.txt)")

        if path:
            inFile = QFile(path)
            if inFile.open(QFile.ReadOnly | QFile.Text):
                text = inFile.readAll()

                try:
                    text = str(text, encoding="UTF-8")
                    print("try")
                except:
                    print("except")
                self.editor.setPlainText(text)

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self,
                                                  "Choose a file name", '.', "UTF-8 (*.txt)")
        if not filename:
            return

        file = QFile(filename+'.txt')
        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "Dock Widgets",
                                "Cannot write file %s:\n%s." % (filename, file.errorString()))
            return

        out = QTextStream(file)
        out.setCodec("UTF-8")
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.editor.toPlainText()
        QApplication.restoreOverrideCursor()

        self.statusBar().showMessage("Saved '%s'" % filename, 2000)

    def undo(self):
        document = self.editor.document()
        document.undo()

    def redo(self):
        document = self.editor.document()
        document.redo()

    def segment(self):
        self.statusBar().showMessage("Segmenting text...", 1000)
        seg = pytib.Segment()
        seg.include_user_vocab()
        file1 = self.editor.toPlainText()
        cut_text = seg.segment(file1)
        self.editor.setPlainText(cut_text)
        self.editor.document().setModified(True)

    def createActions(self):
        self.newFileAction = QAction(QIcon(file_new_path), "&New...",
                                     self, shortcut=QKeySequence.New,
                                     statusTip="Create a new file", triggered=self.newFile)
        self.openFileAction = QAction(QIcon(file_open_path), "&Open...",
                                      self, shortcut=QKeySequence.Open,
                                      statusTip="Open a text file", triggered=self.openFile)
        self.saveFileAction = QAction(QIcon(file_save_path), "&Save...", self,
                                      shortcut=QKeySequence.Save,
                                      statusTip="Save the current document", triggered=self.saveFile)
        self.undoAction = QAction(QIcon(edit_undo_path), "&Undo", self,
                                  shortcut=QKeySequence.Undo,
                                  statusTip="Undo the last editing action", triggered=self.undo)
        self.redoAction = QAction(QIcon(edit_redo_path), "&Redo", self,
                                  shortcut=QKeySequence.Redo,
                                  statusTip="Redo the last editing action", triggered=self.redo)
        self.segmentAction = QAction(QIcon(segment_path), "&Segment", self,
                                     shortcut="Ctrl+Shift+C",
                                     statusTip="Segment the current document", triggered=self.segment)
        self.actionQuit = QAction("&Quit", self, shortcut="Ctrl+Q",
                                  triggered=self.close)

# Get Lists
# TODO: get the level files in the Levels folder, read their names,
# convert their content into a list of regexes and create a dict for
# highlighter.py. A spaces should be added before and after each list
# entry so they can only be discovered after segmentation.

    def loadLists(self):
        self.levelLists = {}
        for level in os.listdir(lists_path):
            level_name = level.replace('.txt', '')
            raw_list = open_file(os.path.join(lists_path, level)).strip().split('\n')
            self.levelLists[level_name] = []
            for word in raw_list:
                # add a tsek where missing
                if not word.endswith('་'):
                    word += '་'
                # format as needed
                formated_word = '^{0}?\\s|\\s{0}?\\s|\\s{0}?$'.format(word)
                self.levelLists[level_name].append(formated_word)
        return self.levelLists

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
