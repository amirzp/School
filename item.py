from PyQt5 import (QtGui, QtWidgets, QtCore)
import sqlite3
import style
import sys
import loginPage
import addMember
import addBook


class Window(QtWidgets.QWidget):
    def __init__(self, data_name, window=None):
        super().__init__()
        self.setGeometry(150, 150, 800, 600)
        self.setWindowTitle("Item")
        self.db = sqlite3.connect("file/database.db")

        self.table = QtWidgets.QTableWidget()
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.data_name = data_name
        self.window = window
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomFrame = QtWidgets.QFrame()

        self.edit_page = None

        # ============= button ================
        self.editButton = QtWidgets.QPushButton()
        self.deleteButton = QtWidgets.QPushButton()
        # =============== set layout ============
        self.mainLayout.addWidget(self.table)
        self.setLayout(self.mainLayout)
        # =============== connect button ==================
        self.deleteButton.clicked.connect(self.delete_item)
        self.editButton.clicked.connect(self.edit_item_object)

    def show_item(self):
        for i in reversed(range(self.table.rowCount())):
            self.table.removeRow(i)

        data = "Select Count(*) from {}".format(self.data_name)
        rows = self.db.execute(data).fetchone()
        data = "SELECT name FROM pragma_table_info('{}')".format(self.data_name)
        columns = self.db.execute(data).fetchall()
        count = len(columns)
        self.table.setRowCount(rows[0])
        self.table.setColumnCount(count)
        for i in range(count):
            name = str(columns[i][0])
            self.table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(name.capitalize()))

        if self.data_name == "student":
            self.table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        if self.data_name == "teacher":
            self.table.setColumnHidden(0, True)
            self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        if self.data_name == "book":
            self.table.setColumnHidden(0, True)
            self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            self.table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        if self.data_name == "admin":
            self.table.setColumnHidden(2, True)
            self.table.setColumnHidden(0, True)
            self.table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        data = "Select id from {}".format(self.data_name)
        _id = self.db.execute(data).fetchall()
        for i in range(rows[0]):

            txt = "Select * from {} where id=?".format(self.data_name)
            table = self.db.execute(txt, (_id[i][0],)).fetchone()
            for j in range(count):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(table[j])))

    def edit_item_layout(self):
        self.bottomLayout.addStretch()
        self.bottomFrame.setStyleSheet(style.item_bottom_layout())
        self.editButton.setIcon(QtGui.QIcon(QtGui.QPixmap("file/Icon/edit_1.svg")))
        self.deleteButton.setIcon(QtGui.QIcon(QtGui.QPixmap("file/Icon/delete.svg")))
        self.bottomLayout.addWidget(self.editButton)
        self.bottomLayout.addWidget(self.deleteButton)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.bottomFrame)

    def data_base(self, txt):
        self.db.execute(txt)
        self.show_item()

    def delete_item(self):
        if self.table.selectionModel().hasSelection():

            m_box = QtWidgets.QMessageBox.information(self, "Warning", "You sure delete item?",
                                                      QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            _id = self.table.item(self.table.currentRow(), 0).text()

            if m_box == QtWidgets.QMessageBox.Yes:
                txt = """DELETE FROM {} where id=?""".format(self.data_name)
                self.db.execute(txt, (_id,))
                self.db.commit()

                QtWidgets.QMessageBox.information(self, "Info", "Item is deleted")
                self.show_item()
        else:
            QtWidgets.QMessageBox.information(self, "Warning", "Select an item first")

    def edit_item_object(self):
        if self.table.selectionModel().hasSelection():
            txt = "select * from {} where id=?".format(self.data_name)
            _id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.execute(txt, (_id,)).fetchone()
            self.window.setDisabled(True)

            if self.data_name == "admin":
                self.edit_page = loginPage.Dialog("reg")
                self.edit_page.edit_reg(data[1], data[2], data[2], data[0], self.window)

            elif self.data_name == "student":
                self.edit_page = addMember.Window("student", page=True)
                self.edit_page.edit_item(data, self.window)

            elif self.data_name == "teacher":
                self.edit_page = addMember.Window("teacher", page=True)
                self.edit_page.edit_item(data, self.window)

            elif self.data_name == "book":
                self.edit_page = addBook.Window(page=True)
                self.edit_page.edit_item(data, self.window)
        else:
            QtWidgets.QMessageBox.information(self, "Warning", "Select an item first")

    def search_item(self, value):
        if value == "":
            QtWidgets.QMessageBox.information(self, "Warning", "Search query can not empty")
            self.show_item()
        else:
            # self.lineEditSearch.setText("")
            txt_2 = "%" + value + "%"
            if self.data_name == "student":
                txt = "select * from {} where name like ? or family like ? or nationalCode like ?".format(self.data_name)
                data = self.db.execute(txt, (txt_2, txt_2, txt_2)).fetchall()
            elif self.data_name == "teacher":
                txt = "select * from {} where name like ? or family like ? or nationalCode like ?".format(self.data_name)
                data = self.db.execute(txt, (txt_2, txt_2, txt_2)).fetchall()
            elif self.data_name == "book":
                txt = "select * from {} where title like ? or author like ? or isbn like ?".format(self.data_name)
                data = self.db.execute(txt, (txt_2, txt_2, txt_2)).fetchall()
            elif self.data_name == "admin":
                txt = "select * from {} where username like ?".format(self.data_name)
                data = self.db.execute(txt, (txt_2, )).fetchall()
            if not data:
                QtWidgets.QMessageBox.information(self, "Warning", "This item does not exist")
            else:
                # if not self.__name__ == "sel":
                #     self.bottomGroupBox.hide()
                for i in reversed(range(self.table.rowCount())):
                    self.table.removeRow(i)
                rows = len(data)
                self.table.setRowCount(rows)
                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
