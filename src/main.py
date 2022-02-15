import sys
from game import gui as game
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)
gui = QtWidgets.QMainWindow()
ui = game.Game()
ui.setup_ui(gui, print_configs=False)
gui.show()
sys.exit(app.exec_())
