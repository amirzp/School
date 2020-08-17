import sys
import style
from PyQt5 import (QtWidgets, QtGui, QtCore)
import searchAdmin


#############################################################################
class Dialog(QtWidgets.QWidget):

    # ========================================================================
    def __init__(self, win=None):
        super().__init__()

        self.setGeometry(150, 150, 800, 600)
        self.win = win

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.topLayout = QtWidgets.QVBoxLayout()
        self.middleLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout = QtWidgets.QVBoxLayout()
        self.childMiddleLayout = QtWidgets.QFormLayout()
        self.frame = QtWidgets.QFrame()

        self.main_reg = QtWidgets.QVBoxLayout()
        self.frame_reg = QtWidgets.QFrame()

        self.labelLog = QtWidgets.QLabel("LOGIN HERE")
        self.labelLog.setFont(QtGui.QFont("Gabriola", 24))
        self.userLabel = QtWidgets.QLabel("User Name : ")
        self.passLabel = QtWidgets.QLabel("Password : ")
        self.confirmPassLabel = QtWidgets.QLabel("ConfirmPass : ")
        self.userLine = QtWidgets.QLineEdit()
        self.userLine.setPlaceholderText("User Name")
        self.passLine = QtWidgets.QLineEdit()
        self.passLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passLine.setPlaceholderText("Password")
        self.confirmPassLine = QtWidgets.QLineEdit()
        self.confirmPassLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassLine.setPlaceholderText("Confirm Password")
        self.logButton = QtWidgets.QPushButton("Login", self)

        self._id = None
        self.window = None
        self.flag = None
        self.admin_name = None

        self.image0 = QtGui.QImage("file/1.jpg")

        self.read_image(self.width(), self.height())
        self.ui_log()

    def ui_log(self):
        self.topLayout.addStretch()
        self.bottomLayout.addStretch()
        self.mainLayout.addLayout(self.topLayout, 3)
        self.mainLayout.addLayout(self.middleLayout, 4)
        self.mainLayout.addLayout(self.bottomLayout, 3)

        self.middleLayout.addStretch(1)
        self.middleLayout.addWidget(self.frame, 2)
        self.middleLayout.addStretch(1)

        self.labelLog.setAlignment(QtCore.Qt.AlignCenter)
        self.logButton.setStyleSheet(style.log_button())

        self.userLine.setStyleSheet(style.line_edit())
        self.passLine.setStyleSheet(style.line_edit())
        self.frame.setStyleSheet(style.main_frame())
        self.childMiddleLayout.setVerticalSpacing(30)
        self.childMiddleLayout.addRow(self.labelLog)
        self.childMiddleLayout.addRow(self.userLabel, self.userLine)
        self.childMiddleLayout.addRow(self.passLabel, self.passLine)
        if self.win == "reg":
            self.confirmPassLine.setStyleSheet(style.line_edit())
            self.childMiddleLayout.addRow(self.confirmPassLabel, self.confirmPassLine)
            self.labelLog.setText("REGISTER HERE")
            self.logButton.setText("Register")
            self.logButton.clicked.connect(self.click_reg)
        self.childMiddleLayout.verticalSpacing()

        self.childMiddleLayout.addRow(self.logButton)
        self.frame.setLayout(self.childMiddleLayout)

    def read_image(self, width=None, height=None):

        if width is not None and height is None:
            image_file = self.image0.scaledToWidth(width, QtCore.Qt.SmoothTransformation)
        elif width is None and height is not None:
            image_file = self.image0.scaledToHeight(height, QtCore.Qt.SmoothTransformation)
        elif width is not None and height is not None:
            image_file = self.image0.scaled(width, height, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        else:
            image_file = self.image0

        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(image_file))

        if not self.win == "reg":
            self.setLayout(self.mainLayout)
            self.setPalette(palette)
        elif self.win == "reg":
            self.frame_reg.setStyleSheet("background-color : #808080;")
            self.frame_reg.setLayout(self.mainLayout)
            self.main_reg.addWidget(self.frame_reg)
            self.setLayout(self.main_reg)
            self.frame_reg.setPalette(palette)
            self.show()

    def click_log(self):
        user = self.userLine.text().lower()
        password = self.passLine.text()
        if user and password:
            flag = searchAdmin.login(user, password)
            if flag:
                self.admin_name = user
                return True
            else:
                QtWidgets.QMessageBox.information(self, "Warning", "Incorrect username or password")
        else:
            QtWidgets.QMessageBox.information(self, "Warning", "Fields can not empty")

    def click_reg(self):
        user = self.userLine.text().lower()
        password = self.passLine.text()
        c_password = self.confirmPassLine.text()
        if user and password and c_password:
            if not len(password) > 3:
                QtWidgets.QMessageBox.information(self, "Warning",
                                                  "Your password must be at least 4 character. please try again")
            else:
                flag = searchAdmin.register(user, password, c_password, self._id)
                if flag is None:
                    QtWidgets.QMessageBox.information(self, "Warning", "Those passwords didn't match. please try again")
                elif flag is False:
                    QtWidgets.QMessageBox.information(self, "Warning", "UserName has been taken. please try again")
                elif flag is True:
                    QtWidgets.QMessageBox.information(self, "info", "Admin has been added")
                    if self._id:
                        self.window.enable_window(page="admin")
                        self.destroy(True)
                    self.userLine.setText("")
                    self.passLine.setText("")
                    self.confirmPassLine.setText("")
        else:
            QtWidgets.QMessageBox.information(self, "Warning", "Fields can not empty")

    def edit_reg(self, user, password, password_c, _id, window):
        self.userLine.setText(user)
        self.passLine.setText(password)
        self.confirmPassLine.setText(password_c)
        self._id = _id
        self.window = window

    def resizeEvent(self, event=None):
        self.read_image(event.size().width(), event.size().height())

    def closeEvent(self, event=None):
        if self._id:
            self.window.enable_window(flag=True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    fen = Dialog()
    # fen.show()
    sys.exit(app.exec_())
