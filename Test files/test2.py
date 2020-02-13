"""
Test Qt Frameless Window resizing with QSizeGrip
Maxwell Grady, September 2017.
"""
import sys
from PyQt5 import QtCore, QtWidgets
from qtmodern.styles import dark
from qtmodern.windows import ModernWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    dark(app)  # qtmodern

    window = QtWidgets.QWidget()

    # if you are not using qtmodern darkstyle, you can still make the QWidget resizeable and frameless by uncommenting the code below then commenting out the qtmodern code

    # flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
    # window.setWindowFlags(flags)
    window.setGeometry(QtCore.QRect(300, 300, 640, 480))  # arbitrary size/location

    layout = QtWidgets.QVBoxLayout()
    sizegrip = QtWidgets.QSizeGrip(window)
    layout.addWidget(sizegrip, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
    window.setLayout(layout)

    mw = ModernWindow(window)  # qtmodern
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()