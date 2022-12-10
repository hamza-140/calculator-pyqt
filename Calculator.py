from functools import partial
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
from PyQt6 import QtGui
from PyQt6.QtGui import QFont


class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.ResultsBar()
        self.Buttons()
        

    def ResultsBar(self):
        self.line = QLineEdit()
        self.line.setStyleSheet("background-color:#FFF7E9")
        self.line.setReadOnly(True)
        self.line.setFixedHeight(35)
        self.line.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.line)
        self.setLayout(self.layout)

    def Buttons(self):
        self.buttonLayout = QGridLayout()
        self.buttonMap = {}
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "💡", ".", "+", "="],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(40, 40)
                self.buttonMap[key].setStyleSheet("background-color:#FF7000;color:#fff")
                self.buttonMap[key].setToolTip(
                    '💡')
                self.buttonLayout.addWidget(self.buttonMap[key], row, col)
        self.layout.addLayout(self.buttonLayout)


    def setDisplay(self, text):
        self.line.setText(text)
        self.line.setFocus()

    def DisplayText(self):
        return self.line.text()

    def clearDisplay(self):
        self.setDisplay("")


def values(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = "Syntax ERROR"
    return result


class Calculation:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connect()

    def _calcResults(self):
        result = self._evaluate(expression=self._view.DisplayText())
        self._view.setDisplay(result)

    def idea(self):
        dialog = QMessageBox()
        dialog.setText("<i> Welcome to My Calculator. This is basic functionality Calculator which allows a user to select multiple expression from on-screen keyboard which is really cool. <br> Press Following Buttons will allow you : <br>' + ' for Addition <br>' + ' for Addition<br>' - ' for Subtraction<br>' * ' for Multiplication<br>' / ' for Division<br>' C ' for Clear </i>")
        dialog.setWindowTitle("My Calculator")
        dialog.exec()

    def _buildExpression(self, subExpression):
        if self._view.DisplayText() == "Syntax ERROR":
            self._view.clearDisplay()
        expression = self._view.DisplayText() + subExpression
        self._view.setDisplay(expression)

    def _connect(self):
        for key, button in self._view.buttonMap.items():
            if key not in {"=", "C", "💡"}:
                button.clicked.connect(partial(self._buildExpression, key))
        self._view.buttonMap["="].clicked.connect(self._calcResults)
        self._view.line.returnPressed.connect(self._calcResults)
        self._view.buttonMap["C"].clicked.connect(self._view.clearDisplay)
        self._view.buttonMap["💡"].clicked.connect(self.idea)


app = QApplication([])
main = MyMainWindow()
main.setFixedSize(300, 300)
app.setWindowIcon(QtGui.QIcon('logo.png'))
main.setWindowTitle("Calculator")
main.setStyleSheet("background-color:#10A19D")
main.show()
Calculation(model=values, view=main)
sys.exit(app.exec())
