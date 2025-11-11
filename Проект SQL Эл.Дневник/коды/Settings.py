import sys

from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import uic
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

class Set(QWidget):
    def __init__(self, mn=None):
        super().__init__()
        uic.loadUi('YandexTool.ui', self)
        self.mn = mn
        self.pushButton_4.clicked.connect(self.theme2)
        self.vostBtn.clicked.connect(self.vostFunc)

    def theme2(self):
        self.tema = """
                QMainWindow, QWidget {
                    background-color: #2b2b2b;
                    color: white;
                }
                QPushButton {
                    background-color: #404040;
                    color: white;
                    border: 1px solid #555;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
                QLineEdit, QComboBox {
                    background-color: #404040;
                    color: white;
                    border: 1px solid #555;
                    padding: 5px;
                }
                QTableWidget {
                    background-color: #2b2b2b;
                    color: white;
                    gridline-color: #555;
                }
                QHeaderView::section {
                    background-color: #404040;
                    color: white;
                    padding: 5px;
                    border: 1px solid #555;
                }
                QTabWidget::pane {
                    border: 1px solid #555;
                    background-color: #2b2b2b;
                }
                QTabBar::tab {
                    background-color: #404040;
                    color: white;
                    padding: 8px 16px;
                    border: 1px solid #555;
                }
                QTabBar::tab:selected {
                    background-color: #2b2b2b;
                    border-bottom: none;
                }
                """
        if not self.radioButton_2.isChecked() and not self.radioButton_3.isChecked():
            self.mn.setStyleSheet(self.tema)
        if self.radioButton_2.isChecked():
            self.mn.setStyleSheet(self.tema)
        if self.radioButton_3.isChecked():
            self.mn.setStyleSheet("""
                    QMainWindow, QWidget {
                        background-color: white;
                        color: black;
                    }
                    QPushButton {
                        background-color: #f0f0f0;
                        color: black;
                        border: 1px solid #ccc;
                        padding: 5px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                    QLineEdit, QComboBox {
                        background-color: white;
                        color: black;
                        border: 1px solid #ccc;
                        padding: 5px;
                    }
                    QTableWidget {
                        background-color: white;
                        color: black;
                        gridline-color: #ccc;
                    }
                    QHeaderView::section {
                        background-color: #f0f0f0;
                        color: black;
                        padding: 5px;
                        border: 1px solid #ccc;
                    }
                    QTabWidget::pane {
                        border: 1px solid #ccc;
                        background-color: white;
                    }
                    QTabBar::tab {
                        background-color: #f0f0f0;
                        color: black;
                        padding: 8px 16px;
                        border: 1px solid #ccc;
                    }
                    QTabBar::tab:selected {
                        background-color: white;
                        border-bottom: none;
                    }
                """)
    def vostFunc(self):
        QDesktopServices.openUrl(QUrl("https://disk.yandex.ru/d/hxMiiP0WLoAMjQ"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Set()
    window.show()
    sys.exit(app.exec())