import sys

from PyQt5.QtWidgets import QApplication

from gui import Window


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
