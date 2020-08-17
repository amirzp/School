import style
from PyQt5 import (QtWidgets, QtGui, QtCore)
import sys
import item
import loginPage
import addMember
import addBook
import showDashBoard


class StudentWindow(QtWidgets.QWidget):
    def __init__(self, admin_name):
        super().__init__()
        self.setGeometry(150, 150, 800, 600)
        self.setWindowTitle("Student Window")
        # ================== items ====================
        self.adminLabel = QtWidgets.QLabel(admin_name.capitalize() + "  ADMIN")
        self.adminLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.adminLabel.setFont(QtGui.QFont("Gabriola", 14))

        self.flag_search = None

        # =================== layouts =========================
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.rightLayout = QtWidgets.QVBoxLayout()
        self.leftLayout = QtWidgets.QFrame()

        # ========== search object =============
        self.searchLayout = QtWidgets.QFormLayout()

        self.searchLine = QtWidgets.QLineEdit()
        self.searchLine.setPlaceholderText("Search for...")
        self.searchButton = QtWidgets.QPushButton()
        self.searchButton.setIcon(QtGui.QIcon(QtGui.QPixmap("file/Icon/search.svg")))
        self.searchLayout.addRow(self.searchLine, self.searchButton)
        self.searchButton.clicked.connect(self.click_search)
        self.search_hide()
        # ================ child right layout ============
        self.rightLayoutTop = QtWidgets.QFrame()
        self.rightLayoutTop.setStyleSheet(style.right_layout_student())
        self.rightLayoutTopBox = QtWidgets.QHBoxLayout()
        self.rightLayoutBottom = QtWidgets.QFrame()

        # ================ child left layout ==============
        self.formLeftLayout = QtWidgets.QFormLayout()

        # ================ tool bar =====================
        self.toolBarLog = QtWidgets.QPushButton()
        self.toolBarLog.setIcon(QtGui.QIcon(QtGui.QPixmap("file/Icon/logout.svg")))
        self.toolBarExit = QtWidgets.QPushButton()
        self.toolBarExit.setIcon(QtGui.QIcon(QtGui.QPixmap("file/Icon/off.svg")))

    def ui(self):
        # =====================================================

        self.mainLayout.addWidget(self.leftLayout, 2)
        self.mainLayout.addLayout(self.rightLayout, 7)

        self.rightLayout.addWidget(self.rightLayoutTop, 1)
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        # self.rightLayoutTop.addWidget(self.toolBar)

        self.leftLayout.setLayout(self.formLeftLayout)

        self.setLayout(self.mainLayout)

        # ==================== left layout design ==============
        self.leftLayout.setStyleSheet(style.left_layout_student())
        self.formLeftLayout.addRow(self.adminLabel)
        ls = ["Home", "DashBoard", "s", "Student", "All Student", "Add Student", "Edit Student",
              "s", "Teacher", "All Teacher", "Add Teacher", "Edit Teacher",
              "s", "Book", "All Book", "Add Book", "Edit Book",
              "s", "Admin", "All Admin", "Add Admin", "Edit Admin"]
        for i in range(len(ls)):
            if ls[i] == "Home" or ls[i] == "Student" or ls[i] == "Teacher" or ls[i] == "Book" or ls[i] == "Admin":
                self.formLeftLayout.addRow(QtWidgets.QLabel(ls[i].upper()))
            elif ls[i] == "s":
                line_sep = QtWidgets.QFrame()
                line_sep.setFrameShape(QtWidgets.QFrame.HLine)
                line_sep.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                line_sep.setLineWidth(3)
                self.formLeftLayout.addRow(line_sep)
            else:

                # =================== click connect =================
                if ls[i] == "DashBoard":
                    icon = QtGui.QPixmap("file/Icon/dashboard.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.dashboard_show)

                elif ls[i] == "All Student":
                    icon = QtGui.QPixmap("file/Icon/list.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.show_student)

                elif ls[i] == "Add Student":
                    icon = QtGui.QPixmap("file/Icon/add.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.add_student)

                elif ls[i] == "Edit Student":
                    icon = QtGui.QPixmap("file/Icon/edit.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.edit_student)

                elif ls[i] == "All Teacher":
                    icon = QtGui.QPixmap("file/Icon/list.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.show_teacher)

                elif ls[i] == "Add Teacher":
                    icon = QtGui.QPixmap("file/Icon/add.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.add_teacher)

                elif ls[i] == "Edit Teacher":
                    icon = QtGui.QPixmap("file/Icon/edit.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.edit_teacher)

                elif ls[i] == "All Book":
                    icon = QtGui.QPixmap("file/Icon/list.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.show_book)

                elif ls[i] == "Add Book":
                    icon = QtGui.QPixmap("file/Icon/knowledge.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.add_book)

                elif ls[i] == "Edit Book":
                    icon = QtGui.QPixmap("file/Icon/edit.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.edit_book)

                elif ls[i] == "All Admin":
                    icon = QtGui.QPixmap("file/Icon/list.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.show_admin)

                elif ls[i] == "Add Admin":
                    icon = QtGui.QPixmap("file/Icon/add.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.add_admin)

                elif ls[i] == "Edit Admin":
                    icon = QtGui.QPixmap("file/Icon/edit.svg")
                    btn = QtWidgets.QPushButton(ls[i])
                    btn.setIcon(QtGui.QIcon(icon))
                    self.formLeftLayout.addRow(btn)

                    btn.clicked.connect(self.edit_admin)
            # h = QtWidgets.QVBoxLayout()
            # self.formLeftLayout.addRow(h.addStretch())
        # ================ right layout design =============
        self.rightLayoutTopBox.addLayout(self.searchLayout)
        self.rightLayoutTopBox.addStretch(10)
        self.rightLayoutTopBox.addWidget(self.toolBarLog)
        self.rightLayoutTopBox.addWidget(self.toolBarExit)
        self.rightLayoutTop.setLayout(self.rightLayoutTopBox)

        self.dashboard_show()
        self.show()

    def delete_right_layout_widget(self):
        widget = self.rightLayout.takeAt(1).widget()
        if widget is not None:
            widget.deleteLater()
            self.rightLayoutBottom = None

    def dashboard_show(self):
        self.search_hide()
        self.delete_right_layout_widget()
        self.rightLayoutBottom = showDashBoard.Window()
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)

    def show_student(self):
        self.delete_right_layout_widget()
        self.rightLayoutBottom = item.Window("student")
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.rightLayoutBottom.data_base("Create Table if not exists student"
                                         "(id integer primary key, name text, family text, "
                                         "fatherName text, nationalCode text, gender text, field text, yearBirth text)")
        self.search_layout()
        self.flag_search = "student"

    def add_student(self):
        self.search_hide()
        self.delete_right_layout_widget()
        self.rightLayoutBottom = addMember.Window("student")
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.search_hide()

    def edit_student(self):
        self.delete_right_layout_widget()
        self.rightLayoutBottom = item.Window(data_name="student", window=self)
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.rightLayoutBottom.data_base("Create Table if not exists student"
                                         "(id integer primary key, name text, family text, "
                                         "fatherName text, nationalCode text, gender text, field text, yearBirth text)")
        self.rightLayoutBottom.edit_item_layout()
        self.search_layout()
        self.flag_search = "student"

    def show_teacher(self):
        self.delete_right_layout_widget()
        self.rightLayoutBottom = item.Window("teacher")
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.rightLayoutBottom.data_base("Create Table if not exists teacher"
                                         "(id integer primary key, name text, family text, "
                                         "fatherName text, nationalCode text, gender text, degree text, yearBirth text)")
        self.search_layout()
        self.flag_search = "teacher"

    def add_teacher(self):
        self.delete_right_layout_widget()
        self.rightLayoutBottom = addMember.Window("teacher")
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.search_hide()

    def edit_teacher(self):
        self.search_hide()
        self.delete_right_layout_widget()
        self.rightLayoutBottom = item.Window("teacher", self)
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.rightLayoutBottom.data_base("Create Table if not exists teacher"
                                         "(id integer primary key, name text, family text, "
                                         "fatherName text, nationalCode text, gender text, degree text, yearBirth text)")
        self.rightLayoutBottom.edit_item_layout()
        self.search_layout()
        self.flag_search = "teacher"

    def show_book(self):
        self.delete_right_layout_widget()
        self.rightLayoutBottom = item.Window("book")
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.rightLayoutBottom.data_base("Create Table if not exists book"
                                         "(id integer primary key, title text, author text, "
                                         "year text, isbn text, page text)")
        self.search_layout()
        self.flag_search = "book"

    def add_book(self):
        self.search_hide()
        self.delete_right_layout_widget()
        self.rightLayoutBottom = addBook.Window()
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.search_hide()

    def edit_book(self):
        self.delete_right_layout_widget()
        self.rightLayoutBottom = item.Window("book", self)
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.rightLayoutBottom.data_base("Create Table if not exists book"
                                         "(id integer primary key, title text, author text, "
                                         "year text, isbn text, page text)")
        self.rightLayoutBottom.edit_item_layout()
        self.search_layout()
        self.flag_search = "book"

    def show_admin(self):
        self.delete_right_layout_widget()
        self.rightLayoutBottom = item.Window("admin")
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.rightLayoutBottom.data_base("create table if not exists admin"
                                         "(id integer primary key, username text, password text)")
        self.search_layout()
        self.flag_search = "admin"

    def add_admin(self):
        self.search_hide()
        self.delete_right_layout_widget()
        self.rightLayoutBottom = loginPage.Dialog("reg")
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.search_hide()

    def edit_admin(self):
        self.delete_right_layout_widget()
        self.rightLayoutBottom = item.Window("admin", self)
        self.rightLayout.addWidget(self.rightLayoutBottom, 20)
        self.rightLayoutBottom.data_base("create table if not exists admin"
                                         "(id integer primary key, username text, password text)")
        self.rightLayoutBottom.edit_item_layout()
        self.search_layout()
        self.flag_search = "admin"

    def enable_window(self, flag=None, page=None):
        if not flag:
            self.setDisabled(False)
            self.rightLayoutBottom.destroy(True)
            self.rightLayoutBottom = None
            if page == "admin":
                self.edit_admin()
            elif page == "student":
                self.edit_student()
            elif page == "teacher":
                self.edit_teacher()
            elif page == "book":
                self.edit_book()
        else:
            self.setDisabled(False)
            # self.rightLayoutBottom.destroy(True)
            # self.rightLayoutBottom = None
            self.rightLayoutBottom.show_item()

    def search_layout(self):
        self.searchLine.show()
        self.searchButton.show()
        self.searchLine.setText("")

    def search_hide(self):
        self.searchLine.hide()
        self.searchButton.hide()
        self.flag_search = None

    def click_search(self):
        if self.flag_search:
            value = self.searchLine.text()
            self.rightLayoutBottom.search_item(value)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = StudentWindow("amir")
    window.ui()
    app.setStyle('Breeze')
    # ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    sys.exit(app.exec_())
