from PyQt5 import QtWidgets
import sys
import sqlite3
import style


class Window(QtWidgets.QWidget):
    def __init__(self, page=None):
        super().__init__()
        self.page = page
        self.window = None
        self._id = None

        self.setGeometry(150, 150, 400, 400)
        # ================ layout =======================
        self.mainLayout = QtWidgets.QVBoxLayout()
        # ================== line edit =================
        self.titleLine = QtWidgets.QLineEdit()
        self.authorLine = QtWidgets.QLineEdit()
        self.yearLine = QtWidgets.QLineEdit()
        self.isbnLine = QtWidgets.QLineEdit()
        self.pageLine = QtWidgets.QLineEdit()
        # ============= button ================
        if not self.page:
            self.addButton = QtWidgets.QPushButton("ADD")
            self.addButton.clicked.connect(self.add_member)
        else:
            self.addButton = QtWidgets.QPushButton("EDIT")
            self.addButton.clicked.connect(self.add_member)
        # ============= data base ======================
        self.db = sqlite3.connect("file/database.db")

        self.ui()

    def page_ui(self):
        group_box = QtWidgets.QGroupBox("Personal Profile")
        group_box.setStyleSheet(style.group_box_student())

        v_form = QtWidgets.QFormLayout()
        h_box = QtWidgets.QHBoxLayout()
        v_box = QtWidgets.QVBoxLayout()

        v_form.setVerticalSpacing(20)
        v_form.addRow("Title :", self.titleLine)
        v_form.addRow("Author :", self.authorLine)
        v_form.addRow("Year :", self.yearLine)
        v_form.addRow("Isbn :", self.isbnLine)
        v_form.addRow("Page :", self.pageLine)

        h_box.addLayout(QtWidgets.QVBoxLayout(), 1)
        h_box.addLayout(v_form, 3)
        h_box.addLayout(QtWidgets.QVBoxLayout(), 1)

        v_box.addLayout(QtWidgets.QHBoxLayout(), 1)
        v_box.addLayout(h_box, 3)
        v_box.addLayout(QtWidgets.QHBoxLayout(), 1)

        group_box.setLayout(v_box)

        return group_box

    def ui(self):
        self.mainLayout.addWidget(self.page_ui(), 7)
        self.mainLayout.addWidget(self.addButton, 1)
        self.setLayout(self.mainLayout)
        self.show()

    def add_member(self):
        title = self.titleLine.text()
        author = self.authorLine.text()
        year = self.yearLine.text()
        code = self.isbnLine.text()
        page = self.pageLine.text()
        if not (title and author and year and code and page) == "":
            txt_1 = "UPDATE book set title=?, author=?, year=?, isbn=?, page=? WHERE id=?"

            txt_2 = "insert into book(title, author, year, isbn, page) values(?,?,?,?,?) "

            if self.page:
                self.db.execute(txt_1, (title, author, year, code, page, self._id))
                self.db.commit()
                self.window.enable_window(page="book")
                QtWidgets.QMessageBox.information(self, "Info", "Item is updated")
                self.destroy(True)
            else:
                self.db.execute(txt_2, (title, author, year, code, page))
                self.db.commit()
                QtWidgets.QMessageBox.information(self, "Info", "Item is added")
                self.titleLine.setText("")
                self.authorLine.setText("")
                self.yearLine.setText("")
                self.isbnLine.setText("")
                self.pageLine.setText("")
        else:
            QtWidgets.QMessageBox.information(self, "Warning", "Fields can not empty")

    def edit_item(self, data, win):
        self.titleLine.setText(data[1])
        self.authorLine.setText(data[2])
        self.yearLine.setText(data[3])
        self.isbnLine.setText(data[4])
        self.pageLine.setText(data[5])

        self._id = data[0]
        self.window = win

    def closeEvent(self, event=None):
        if self._id:
            self.window.enable_window(flag=True)
