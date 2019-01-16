# -*- coding=utf-8 -*-

import PySide2
import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui
import mywidget as ui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World")
        # self.text.setAlignment(QtCore.Qt.)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText(random.choice(self.hello))

    def test():
        print(PySide2.__version__)
        print(PySide2.__version_info__)


class MyMainWindow(QtWidgets.QWidget, ui.Ui_mywidget):
    def __init__(self, parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = MyMainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())