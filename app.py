import sys
from PyQt5.QtWidgets import QApplication
from main_menu import MainPage

def main():
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()