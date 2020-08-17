from PyQt5 import QtWidgets
import sys
import sqlite3
import style


class Window(QtWidgets.QWidget):
    def __init__(self, data_name, page=None):
        super().__init__()

        self.data_name = data_name
        self.page = page
        self.window = None
        self._id = None

        self.setGeometry(150, 150, 400, 400)
        # ================ layout =======================
        self.mainLayout = QtWidgets.QVBoxLayout()
        # ================== line edit =================
        self.nameLine = QtWidgets.QLineEdit()
        self.familyLine = QtWidgets.QLineEdit()
        self.fatherNameLine = QtWidgets.QLineEdit()
        self.nationalCodeLine = QtWidgets.QLineEdit()
        # ================== combo box =================
        self.genderCombo = QtWidgets.QComboBox()
        self.bothCombo = QtWidgets.QComboBox()
        self.yearBirthCombo = QtWidgets.QComboBox()
        # ============= button ================
        if not self.page:
            self.addButton = QtWidgets.QPushButton("ADD")
            self.addButton.clicked.connect(self.add_member)
        else:
            self.addButton = QtWidgets.QPushButton("EDIT")
            self.addButton.clicked.connect(self.add_member)
        # ============= data base ======================
        self.db = sqlite3.connect("file/database.db")

        if self.data_name == "student":
            for i in range(80, 100):
                self.yearBirthCombo.addItem("13" + str(i))
            self.bothLabel = QtWidgets.QLabel("Field :")
            self.bothCombo.addItems(["Mathematics", "Biology", "Chemistry", "History"])
        elif self.data_name == "teacher":
            for i in range(20, 80):
                self.yearBirthCombo.addItem("13" + str(i))
            self.bothLabel = QtWidgets.QLabel("Degree :")
            self.bothCombo.addItems(["Associate", "Bachelor", "Master", "Doctorate"])
        self.genderCombo.addItems(["Male", "Female", "Other"])

        self.ui()

    def top_ui(self):
        group_box = QtWidgets.QGroupBox("Personal Profile")
        if self.data_name == "student":
            group_box.setStyleSheet(style.group_box_student())
        elif self.data_name == "teacher":
            group_box.setStyleSheet(style.group_box_teacher())

        v_form = QtWidgets.QFormLayout()
        h_box = QtWidgets.QHBoxLayout()
        v_box = QtWidgets.QVBoxLayout()

        v_form.setVerticalSpacing(20)
        v_form.addRow("Name :", self.nameLine)
        v_form.addRow("Family :", self.familyLine)
        v_form.addRow("Father's Name :", self.fatherNameLine)
        v_form.addRow("National Code :", self.nationalCodeLine)

        h_box.addLayout(QtWidgets.QVBoxLayout(), 1)
        h_box.addLayout(v_form, 3)
        h_box.addLayout(QtWidgets.QVBoxLayout(), 1)

        v_box.addLayout(QtWidgets.QHBoxLayout(), 1)
        v_box.addLayout(h_box, 3)
        v_box.addLayout(QtWidgets.QHBoxLayout(), 1)

        group_box.setLayout(v_box)

        return group_box

    def bottom_ui(self):
        group_box = QtWidgets.QGroupBox("School Profile")
        if self.data_name == "student":
            group_box.setStyleSheet(style.group_box_student())
        elif self.data_name == "teacher":
            group_box.setStyleSheet(style.group_box_teacher())

        f_box = QtWidgets.QFormLayout()
        h_box = QtWidgets.QHBoxLayout()
        v_box = QtWidgets.QVBoxLayout()

        f_box.addRow("Gender :", self.genderCombo)
        h_box.addLayout(f_box)
        f_box = QtWidgets.QFormLayout()
        f_box.addRow(self.bothLabel, self.bothCombo)
        h_box.addLayout(f_box)
        f_box = QtWidgets.QFormLayout()
        f_box.addRow("Year Birth :", self.yearBirthCombo)
        h_box.addLayout(f_box)

        v_box.addLayout(QtWidgets.QHBoxLayout(), 1)
        v_box.addLayout(h_box, 2)

        group_box.setLayout(v_box)

        return group_box

    def ui(self):
        self.mainLayout.addWidget(self.top_ui(), 7)
        self.mainLayout.addWidget(self.bottom_ui(), 2)
        self.mainLayout.addWidget(self.addButton, 1)
        self.setLayout(self.mainLayout)
        self.show()

    def add_member(self):
        name = self.nameLine.text()
        family = self.familyLine.text()
        father_name = self.fatherNameLine.text()
        code = self.nationalCodeLine.text()
        gender = self.genderCombo.currentText()
        both = self.bothCombo.currentText()
        birth = self.yearBirthCombo.currentText()
        if not (name and family and father_name and code and gender) == "":
            if self.data_name == "student":
                txt_1 = "UPDATE student set name=?, family=?, fathername=?, nationalcode=?, gender=?, field=?, " \
                        "yearbirth=? WHERE id=?"

                txt_2 = "insert into student(name, family, fathername, nationalcode, gender, field, yearbirth) " \
                        "values(?,?,?,?,?,?,?) "
            elif self.data_name == "teacher":
                txt_1 = "UPDATE teacher set name=?, family=?, fathername=?, nationalcode=?, gender=?, degree=?, " \
                        "yearbirth=? WHERE id=?"

                txt_2 = "insert into teacher(name, family, fathername, nationalcode, gender, degree, yearbirth) " \
                        "values(?,?,?,?,?,?,?) "

            if self.page:
                self.db.execute(txt_1, (name, family, father_name, code, gender, both, birth, self._id))
                self.db.commit()
                self.window.enable_window(page=self.data_name)
                QtWidgets.QMessageBox.information(self, "Info", "Item is updated")
                self.destroy(True)
            else:
                self.db.execute(txt_2, (name, family, father_name, code, gender, both, birth))
                self.db.commit()
                QtWidgets.QMessageBox.information(self, "Info", "Item is added")
                self.nameLine.setText("")
                self.familyLine.setText("")
                self.fatherNameLine.setText("")
                self.nationalCodeLine.setText("")
        else:
            QtWidgets.QMessageBox.information(self, "Warning", "Fields can not empty")

    def edit_item(self, data, win):
        self.nameLine.setText(data[1])
        self.familyLine.setText(data[2])
        self.fatherNameLine.setText(data[3])
        self.nationalCodeLine.setText(data[4])
        self.genderCombo.setCurrentText(data[5])
        self.bothCombo.setCurrentText(data[6])
        self.yearBirthCombo.setCurrentText(data[7])

        self._id = data[0]
        self.window = win

    def closeEvent(self, event=None):
        if self._id:
            self.window.enable_window(flag=True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window("student")
    window.ui()
    sys.exit(app.exec_())
