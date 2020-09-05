from PyQt5 import QtCore, QtWidgets
from bin.text_audio import TextAudio
import sys

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = TextAudio()
    ui.show()
    sys.exit(app.exec_())
