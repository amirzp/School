from PyQt5 import (QtWidgets, QtGui)
import sys
import style
import sqlite3


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(150, 150, 600, 800)
        # ============ layout ====================
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.middleLayout = QtWidgets.QHBoxLayout()
        self.middleLayoutChild = QtWidgets.QFormLayout()
        # ========== data base ====================
        self.db = sqlite3.connect("file/database.db")

        self.ui()

    def ui(self):
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addStretch()

        self.middleLayoutChild.setVerticalSpacing(30)


        self.middleLayoutChild.addRow(self.middle_layout_design("Student", self.data_count("student"), "file/Icon/school.svg"))

        self.middleLayoutChild.addRow(self.middle_layout_design("Teacher", self.data_count("teacher"), "file/Icon/teacher.svg"))

        self.middleLayoutChild.addRow(self.middle_layout_design("Book", self.data_count("book"), "file/Icon/book.svg"))

        self.middleLayoutChild.addRow(self.middle_layout_design("Admin", self.data_count("admin"), "file/Icon/admin-ui.svg"))

        self.middleLayout.addStretch(1)
        self.middleLayout.addLayout(self.middleLayoutChild, 4)
        self.middleLayout.addStretch(1)

        self.setLayout(self.mainLayout)

    @staticmethod
    def middle_layout_design(label_data, label_number, icon):
        q_form = QtWidgets.QFrame()
        q_form.setStyleSheet(style.dashboard_frame())
        h_box = QtWidgets.QHBoxLayout()
        v_box = QtWidgets.QVBoxLayout()

        v_box.addWidget(QtWidgets.QLabel(label_data))
        v_box.addWidget(QtWidgets.QLabel(label_number))

        h_box.addLayout(v_box)
        h_box.addStretch()
        label = QtWidgets.QLabel()
        image = QtGui.QPixmap(icon)
        f = image.scaled(80, 80)
        label.setPixmap(f)

        h_box.addWidget(label)

        q_form.setLayout(h_box)

        return q_form

    def data_count(self, data_name):
        txt = "select count(*) from {}".format(data_name)
        count = self.db.execute(txt).fetchone()

        if count is None:
            return str(0)
        else:
            return str(count[0])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
