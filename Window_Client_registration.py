# Form implementation generated from reading ui file 'UIes/Window_Client_registration.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog_Clients_registration(object):
    def setupUi(self, Dialog_Clients_registration):
        Dialog_Clients_registration.setObjectName("Dialog_Clients_registration")
        Dialog_Clients_registration.resize(787, 308)
        Dialog_Clients_registration.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        Dialog_Clients_registration.setAcceptDrops(False)
        Dialog_Clients_registration.setStyleSheet("")
        Dialog_Clients_registration.setSizeGripEnabled(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=Dialog_Clients_registration)
        self.buttonBox.setGeometry(QtCore.QRect(580, 260, 175, 34))
        self.buttonBox.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.buttonBox.setStyleSheet("")
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frame_2 = QtWidgets.QFrame(parent=Dialog_Clients_registration)
        self.frame_2.setGeometry(QtCore.QRect(30, 20, 731, 221))
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.te_cl_fname = QtWidgets.QTextEdit(parent=self.frame_2)
        self.te_cl_fname.setGeometry(QtCore.QRect(30, 70, 211, 26))
        self.te_cl_fname.setTabletTracking(False)
        self.te_cl_fname.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.te_cl_fname.setStyleSheet("")
        self.te_cl_fname.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.te_cl_fname.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.te_cl_fname.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.te_cl_fname.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.te_cl_fname.setTabChangesFocus(False)
        self.te_cl_fname.setUndoRedoEnabled(True)
        self.te_cl_fname.setOverwriteMode(False)
        self.te_cl_fname.setAcceptRichText(True)
        self.te_cl_fname.setObjectName("te_cl_fname")
        self.te_cl_lname = QtWidgets.QTextEdit(parent=self.frame_2)
        self.te_cl_lname.setGeometry(QtCore.QRect(260, 70, 211, 26))
        self.te_cl_lname.setTabletTracking(False)
        self.te_cl_lname.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.te_cl_lname.setStyleSheet("")
        self.te_cl_lname.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.te_cl_lname.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.te_cl_lname.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.te_cl_lname.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.te_cl_lname.setTabChangesFocus(False)
        self.te_cl_lname.setUndoRedoEnabled(True)
        self.te_cl_lname.setOverwriteMode(False)
        self.te_cl_lname.setAcceptRichText(True)
        self.te_cl_lname.setObjectName("te_cl_lname")
        self.te_cl_email = QtWidgets.QTextEdit(parent=self.frame_2)
        self.te_cl_email.setGeometry(QtCore.QRect(410, 120, 291, 26))
        self.te_cl_email.setTabletTracking(False)
        self.te_cl_email.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.te_cl_email.setStyleSheet("")
        self.te_cl_email.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.te_cl_email.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.te_cl_email.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.te_cl_email.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.te_cl_email.setTabChangesFocus(False)
        self.te_cl_email.setUndoRedoEnabled(True)
        self.te_cl_email.setOverwriteMode(False)
        self.te_cl_email.setAcceptRichText(True)
        self.te_cl_email.setObjectName("te_cl_email")
        self.te_cl_patr = QtWidgets.QTextEdit(parent=self.frame_2)
        self.te_cl_patr.setGeometry(QtCore.QRect(490, 70, 211, 26))
        self.te_cl_patr.setTabletTracking(False)
        self.te_cl_patr.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.te_cl_patr.setStyleSheet("")
        self.te_cl_patr.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.te_cl_patr.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.te_cl_patr.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.te_cl_patr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.te_cl_patr.setTabChangesFocus(False)
        self.te_cl_patr.setUndoRedoEnabled(True)
        self.te_cl_patr.setOverwriteMode(False)
        self.te_cl_patr.setAcceptRichText(True)
        self.te_cl_patr.setObjectName("te_cl_patr")
        self.te_cl_phone = QtWidgets.QTextEdit(parent=self.frame_2)
        self.te_cl_phone.setGeometry(QtCore.QRect(30, 120, 171, 26))
        self.te_cl_phone.setTabletTracking(False)
        self.te_cl_phone.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.te_cl_phone.setStyleSheet("")
        self.te_cl_phone.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.te_cl_phone.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.te_cl_phone.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.te_cl_phone.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.te_cl_phone.setTabChangesFocus(False)
        self.te_cl_phone.setUndoRedoEnabled(True)
        self.te_cl_phone.setOverwriteMode(False)
        self.te_cl_phone.setAcceptRichText(True)
        self.te_cl_phone.setObjectName("te_cl_phone")
        self.te_cl_address = QtWidgets.QTextEdit(parent=self.frame_2)
        self.te_cl_address.setGeometry(QtCore.QRect(30, 170, 581, 26))
        self.te_cl_address.setTabletTracking(False)
        self.te_cl_address.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.te_cl_address.setStyleSheet("")
        self.te_cl_address.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.te_cl_address.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.te_cl_address.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.te_cl_address.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.te_cl_address.setTabChangesFocus(False)
        self.te_cl_address.setUndoRedoEnabled(True)
        self.te_cl_address.setOverwriteMode(False)
        self.te_cl_address.setAcceptRichText(True)
        self.te_cl_address.setObjectName("te_cl_address")
        self.label = QtWidgets.QLabel(parent=self.frame_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 403, 37))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.te_cl_passport = QtWidgets.QTextEdit(parent=self.frame_2)
        self.te_cl_passport.setGeometry(QtCore.QRect(230, 120, 161, 26))
        self.te_cl_passport.setTabletTracking(False)
        self.te_cl_passport.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.DefaultContextMenu)
        self.te_cl_passport.setStyleSheet("")
        self.te_cl_passport.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.te_cl_passport.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.te_cl_passport.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.te_cl_passport.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.te_cl_passport.setTabChangesFocus(False)
        self.te_cl_passport.setUndoRedoEnabled(True)
        self.te_cl_passport.setOverwriteMode(False)
        self.te_cl_passport.setAcceptRichText(True)
        self.te_cl_passport.setObjectName("te_cl_passport")

        self.retranslateUi(Dialog_Clients_registration)
        self.buttonBox.accepted.connect(Dialog_Clients_registration.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog_Clients_registration.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog_Clients_registration)

    def retranslateUi(self, Dialog_Clients_registration):
        _translate = QtCore.QCoreApplication.translate
        Dialog_Clients_registration.setWindowTitle(_translate("Dialog_Clients_registration", "Регистрация клиента"))
        self.te_cl_fname.setPlaceholderText(_translate("Dialog_Clients_registration", "Фамилия"))
        self.te_cl_lname.setPlaceholderText(_translate("Dialog_Clients_registration", "Имя"))
        self.te_cl_email.setPlaceholderText(_translate("Dialog_Clients_registration", "Адрес электронной почты (...@domain.com)"))
        self.te_cl_patr.setPlaceholderText(_translate("Dialog_Clients_registration", "Отчество"))
        self.te_cl_phone.setPlaceholderText(_translate("Dialog_Clients_registration", "Номер телефона"))
        self.te_cl_address.setPlaceholderText(_translate("Dialog_Clients_registration", "Адрес проживания"))
        self.label.setText(_translate("Dialog_Clients_registration", "Регистрация нового клиента"))
        self.te_cl_passport.setPlaceholderText(_translate("Dialog_Clients_registration", "Паспорт (****-******)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_Clients_registration = QtWidgets.QDialog()
    ui = Ui_Dialog_Clients_registration()
    ui.setupUi(Dialog_Clients_registration)
    Dialog_Clients_registration.show()
    sys.exit(app.exec())
