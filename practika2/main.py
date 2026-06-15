# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from form2 import Ui_Widget2
from podcluch import Connection

class Widget2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget2()
        self.ui.setupUi(self)
        self.connect = Connection()
        self.ui.exit.clicked.connect(self.exit)
        self.ui.comboBox.currentTextChanged.connect(self.on_combo_changed)
        self.ui.pushButton_4.clicked.connect(self.poisk)
        self.current_index = 0
        self.pokazat_sotrudniki()

    def on_combo_changed(self, text):
        if text == "Сотрудники":
            self.current_index = 0
            self.pokazat_sotrudniki()
        elif text == "История должностей":
            self.current_index = 1
            self.pokazat_istoriyu()
        elif text == "Подразделения":
            self.current_index = 2
            self.pokazat_podrazdeleniya()
        elif text == "Помещения":
            self.current_index = 3
            self.pokazat_pomeshcheniya()

    def poisk(self):
        #Поиск по таблице
        search_text = self.ui.lineEdit.text().strip()
        if self.current_index == 0:
            self.pokazat_sotrudniki(search_text)
        elif self.current_index == 1:
            self.pokazat_istoriyu(search_text)
        elif self.current_index == 2:
            self.pokazat_podrazdeleniya(search_text)
        elif self.current_index == 3:
            self.pokazat_pomeshcheniya(search_text)

    def pokazat_sotrudniki(self, search_text=""):
        if search_text:
            self.connect.cur.execute("""
                SELECT 
                    s.fio AS "ФИО",
                    d.nazvanie_dolzhnosti AS "Должность",
                    p.nazvanie_podrazdeleniya AS "Подразделение",
                    COALESCE(pm.nomer_pomeshcheniya, '—') AS "Помещение"
                FROM sotrudniki s
                JOIN dolzhnosti d ON s.id_dolzhnosti = d.id_dolzhnosti
                JOIN podrazdeleniya p ON s.id_podrazdeleniya = p.id_podrazdeleniya
                LEFT JOIN pomeshcheniya pm ON s.id_pomeshcheniya = pm.id_pomeshcheniya
                WHERE s.fio ILIKE %s
                ORDER BY s.fio""", (f"%{search_text}%",))
        else:
            self.connect.cur.execute("""
                SELECT 
                    s.fio AS "ФИО",
                    d.nazvanie_dolzhnosti AS "Должность",
                    p.nazvanie_podrazdeleniya AS "Подразделение",
                    COALESCE(pm.nomer_pomeshcheniya, '—') AS "Помещение"
                FROM sotrudniki s
                JOIN dolzhnosti d ON s.id_dolzhnosti = d.id_dolzhnosti
                JOIN podrazdeleniya p ON s.id_podrazdeleniya = p.id_podrazdeleniya
                LEFT JOIN pomeshcheniya pm ON s.id_pomeshcheniya = pm.id_pomeshcheniya
                ORDER BY s.fio""")
        headers = [desc[0] for desc in self.connect.cur.description]
        data = self.connect.cur.fetchall()
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ui.tableWidget.setItem(row_num, col_num, item)
        self.ui.tableWidget.resizeColumnsToContents()

    def pokazat_istoriyu(self, search_text=""):
        if search_text:
            self.connect.cur.execute("""
                SELECT 
                    s.fio AS "ФИО",
                    COALESCE(h.staraya_dolzhnost, '—') AS "Старая должность",
                    h.novaya_dolzhnost AS "Новая должность",
                    TO_CHAR(h.data_smeny, 'DD.MM.YYYY') AS "Дата смены"
                FROM istoriya_dolzhnostey h
                JOIN sotrudniki s ON h.id_sotrudnika = s.id_sotrudnika
                WHERE s.fio ILIKE %s
                ORDER BY h.data_smeny DESC""", (f"%{search_text}%",))
        else:
            self.connect.cur.execute("""
                SELECT 
                    s.fio AS "ФИО",
                    COALESCE(h.staraya_dolzhnost, '—') AS "Старая должность",
                    h.novaya_dolzhnost AS "Новая должность",
                    TO_CHAR(h.data_smeny, 'DD.MM.YYYY') AS "Дата смены"
                FROM istoriya_dolzhnostey h
                JOIN sotrudniki s ON h.id_sotrudnika = s.id_sotrudnika
                ORDER BY h.data_smeny DESC""")
        headers = [desc[0] for desc in self.connect.cur.description]
        data = self.connect.cur.fetchall()
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ui.tableWidget.setItem(row_num, col_num, item)
        self.ui.tableWidget.resizeColumnsToContents()

    def pokazat_podrazdeleniya(self, search_text=""):
        if search_text:
            self.connect.cur.execute("""
                SELECT 
                    nazvanie_podrazdeleniya AS "Подразделение",
                    COALESCE(kod_podrazdeleniya, '—') AS "Код"
                FROM podrazdeleniya
                WHERE nazvanie_podrazdeleniya ILIKE %s
                ORDER BY nazvanie_podrazdeleniya""", (f"%{search_text}%",))
        else:
            self.connect.cur.execute("""
                SELECT 
                    nazvanie_podrazdeleniya AS "Подразделение",
                    COALESCE(kod_podrazdeleniya, '—') AS "Код"
                FROM podrazdeleniya
                ORDER BY nazvanie_podrazdeleniya""")
        headers = [desc[0] for desc in self.connect.cur.description]
        data = self.connect.cur.fetchall()
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ui.tableWidget.setItem(row_num, col_num, item)
        self.ui.tableWidget.resizeColumnsToContents()

    def pokazat_pomeshcheniya(self, search_text=""):
        if search_text:
            self.connect.cur.execute("""
                SELECT 
                    pm.nomer_pomeshcheniya AS "Помещение",
                    p.nazvanie_podrazdeleniya AS "Подразделение",
                    pm.vmestimost AS "Вместимость"
                FROM pomeshcheniya pm
                JOIN podrazdeleniya p ON pm.id_podrazdeleniya = p.id_podrazdeleniya
                WHERE pm.nomer_pomeshcheniya ILIKE %s
                ORDER BY pm.nomer_pomeshcheniya""", (f"%{search_text}%",))
        else:
            self.connect.cur.execute("""
                SELECT 
                    pm.nomer_pomeshcheniya AS "Помещение",
                    p.nazvanie_podrazdeleniya AS "Подразделение",
                    pm.vmestimost AS "Вместимость"
                FROM pomeshcheniya pm
                JOIN podrazdeleniya p ON pm.id_podrazdeleniya = p.id_podrazdeleniya
                ORDER BY pm.nomer_pomeshcheniya""")
        headers = [desc[0] for desc in self.connect.cur.description]
        data = self.connect.cur.fetchall()
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ui.tableWidget.setItem(row_num, col_num, item)
        self.ui.tableWidget.resizeColumnsToContents()

    def exit(self):
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget2()
    widget.show()
    sys.exit(app.exec())


