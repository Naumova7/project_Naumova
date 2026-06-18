# This Python file uses the following encoding: utf-8
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt, QEvent
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
        self.ui.exit.clicked.connect(self.close_app)
        self.ui.comboBox.currentTextChanged.connect(self.on_combo_changed)
        self.ui.pushButton_4.clicked.connect(self.poisk)
        self.ui.add.clicked.connect(self.dobavit)
        self.ui.izm.clicked.connect(self.izmenit)
        self.ui.tableWidget.installEventFilter(self)
        self.current_index = 0
        self.pokazat_sotrudniki()

    def eventFilter(self, obj, event):
        return self.obrabotat_enter(obj, event)

    def obrabotat_enter(self, obj, event):
        if obj == self.ui.tableWidget and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                row = self.ui.tableWidget.currentRow()
                if row == self.ui.tableWidget.rowCount() - 1:
                    self.dobavit()
                    return True
        return super().eventFilter(obj, event)

    def dobavit(self):
        row = self.ui.tableWidget.rowCount() - 1
        if self.current_index == 0:
            fio_item = self.ui.tableWidget.item(row, 0)
            dolzhnost_item = self.ui.tableWidget.item(row, 1)
            podrazdelenie_item = self.ui.tableWidget.item(row, 2)
            pomeshchenie_item = self.ui.tableWidget.item(row, 3)

            if not fio_item or not fio_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните ФИО")
                return
            if not dolzhnost_item or not dolzhnost_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните должность")
                return
            if not podrazdelenie_item or not podrazdelenie_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните подразделение")
                return
            fio_text = fio_item.text()
            dolzhnost_text = dolzhnost_item.text()
            podrazdelenie_text = podrazdelenie_item.text()
            pomeshchenie_text = pomeshchenie_item.text() if pomeshchenie_item and pomeshchenie_item.text() else None
            self.connect.cur.execute("SELECT id_sotrudnika FROM sotrudniki WHERE fio = %s", (fio_text,))
            if self.connect.cur.fetchone():
                QMessageBox.warning(self, "Ошибка", f"Сотрудник '{fio_text}' уже существует")
                return
            try:
                self.connect.cur.execute("SELECT id_dolzhnosti FROM dolzhnosti WHERE nazvanie_dolzhnosti = %s",
                                         (dolzhnost_text,))
                dolzhnost_result = self.connect.cur.fetchone()
                if not dolzhnost_result:
                    self.connect.cur.execute(
                        "INSERT INTO dolzhnosti (nazvanie_dolzhnosti) VALUES (%s)",
                        (dolzhnost_text,)
                    )
                    self.connect.cur.execute("SELECT id_dolzhnosti FROM dolzhnosti WHERE nazvanie_dolzhnosti = %s",
                                             (dolzhnost_text,))
                    dolzhnost_result = self.connect.cur.fetchone()
                dolzhnost_id = dolzhnost_result[0]
                self.connect.cur.execute(
                    "SELECT id_podrazdeleniya FROM podrazdeleniya WHERE nazvanie_podrazdeleniya = %s",
                    (podrazdelenie_text,))
                podrazdelenie_result = self.connect.cur.fetchone()
                if not podrazdelenie_result:
                    self.connect.cur.execute(
                        "INSERT INTO podrazdeleniya (nazvanie_podrazdeleniya) VALUES (%s)",
                        (podrazdelenie_text,)
                    )
                    self.connect.cur.execute(
                        "SELECT id_podrazdeleniya FROM podrazdeleniya WHERE nazvanie_podrazdeleniya = %s",
                        (podrazdelenie_text,))
                    podrazdelenie_result = self.connect.cur.fetchone()
                podrazdelenie_id = podrazdelenie_result[0]
                pomeshchenie_id = None
                if pomeshchenie_text:
                    self.connect.cur.execute(
                        "SELECT id_pomeshcheniya FROM pomeshcheniya WHERE nomer_pomeshcheniya = %s",
                        (pomeshchenie_text,))
                    pomeshchenie_result = self.connect.cur.fetchone()
                    if not pomeshchenie_result:
                        self.connect.cur.execute(
                            "INSERT INTO pomeshcheniya (nomer_pomeshcheniya, id_podrazdeleniya, vmestimost) VALUES (%s, %s, 10)",
                            (pomeshchenie_text, podrazdelenie_id)
                        )
                        self.connect.cur.execute(
                            "SELECT id_pomeshcheniya FROM pomeshcheniya WHERE nomer_pomeshcheniya = %s",
                            (pomeshchenie_text,))
                        pomeshchenie_result = self.connect.cur.fetchone()
                    pomeshchenie_id = pomeshchenie_result[0]
                self.connect.cur.execute(
                    "INSERT INTO sotrudniki (fio, id_podrazdeleniya, id_dolzhnosti, id_pol, id_pomeshcheniya) VALUES (%s, %s, %s, 1, %s)",
                    (fio_text, podrazdelenie_id, dolzhnost_id, pomeshchenie_id)
                )
                self.obnovit_tablicu()
                QMessageBox.information(self, "Успех", "Сотрудник успешно добавлен")
            except Exception as e:
                self.connect.con.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить:\n{e}")
        elif self.current_index == 2:
            name_item = self.ui.tableWidget.item(row, 0)
            kod_item = self.ui.tableWidget.item(row, 1)
            if not name_item or not name_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните название подразделения")
                return
            name = name_item.text()
            kod = kod_item.text() if kod_item and kod_item.text() else None
            try:
                self.connect.cur.execute(
                    "INSERT INTO podrazdeleniya (nazvanie_podrazdeleniya, kod_podrazdeleniya) VALUES (%s, %s)",
                    (name, kod)
                )
                self.obnovit_tablicu()
                QMessageBox.information(self, "Успех", "Подразделение успешно добавлено")
            except Exception as e:
                self.connect.con.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить:\n{e}")
        elif self.current_index == 3:
            nomer_item = self.ui.tableWidget.item(row, 0)
            podrazdelenie_item = self.ui.tableWidget.item(row, 1)
            vmestimost_item = self.ui.tableWidget.item(row, 2)
            if not nomer_item or not nomer_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните номер помещения")
                return
            if not podrazdelenie_item or not podrazdelenie_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните подразделение")
                return
            if not vmestimost_item or not vmestimost_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните вместимость")
                return
            nomer = nomer_item.text()
            podrazdelenie_text = podrazdelenie_item.text()
            vmestimost = int(vmestimost_item.text())
            try:
                self.connect.cur.execute(
                    "SELECT id_podrazdeleniya FROM podrazdeleniya WHERE nazvanie_podrazdeleniya = %s",
                    (podrazdelenie_text,))
                podrazdelenie_result = self.connect.cur.fetchone()
                if not podrazdelenie_result:
                    self.connect.cur.execute(
                        "INSERT INTO podrazdeleniya (nazvanie_podrazdeleniya) VALUES (%s)",
                        (podrazdelenie_text,)
                    )
                    self.connect.cur.execute(
                        "SELECT id_podrazdeleniya FROM podrazdeleniya WHERE nazvanie_podrazdeleniya = %s",
                        (podrazdelenie_text,))
                    podrazdelenie_result = self.connect.cur.fetchone()
                podrazdelenie_id = podrazdelenie_result[0]
                self.connect.cur.execute(
                    "INSERT INTO pomeshcheniya (nomer_pomeshcheniya, id_podrazdeleniya, vmestimost) VALUES (%s, %s, %s)",
                    (nomer, podrazdelenie_id, vmestimost)
                )
                self.obnovit_tablicu()
                QMessageBox.information(self, "Успех", "Помещение успешно добавлено")
            except Exception as e:
                self.connect.con.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить:\n{e}")
        elif self.current_index == 1:
            fio_item = self.ui.tableWidget.item(row, 0)
            staraya_item = self.ui.tableWidget.item(row, 1)
            novaya_item = self.ui.tableWidget.item(row, 2)
            if not fio_item or not fio_item.text():
                QMessageBox.warning(self, "Ошибка", "Выберите сотрудника")
                return
            if not staraya_item or not staraya_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните старую должность")
                return
            if not novaya_item or not novaya_item.text():
                QMessageBox.warning(self, "Ошибка", "Заполните новую должность")
                return
            fio = fio_item.text()
            staraya = staraya_item.text()
            novaya = novaya_item.text()
            try:
                self.connect.cur.execute("SELECT id_sotrudnika FROM sotrudniki WHERE fio = %s", (fio,))
                emp = self.connect.cur.fetchone()
                if not emp:
                    QMessageBox.warning(self, "Ошибка", f"Сотрудник '{fio}' не найден")
                    return
                self.connect.cur.execute(
                    "INSERT INTO istoriya_dolzhnostey (id_sotrudnika, staraya_dolzhnost, novaya_dolzhnost) VALUES (%s, %s, %s)",
                    (emp[0], staraya, novaya)
                )
                self.obnovit_tablicu()
                QMessageBox.information(self, "Успех", "Запись в историю успешно добавлена")
            except Exception as e:
                self.connect.con.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить:\n{e}")

    def izmenit(self):
        current_row = self.ui.tableWidget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите строку для изменения")
            return
        if current_row == self.ui.tableWidget.rowCount() - 1:
            QMessageBox.warning(self, "Предупреждение", "Нельзя изменить пустую строку")
            return
        headers = []
        for col in range(self.ui.tableWidget.columnCount()):
            header = self.ui.tableWidget.horizontalHeaderItem(col)
            if header:
                headers.append(header.text())
            else:
                headers.append(f"Столбец {col + 1}")
        current_values = []
        for col in range(self.ui.tableWidget.columnCount()):
            item = self.ui.tableWidget.item(current_row, col)
            if item:
                current_values.append(item.text())
            else:
                current_values.append("")
        fields = [f"{headers[i]}: {current_values[i]}" for i in range(len(headers))]
        from PyQt5.QtWidgets import QInputDialog
        field_str, ok = QInputDialog.getItem(
            self,
            "Изменить запись",
            "Выберите поле для изменения:",
            fields,
            0,
            False
        )
        if not ok or not field_str:
            return
        selected_index = fields.index(field_str)
        selected_header = headers[selected_index]
        old_value = current_values[selected_index]
        new_value, ok = QInputDialog.getText(
            self,
            f"Изменить '{selected_header}'",
            f"Введите новое значение для '{selected_header}':",
            text=old_value
        )
        if not ok:
            return
        try:
            if self.current_index == 0:
                if selected_header == "ФИО":
                    self.connect.cur.execute(
                        "UPDATE sotrudniki SET fio = %s WHERE fio = %s",
                        (new_value, current_values[0])
                    )
                elif selected_header == "Должность":
                    self.connect.cur.execute(
                        "SELECT id_dolzhnosti FROM dolzhnosti WHERE nazvanie_dolzhnosti = %s",
                        (new_value,)
                    )
                    result = self.connect.cur.fetchone()
                    if not result:
                        QMessageBox.warning(self, "Ошибка", f"Должность '{new_value}' не найдена")
                        return
                    self.connect.cur.execute(
                        "UPDATE sotrudniki SET id_dolzhnosti = %s WHERE fio = %s",
                        (result[0], current_values[0])
                    )
                elif selected_header == "Подразделение":
                    self.connect.cur.execute(
                        "SELECT id_podrazdeleniya FROM podrazdeleniya WHERE nazvanie_podrazdeleniya = %s",
                        (new_value,)
                    )
                    result = self.connect.cur.fetchone()
                    if not result:
                        QMessageBox.warning(self, "Ошибка", f"Подразделение '{new_value}' не найдено")
                        return
                    self.connect.cur.execute(
                        "UPDATE sotrudniki SET id_podrazdeleniya = %s WHERE fio = %s",
                        (result[0], current_values[0])
                    )
                elif selected_header == "Помещение":
                    self.connect.cur.execute(
                        "SELECT id_pomeshcheniya FROM pomeshcheniya WHERE nomer_pomeshcheniya = %s",
                        (new_value,)
                    )
                    result = self.connect.cur.fetchone()
                    if result:
                        self.connect.cur.execute(
                            "UPDATE sotrudniki SET id_pomeshcheniya = %s WHERE fio = %s",
                            (result[0], current_values[0])
                        )
                    else:
                        self.connect.cur.execute(
                            "UPDATE sotrudniki SET id_pomeshcheniya = NULL WHERE fio = %s",
                            (current_values[0],)
                        )
            elif self.current_index == 2:
                if selected_header == "Подразделение":
                    self.connect.cur.execute(
                        "UPDATE podrazdeleniya SET nazvanie_podrazdeleniya = %s WHERE nazvanie_podrazdeleniya = %s",
                        (new_value, current_values[0])
                    )
                elif selected_header == "Код":
                    self.connect.cur.execute(
                        "UPDATE podrazdeleniya SET kod_podrazdeleniya = %s WHERE nazvanie_podrazdeleniya = %s",
                        (new_value, current_values[0])
                    )
            elif self.current_index == 3:
                if selected_header == "Помещение":
                    self.connect.cur.execute(
                        "UPDATE pomeshcheniya SET nomer_pomeshcheniya = %s WHERE nomer_pomeshcheniya = %s",
                        (new_value, current_values[0])
                    )
                elif selected_header == "Подразделение":
                    self.connect.cur.execute(
                        "SELECT id_podrazdeleniya FROM podrazdeleniya WHERE nazvanie_podrazdeleniya = %s",
                        (new_value,)
                    )
                    result = self.connect.cur.fetchone()
                    if result:
                        self.connect.cur.execute(
                            "UPDATE pomeshcheniya SET id_podrazdeleniya = %s WHERE nomer_pomeshcheniya = %s",
                            (result[0], current_values[0])
                        )
                elif selected_header == "Вместимость":
                    self.connect.cur.execute(
                        "UPDATE pomeshcheniya SET vmestimost = %s WHERE nomer_pomeshcheniya = %s",
                        (int(new_value), current_values[0])
                    )
            elif self.current_index == 1:
                QMessageBox.information(self, "Информация", "Изменение истории должностей не разрешено")
                return
            QMessageBox.information(self, "Успех", "Запись изменена")
            self.obnovit_tablicu()
        except Exception as e:
            self.connect.con.rollback()
            QMessageBox.critical(self, "Ошибка", f"Не удалось изменить:\n{e}")

    def obnovit_tablicu(self):
        if self.current_index == 0:
            self.pokazat_sotrudniki()
        elif self.current_index == 1:
            self.pokazat_istoriyu()
        elif self.current_index == 2:
            self.pokazat_podrazdeleniya()
        elif self.current_index == 3:
            self.pokazat_pomeshcheniya()

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
        data = list(self.connect.cur.fetchall())
        data.append(("", "", "", ""))
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
        data = list(self.connect.cur.fetchall())
        data.append(("", "", "", ""))
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
        data = list(self.connect.cur.fetchall())
        data.append(("", ""))
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
        data = list(self.connect.cur.fetchall())
        data.append(("", "", ""))
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        for row_num, row_data in enumerate(data):
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ui.tableWidget.setItem(row_num, col_num, item)
        self.ui.tableWidget.resizeColumnsToContents()

    def close_app(self):
        QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget2()
    widget.show()
    sys.exit(app.exec())
