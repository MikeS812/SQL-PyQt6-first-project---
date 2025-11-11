import os
import sqlite3
import sys
import fnmatch

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from FileLoader import FileOpen
from Settings import Set


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('YandexPres.ui', self)
        self.run()
        self.theme()
        self.SetBtn.clicked.connect(self.sets)
        self.off.clicked.connect(self.off1)
        self.dobBtn.clicked.connect(self.addfunc)
        self.delbut.clicked.connect(self.delfunc)
        self.zachBtn.clicked.connect(self.dobav)
        self.rBtn.clicked.connect(self.open_file)

    def open_file(self):
        self.text_viewer = FileOpen()
        self.text_viewer.show()

    def addfunc(self):
        result2 = self.cursor.execute("SELECT * FROM Ученики").fetchall()

        try:
            fio = self.fio.text().strip()
            number = self.nymber.text()
            course = self.course.text().strip()

            if not fio and not number and not course:
                QMessageBox.warning(self, "Ошибка", "Вы ничего не ввели!")
                return

            if not fnmatch.fnmatch(str(number), "*-???-???-??-??"):
                QMessageBox.warning(self, "Ошибка", "Номер должен быть формата +7/8-???-???-??-??")
                return

            if not fio:
                QMessageBox.warning(self, "Ошибка", "Введите Ф.И.О!")
                return

            if not number:
                QMessageBox.warning(self, "Ошибка", "Введите номер!")
                return

            if not course:
                QMessageBox.warning(self, "Ошибка", "Введите курс!")
                return
            try:
                course_int = int(course)
                if True == 1 <= course_int <= 4:
                    pass
                else:
                    QMessageBox.warning(self, "Ошибка", "Курс должен быть в диапазоне 1-4")
                    return
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Курс должен быть числом!")
                return

            sp = self.cursor.execute(f"SELECT Номер FROM Ученики WHERE Номер = '{str(number)}'").fetchall()
            if len(sp) != 0:
                QMessageBox.warning(self, "Ошибка", "Данный номер уже есть!")
                return

            self.cursor.execute(f'''
                INSERT INTO Ученики (ID, "Ф.И.О", Номер, Факультет, Курс)
                VALUES ('{len(result2) + 1}', '{fio}', '{number}', 'Механика', '{course_int}')
            ''')
            for i in range(1, 4):
                self.cursor.execute(f'''
                                INSERT INTO [{i}Триместр] (ID, [Ф.И.О],Номер)
                                VALUES ('{len(result2) + 1}', '{fio}', '{number}')
                            ''')
            self.conn.commit()
            self.clear()
            self.run()

            QMessageBox.information(self, "Успех", "Ученик добавлен!")

        except Exception:
            QMessageBox.critical(self, "Ошибка", f"Упс, попробуйте еще раз")

    def delfunc(self):
        try:
            del_x = self.comboBox.currentText()
            del_l = self.delLine.text().strip()
            del_p = self.prichLine.text().strip()

            if del_x == "Ф.И.О":
                if not del_l:
                    QMessageBox.warning(self, "Ошибка", "Введите Имя!")
                    return

            else:
                if not del_l:
                    QMessageBox.warning(self, "Ошибка", "Введите Номер!")
                    return

            if not del_p:
                QMessageBox.information(self, "Подтверждение", "Вы не ввели причину.")
                return

        except Exception:
            QMessageBox.critical(self, "Ошибка", f"Упс, попробуйте еще раз")

        if del_x == "Ф.И.О":
            sp = self.cursor.execute(f"SELECT [Ф.И.О] FROM Ученики WHERE [Ф.И.О] = '{str(del_l)}'").fetchall()
            if len(sp) > 1:
                QMessageBox.warning(self, "Ошибка", "Учеников с такими инициалами несколько удалите ученика по номеру")
                return
            self.cursor.execute(f"""DELETE FROM Ученики
                       WHERE "Ф.И.О" = '{del_l}'""")
            for i in range(1, 4):
                self.cursor.execute(f"""DELETE FROM [{i}Триместр]
                       WHERE "Ф.И.О" = '{del_l}'""")
        else:
            self.cursor.execute(f"""DELETE FROM Ученики
                       WHERE Номер = '{del_l}'""")
            for i in range(1, 4):
                self.cursor.execute(f"""DELETE FROM [{i}Триместр]
                       WHERE Номер = '{del_l}'""")

        if self.cursor.rowcount != 0:
            QMessageBox.information(self, "Успех", "Ученик удален!")
        else:
            QMessageBox.warning(self, "Ошибка", "Ученик не найден!")

        self.conn.commit()
        self.delLine.clear()
        self.prichLine.clear()
        self.run()

    def off1(self):
        r = QMessageBox.question(self, "Предупреждение",
                                 "Уверены что хотите закрыть программу?",
                                 QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)

        if r == QMessageBox.StandardButton.Ok:
            exit(0)

    def clear(self):
        self.fio.clear()
        self.nymber.clear()
        self.course.clear()

    def run(self):
        self.conn = sqlite3.connect("Teen_db.sqlite")
        self.cursor = self.conn.cursor()

        result = self.cursor.execute("SELECT * FROM Ученики").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Ф.И.О', 'Номер', 'Факультет', 'Курс'])
        for row_num, row_data in enumerate(result):
            for col_num, data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        # 1трим
        result = self.cursor.execute("SELECT * FROM [1Триместр]").fetchall()
        self.tableWidget_2.setRowCount(len(result))
        self.tableWidget_2.setColumnCount(len(result[0]))
        self.tableWidget_2.setHorizontalHeaderLabels(['ID', 'Ф.И.О', 'Номер', 'Физика', 'Математика', 'Информатика'])
        for row_num, row_data in enumerate(result):
            for col_num, data in enumerate(row_data):
                self.tableWidget_2.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        # 2трим
        result = self.cursor.execute("SELECT * FROM [2Триместр]").fetchall()
        self.tableWidget_3.setRowCount(len(result))
        self.tableWidget_3.setColumnCount(len(result[0]))
        self.tableWidget_3.setHorizontalHeaderLabels(['ID', 'Ф.И.О', 'Номер', 'Физика', 'Математика', 'Информатика'])
        for row_num, row_data in enumerate(result):
            for col_num, data in enumerate(row_data):
                self.tableWidget_3.setItem(row_num, col_num, QTableWidgetItem(str(data)))
        # 3трим
        result = self.cursor.execute("SELECT * FROM [3Триместр]").fetchall()
        self.tableWidget_4.setRowCount(len(result))
        self.tableWidget_4.setColumnCount(len(result[0]))
        self.tableWidget_4.setHorizontalHeaderLabels(['ID', 'Ф.И.О', 'Номер', 'Физика', 'Математика', 'Информатика'])
        for row_num, row_data in enumerate(result):
            for col_num, data in enumerate(row_data):
                self.tableWidget_4.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def dobav(self):
        v_l = self.comboBox_2.currentText()
        v_trim = self.comboBox_3.currentText()
        v_pred = self.comboBox_4.currentText()

        if self.radioButton.isChecked():
            v_z = "Зачет"
        else:
            v_z = "Незачет"

        try:
            v_index = self.indexLine.text()
            if v_l == "Ф.И.О":
                if not v_index:
                    QMessageBox.information(self, "Подтверждение", "Вы не ввели Ф.И.О.")
                    return
            else:
                if not v_index:
                    QMessageBox.information(self, "Подтверждение", "Вы не ввели Номер.")
                    return
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Упс, попробуйте еще раз {str(e)}")
            return

        sp = self.cursor.execute(f"SELECT [Ф.И.О] FROM Ученики WHERE [Ф.И.О] = '{str(v_index)}'").fetchall()
        if len(sp) > 1:
            QMessageBox.warning(self, "Ошибка", "Учеников с такими инициалами несколько. Выставте зачет по номеру")
            return

        if v_l == "Ф.И.О":
            self.cursor.execute(f'''UPDATE [{v_trim}Триместр] SET {v_pred} = '{v_z}' WHERE [Ф.И.О] = '{v_index}' ''')
        else:
            self.cursor.execute(f'''UPDATE [{v_trim}Триместр] SET {v_pred} = '{v_z}' WHERE Номер = '{v_index}' ''')

        if self.cursor.rowcount != 0:
            QMessageBox.information(self, "Успех", "Зачет выставлен!")
        else:
            QMessageBox.warning(self, "Ошибка", "Ученик не найден!")

        self.conn.commit()
        self.clear()
        self.run()

    def theme(self):
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
        self.setStyleSheet(self.tema)

    def sets(self):
        self.sett = Set(mn=self)
        self.sett.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
