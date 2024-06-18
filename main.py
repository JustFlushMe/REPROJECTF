import io
import json
import sys
import datetime
import time

import DataSets
import psycopg2
import pyperclip
import openpyxl
import importlib
import pandas as pd
# 09.06.2024 - Отчеты, фото объектов
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QImage
from psycopg2 import Binary
from PIL import Image
from PyQt6.QtGui import QPixmap

import connect_config
from DataSets import *
from UserInterface import Ui_MainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QDateTime
from datetime import datetime, date
import connect_config
import pickle
from PyQt6.QtCore import QTimer
from Window_Client_registration import Ui_Dialog_Clients_registration
from Window_Impressions_add import Ui_Dialog_Impressions_add
from Window_Objects_add import Ui_Dialog_Objects_add
from Window_Representatives_add import Ui_Dialog_Representatives_add
from Window_Meetings_add import Ui_Dialog_Meetings_add
from Window_ServicesHist_add import Ui_Dialog_ServiceHist_add
from Window_ObjectsC_add import Ui_Dialog_Objects_add
from Window_Deals_add import Ui_Dialog_Deals_add
from Window_Deals_c_add import Ui_Dialog_Deals_c_add
from Window_Requests_add import Ui_Dialog_Requests_add
from Window_Guests_add import Ui_Dialog_Guests_add
from Window_Pictures import Ui_Dialog_pictures

class AuthorizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Авторизация")

        self.ip_label = QLabel("IP Адрес сервера:")
        self.ip_input = QLineEdit()
        self.port_label = QLabel("Порт сервера")
        self.port_input = QLineEdit()
        self.db_label = QLabel("Название БД")
        self.db_input = QLineEdit()

        self.username_label = QLabel("Имя пользователя:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        self.ip_input.setText(connect_config.host)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)
        self.port_input.setText(connect_config.port)
        layout.addWidget(self.db_label)
        layout.addWidget(self.db_input)
        self.db_input.setText(connect_config.dbname)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        self.username_input.setText(connect_config.user)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        self.password_input.setText(connect_config.password)
        layout.addWidget(self.login_button)
        self.setLayout(layout)



        # try:                user = 'postgres',
        #                 password = 'password',
        #                 host = '172.17.0.2',
        #                 port = '5432'
        #     connection = psycopg2.connect(
        #
        #     )
        #     connection.close()
        #
        # except()

    def login(self):
        try:
            with open ('connect_config.py', 'w') as file:
                file.write(
f'''dbname = '{self.db_input.text()}'
user = '{self.username_input.text()}'
password = '{self.password_input.text()}'
host = '{self.ip_input.text()}'
port = '{self.port_input.text()}' ''')

            database = self.db_input.text()
            user = self.username_input.text()
            password = self.password_input.text()
            host = self.ip_input.text()
            port = self.port_input.text()

            # Здесь можно добавить логику проверки имени пользователя и пароля
            self.connection = psycopg2.connect(
                dbname = database,
                user = user,
                password = password,
                host = host,
                port = port,
            )

            cur = self.connection.cursor()
            window.show()

            auth_window.close()

        except psycopg2.Error as e:
            MainWindow.show_errorMessage(self, 'Ошибкаа', 'Ошибка')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1700, 850)

        self.rowValues = None #
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Глобальные переменные
        self.sqlquery = ""
        self.connection = ""
        self.currentTable = ""
        self.pictures = []
        self.file_paths = []
        # Обработка событий панели действий

        self.ui.bt_clientsReg.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_Clients_registration()))
        self.ui.bt_meetingsAdd.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_Meetings_add()))
        self.ui.bt_servicesHistAdd.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_ServiceHist_add()))

        self.ui.bt_requests_add.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_Requests_add()))
        self.ui.bt_objects_add.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_Objects_add()))
        self.ui.bt_representatives_add.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_Representatives_add()))
        self.ui.bt_deals_add.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_Deals_add()))
        self.ui.bt_impressions_add.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_Impressions_add()))
        self.ui.bt_guests_add.clicked.connect(lambda: self.ShowAddDialog(Ui_Dialog_Guests_add()))

        # Обработка событий панели навигации
        self.ui.bt_services.clicked.connect(self.eventHandler_bt_servicesHist)
        self.ui.bt_meetings.clicked.connect(self.eventHandler_bt_meetings)
        self.ui.bt_deals.clicked.connect(self.eventHandler_bt_deals)
        self.ui.bt_deals_c.clicked.connect(self.eventHandler_bt_deals_c)
        self.ui.bt_clients.clicked.connect(self.eventHandler_bt_clients)
        self.ui.bt_requests.clicked.connect(self.eventHandler_bt_requests)
        self.ui.bt_objects.clicked.connect(self.eventHandler_bt_objects)
        self.ui.bt_representatives.clicked.connect(self.eventHandler_bt_representatives)
        self.ui.bt_objectsC.clicked.connect(self.eventHandler_bt_objectsC)
        self.ui.bt_guests.clicked.connect(self.eventHandler_bt_guests)
        self.ui.bt_impressions.clicked.connect(self.eventHandler_bt_impressions)

        # Обработка событий панели свойств
        self.ui.tableWidget_main.clicked.connect(self.GetDataFromCurrentRow)
        self.ui.bt_edit.clicked.connect(lambda: self.EditCurrentRow())
        self.ui.bt_delete.clicked.connect(self.DeleteDataFromCurrentRow)
        self.ui.bt_objectsc_showPhotos.clicked.connect(self.ExportPicturesFromDB)

        self.ui.bt_notifications.clicked.connect(lambda: self.showTodaysImpressions())

        # Обработка событий виджетов
        self.ui.bt_guests_contacts_export.clicked.connect(self.ExportGuestContacts)
        self.ui.bt_guests_showBlacklist.clicked.connect(self.ShowGuestsBlacklist)
        self.ui.bt_guests_blacklist_addrem.clicked.connect(self.AddRemGuestToBlackList)

    def checkTodaysImpressions(self):
        today = datetime.now()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today.replace(hour=23, minute=59, second=59)
        print(today)
        result = self.SendQueryWithOneRow(f"SELECT COUNT(imp_id) FROM Impressions WHERE imp_datetime > '{today}' AND imp_datetime < '{today_end}'")
        self.ui.bt_notifications.setText(f'Встреч на сегодня: {result}')

    def showTodaysImpressions(self):
        self.eventHandler_bt_impressions()
        self.ui.tableWidget_main.setRowCount(0)

        today = datetime.now()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today.replace(hour=23, minute=59, second=59)

        result = self.SendQueryWithSomeRow(f"SELECT * FROM Impressions WHERE imp_datetime > '{today}' AND imp_datetime < '{today_end}'")
        for row_number, row_data in enumerate(result):
            self.ui.tableWidget_main.insertRow(row_number)
            for column_nmber, data in enumerate(row_data):
                self.ui.tableWidget_main.setItem(row_number, column_nmber, QTableWidgetItem(str(data)))





    def eventHandler_bt_servicesHist(self):
        self.ui.stackWid_Properties.setFixedHeight(300)
        self.markButtons(430)
        self.Mark_TableWidget(TableWidgetContent.ServicesHist.__len__(), TableWidgetContent.ServicesHist)
        self.Show_Table('ServicesHist')
        self.ui.stackWid_Actions.setCurrentIndex(0)
        self.ui.stackWid_Properties.setCurrentIndex(0)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.ServicesHist)


    def eventHandler_bt_meetings(self):
        self.ui.stackWid_Properties.setFixedHeight(350)
        self.markButtons(480)
        self.Mark_TableWidget(TableWidgetContent.Meetings.__len__(), TableWidgetContent.Meetings)
        self.Show_Table('Meetings')
        self.ui.stackWid_Actions.setCurrentIndex(1)
        self.ui.stackWid_Properties.setCurrentIndex(1)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Meetings)


    def eventHandler_bt_deals(self):
        self.ui.stackWid_Properties.setFixedHeight(400)
        self.markButtons(530)
        self.Mark_TableWidget(TableWidgetContent.Deals.__len__(), TableWidgetContent.Deals)
        self.ui.lb_deals_cbuyer.setText('Клиент')
        self.Show_Table('Deals')
        self.ui.stackWid_Actions.setCurrentIndex(2)
        self.ui.stackWid_Properties.setCurrentIndex(2)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Deals)


    def eventHandler_bt_deals_c(self):
        self.ui.stackWid_Properties.setFixedHeight(400)
        self.markButtons(530)
        self.Mark_TableWidget(TableWidgetContent.Deals_c.__len__(), TableWidgetContent.Deals_c)
        self.Show_Table('Deals_c')
        self.ui.lb_deals_cbuyer.setText('Покупатель')
        self.ui.stackWid_Actions.setCurrentIndex(2)
        self.ui.stackWid_Properties.setCurrentIndex(2)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Deals_c)

    def markButtons(self, height):
        self.ui.bt_copy.move(self.ui.bt_copy.x(), height)
        self.ui.bt_edit.move(self.ui.bt_edit.x(), height)
        self.ui.bt_delete.move(self.ui.bt_delete.x(), height)


    def eventHandler_bt_clients(self):
        self.ui.stackWid_Properties.setFixedHeight(460)
        self.markButtons(590)
        self.Mark_TableWidget(TableWidgetContent.Clients.__len__(), TableWidgetContent.Clients)
        self.Show_Table('Clients')
        self.ui.stackWid_Actions.setCurrentIndex(3)
        self.ui.stackWid_Properties.setCurrentIndex(3)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Clients)


    def eventHandler_bt_requests(self):
        self.Mark_TableWidget(TableWidgetContent.Requests.__len__(), TableWidgetContent.Requests)
        self.ui.stackWid_Properties.setFixedHeight(281)
        self.markButtons(411)
        self.Show_Table('Requests')
        self.ui.stackWid_Actions.setCurrentIndex(4)
        self.ui.stackWid_Properties.setCurrentIndex(4)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Requests)


    def eventHandler_bt_objects(self):
        self.ui.stackWid_Properties.setFixedHeight(521)
        self.markButtons(651)
        self.Mark_TableWidget(TableWidgetContent.Objects.__len__(), TableWidgetContent.Objects)
        self.Show_Table('Objects')
        self.ui.stackWid_Actions.setCurrentIndex(7)
        self.ui.stackWid_Properties.setCurrentIndex(7)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Objects)


    def eventHandler_bt_representatives(self):
        self.ui.stackWid_Properties.setFixedHeight(361)
        self.markButtons(491)
        self.Mark_TableWidget(TableWidgetContent.Representatives.__len__(), TableWidgetContent.Representatives)
        self.Show_Table('Representatives')
        self.ui.stackWid_Actions.setCurrentIndex(6)
        self.ui.stackWid_Properties.setCurrentIndex(6)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Representatives)


    def eventHandler_bt_objectsC(self):
        self.ui.stackWid_Properties.setFixedHeight(581)
        self.markButtons(711)
        self.Mark_TableWidget(TableWidgetContent.ObjectsC.__len__(), TableWidgetContent.ObjectsC)
        self.Show_Table('Objects_C')
        self.ui.stackWid_Actions.setCurrentIndex(5)
        self.ui.stackWid_Properties.setCurrentIndex(10)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.ObjectsC)


    def eventHandler_bt_guests(self):
        self.ui.stackWid_Properties.setFixedHeight(271)
        self.markButtons(401)
        self.Mark_TableWidget(TableWidgetContent.Guests.__len__(), TableWidgetContent.Guests)
        self.Show_Table('Guests')
        self.ui.stackWid_Actions.setCurrentIndex(8)
        self.ui.stackWid_Properties.setCurrentIndex(8)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Guests)


    def eventHandler_bt_impressions(self):
        self.ui.stackWid_Properties.setFixedHeight(331)
        self.markButtons(460)
        self.Mark_TableWidget(TableWidgetContent.Impressions.__len__(), TableWidgetContent.Impressions)
        self.Show_Table('Impressions')
        self.ui.stackWid_Actions.setCurrentIndex(9)
        self.ui.stackWid_Properties.setCurrentIndex(9)
        self.ui.cb_column.clear()
        self.ui.cb_column.addItems(TableWidgetContent.Impressions)


    def GetDataFromCurrentRow(self):
        """Отобразить выбранную запись в окне свойств"""
        cur_row = self.ui.tableWidget_main.currentRow()

        match(self.currentTable):
            case "ServicesHist":
                value = self.ui.tableWidget_main.item(cur_row, 0).text()
                self.ui.tb_servicesHist_id.setText(value)
                self.ui.tb_servicesHist_client.setText(self.ui.tableWidget_main.item(cur_row, 1).text())
                self.ui.dtpicker_servicesHist_datetime.setDateTime(QDateTime.fromString(self.ui.tableWidget_main.item(cur_row, 2).text(), "yyyy-MM-dd HH:mm:ss"))
                self.ui.tb_servicesHist_service.setText(self.ui.tableWidget_main.item(cur_row, 3).text())
                self.ui.tb_servicesHist_cost.setText(self.ui.tableWidget_main.item(cur_row, 4).text())

            case "Meetings":
                self.ui.tb_meetings_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.dtpicker_meetings_datetime.setDateTime(QDateTime.fromString(self.ui.tableWidget_main.item(cur_row, 1).text(), "yyyy-MM-dd HH:mm:ss"))

                self.ui.tb_meetings_name.setText(self.ui.tableWidget_main.item(cur_row, 2).text())
                self.ui.cb_meetings_status.setCurrentText(self.ui.tableWidget_main.item(cur_row, 3).text())

                self.ui.tb_meetings_desc.setPlainText(self.ui.tableWidget_main.item(cur_row, 4).text())

            case "Clients":
                self.ui.tb_client_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.tb_client_lname.setText(self.ui.tableWidget_main.item(cur_row, 1).text())
                self.ui.tb_client_fname.setText(self.ui.tableWidget_main.item(cur_row, 2).text())
                self.ui.tb_client_patronymic.setText(self.ui.tableWidget_main.item(cur_row, 3).text())
                self.ui.tb_client_passport.setText(self.ui.tableWidget_main.item(cur_row, 4).text())
                self.ui.tb_client_phone.setText(self.ui.tableWidget_main.item(cur_row, 5).text())
                self.ui.tb_client_email.setText(self.ui.tableWidget_main.item(cur_row, 6).text())
                self.ui.tb_client_address.setText(self.ui.tableWidget_main.item(cur_row, 7).text())

            case "Requests":
                self.ui.tb_req_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.tb_req_client.setText(self.ui.tableWidget_main.item(cur_row, 1).text())
                self.ui.tb_req_details.setText(self.ui.tableWidget_main.item(cur_row, 2).text())

            case "Objects":
                self.ui.tb_objects_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.tb_objects_name.setText(self.ui.tableWidget_main.item(cur_row, 1).text())
                self.ui.tb_objects_representative.setText(self.ui.tableWidget_main.item(cur_row, 2).text())
                self.ui.cb_objects_second.setCurrentText(self.ui.tableWidget_main.item(cur_row, 3).text())
                self.ui.cb_objects_type.setCurrentText(self.ui.tableWidget_main.item(cur_row, 4).text())
                self.ui.cb_objects_dtype.setCurrentText(self.ui.tableWidget_main.item(cur_row, 5).text())
                self.ui.tb_objects_square.setText(self.ui.tableWidget_main.item(cur_row, 6).text())
                self.ui.sb_objects_rooms.setValue(int(float(self.ui.tableWidget_main.item(cur_row, 7).text())))
                self.ui.tb_objects_price.setText(self.ui.tableWidget_main.item(cur_row, 8).text())
                self.ui.tb_objects_address.setText(self.ui.tableWidget_main.item(cur_row, 9).text())
                self.ui.tb_objects_desc.setPlainText(self.ui.tableWidget_main.item(cur_row, 10).text())
                self.ui.tb_objects_addprops.setText(self.ui.tableWidget_main.item(cur_row, 11).text())

            case "Representatives":
                self.ui.tb_representatives_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.tb_representatives_name.setText(self.ui.tableWidget_main.item(cur_row, 1).text())
                self.ui.tb_representatives_phone.setText(self.ui.tableWidget_main.item(cur_row, 2).text())
                self.ui.tb_representatives_email.setText(self.ui.tableWidget_main.item(cur_row, 3).text())
                self.ui.tb_representatives_website.setText(self.ui.tableWidget_main.item(cur_row, 4).text())
                self.ui.tb_representatives_telegram.setText(self.ui.tableWidget_main.item(cur_row, 5).text())
                self.ui.tb_representatives_vk.setText(self.ui.tableWidget_main.item(cur_row, 6).text())

            case "Deals":
                self.ui.tb_deals_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.dtpicker_deals_datetime.setDateTime(QDateTime.fromString(self.ui.tableWidget_main.item(cur_row, 1).text(), "yyyy-MM-dd"))
                self.ui.tb_deals_name.setText(self.ui.tableWidget_main.item(cur_row, 2).text())
                self.ui.cb_deals_type.setCurrentText(self.ui.tableWidget_main.item(cur_row, 3).text())
                self.ui.tb_deals_object.setText(self.ui.tableWidget_main.item(cur_row, 4).text())
                self.ui.tb_deals_cost.setText(self.ui.tableWidget_main.item(cur_row, 5).text())
                self.ui.tb_deals_cpercent.setText(self.ui.tableWidget_main.item(cur_row, 6).text())
                self.ui.tb_deals_csum.setText(self.ui.tableWidget_main.item(cur_row, 7).text())
                self.ui.tb_deals_client.setText(self.ui.tableWidget_main.item(cur_row, 8).text())
                self.ui.tb_deals_status.setText(self.ui.tableWidget_main.item(cur_row, 9).text())

            case "Deals_c":
                self.ui.tb_deals_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.dtpicker_deals_datetime.setDateTime(QDateTime.fromString(self.ui.tableWidget_main.item(cur_row, 1).text(), "yyyy-MM-dd"))
                self.ui.tb_deals_name.setText(self.ui.tableWidget_main.item(cur_row, 2).text())
                self.ui.cb_deals_type.setCurrentText(self.ui.tableWidget_main.item(cur_row, 3).text())
                self.ui.tb_deals_object.setText(self.ui.tableWidget_main.item(cur_row, 4).text())
                self.ui.tb_deals_cost.setText(self.ui.tableWidget_main.item(cur_row, 5).text())
                self.ui.tb_deals_cpercent.setText(self.ui.tableWidget_main.item(cur_row, 6).text())
                self.ui.tb_deals_csum.setText(self.ui.tableWidget_main.item(cur_row, 7).text())
                self.ui.tb_deals_client.setText(self.ui.tableWidget_main.item(cur_row, 8).text())
                self.ui.tb_deals_status.setText(self.ui.tableWidget_main.item(cur_row, 9).text())

            case "Objects_C":
                self.ui.tb_objectsc_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.tb_objectsc_cadastral.setText(self.ui.tableWidget_main.item(cur_row, 1).text())
                self.ui.tb_objectsc_owner.setText(self.ui.tableWidget_main.item(cur_row, 2).text())
                self.ui.tb_objectsc_name.setText(self.ui.tableWidget_main.item(cur_row, 3).text())
                self.ui.cb_objectsc_type.setCurrentText(self.ui.tableWidget_main.item(cur_row, 4).text())
                self.ui.tb_objectsc_square.setText(self.ui.tableWidget_main.item(cur_row, 5).text())
                self.ui.sb_objectsc_rooms.setValue(int(float(self.ui.tableWidget_main.item(cur_row, 6).text())))
                self.ui.tb_objectsc_price.setText(self.ui.tableWidget_main.item(cur_row, 7).text())
                self.ui.dtpicker_objectsc_addate.setDateTime(QDateTime.fromString(self.ui.tableWidget_main.item(cur_row, 8).text(), "yyyy-MM-dd"))
                self.ui.cb_objectsc_dtype.setCurrentText(self.ui.tableWidget_main.item(cur_row, 9).text())
                self.ui.cb_objectsc_status.setCurrentText(self.ui.tableWidget_main.item(cur_row, 10).text())
                self.ui.tb_objectsc_address.setText(self.ui.tableWidget_main.item(cur_row, 11).text())
                self.ui.tb_objectsc_desc.setPlainText(self.ui.tableWidget_main.item(cur_row, 12).text())


            case "Guests":
                self.ui.tb_guests_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.tb_guests_fullname.setText(self.ui.tableWidget_main.item(cur_row, 1).text())
                self.ui.dtpicker_guests_added.setDateTime(QDateTime.fromString(self.ui.tableWidget_main.item(cur_row, 2).text(), "yyyy-MM-dd HH:mm:ss"))
                self.ui.tb_guests_phone.setText(self.ui.tableWidget_main.item(cur_row, 3).text())
                blacklist = self.ui.tableWidget_main.item(cur_row, 4).text()
                if blacklist == 'False': self.ui.cb_guests_blacklist.setChecked(True)
                else: self.ui.cb_guests_blacklist.setChecked(False)

            case "Impressions":
                self.ui.tb_impressions_id.setText(self.ui.tableWidget_main.item(cur_row, 0).text())
                self.ui.dtpicker_impressions_datetime.setDateTime(QDateTime.fromString(self.ui.tableWidget_main.item(cur_row, 1).text(), "yyyy-MM-dd HH:mm:ss"))
                self.ui.tb_imressions_object.setText(self.ui.tableWidget_main.item(cur_row, 2,).text())
                self.ui.tb_impressions_guests.setText(self.ui.tableWidget_main.item(cur_row, 3).text())
                self.ui.cb_impressions_finished.setText(self.ui.tableWidget_main.item(cur_row, 4).text())


    def EditCurrentRow(self):
        """Отредактировать запись"""

        match(self.currentTable):
            case "Clients":
                id = self.ui.tb_client_id.text()
                lname = self.ui.tb_client_lname.text()
                fname = self.ui.tb_client_fname.text()
                patronymic = self.ui.tb_client_patronymic.text()
                phone = self.ui.tb_client_phone.text()
                email = self.ui.tb_client_email.text()
                address = self.ui.tb_client_address.text()

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET cl_lname = '{lname}', "
                                            f"cl_fname = '{fname}', cl_patronymic = '{patronymic}', "
                                            f"cl_phone = '{phone}', cl_email = '{email}', "
                                            f"cl_address = '{address}' WHERE cl_id = {id}")

            case "Meetings":
                id = self.ui.tb_meetings_id.text()
                dttime = (self.ui.dtpicker_meetings_datetime.dateTime()).toString("yyyy-MM-dd HH:mm")
                name = self.ui.tb_meetings_name.text()
                status = self.ui.cb_meetings_status.currentText()
                desc = self.ui.tb_meetings_desc.toPlainText()

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET met_datetime = '{dttime}', met_name = '{name}', met_status = '{status}', met_desc = '{desc}' WHERE met_id = {id}")

            case "ServicesHist":
                id = self.ui.tb_servicesHist_id.text()
                client = self.ui.tb_servicesHist_client.text()
                dttime = self.ui.dtpicker_servicesHist_datetime.text()
                service = self.ui.tb_servicesHist_service.text()
                cost = self.ui.tb_servicesHist_cost.text()

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET sh_client = {client}, "
                                            f"sh_datetime = '{dttime}', sh_service = '{service}', "
                                            f"sh_cost = '{cost}' WHERE sh_id = {id}")

            case "Requests":
                id = self.ui.tb_req_id.text()
                client = self.ui.tb_req_client.text()
                details = self.ui.tb_req_details.text()

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET req_client = {client}, "
                                            f"req_details = '{details}' WHERE req_id = {id}")

            case "Objects":
                id = self.ui.tb_objects_id.text()
                name = self.ui.tb_objects_name.text()
                representative = self.ui.tb_objects_representative.text()
                if self.ui.cb_objects_second.currentText() == 'Да':
                    second = 'True'
                else: second = 'False'
                type = self.ui.cb_objects_type.currentText()
                dtype = self.ui.cb_objects_dtype.currentText()
                square = self.ui.tb_objects_square.text()
                rooms = self.ui.sb_objects_rooms.value()
                price = self.ui.tb_objects_price.text()
                address = self.ui.tb_objects_address.text()
                desc = self.ui.tb_objects_desc.toPlainText()
                addprops = self.ui.tb_objects_addprops.text()

                if addprops == 'None': addprops = 'Null'

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET obj_name = '{name}', "
                                            f"obj_representative  = {representative}, obj_second  = {second}, "
                                            f"obj_type  = '{type}', obj_dtype  = '{dtype}', obj_square  = {square}, "
                                            f"obj_rooms = {rooms}, obj_price = {price}, obj_address = '{address}', "
                                            f"obj_desc = '{desc}', obj_addpr = {addprops} WHERE obj_id = {id}")


            case "Representatives":
                id = self.ui.tb_representatives_id.text()
                name = self.ui.tb_representatives_name.text()
                phone = self.ui.tb_representatives_phone.text()
                email = self.ui.tb_representatives_email.text()
                website = self.ui.tb_representatives_website.text()
                telegram = self.ui.tb_representatives_telegram.text()
                vk = self.ui.tb_representatives_vk.text()

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET "
                                            f"rep_name = '{name}', rep_phone = '{phone}', rep_email = '{email}',"
                                            f"rep_website = '{website}', rep_telegram = '{telegram}', "
                                            f"rep_vk = '{vk}' WHERE rep_id = {id}")

            case "Deals":
                id = self.ui.tb_deals_id.text()
                date = (self.ui.dtpicker_deals_datetime.dateTime()).toString("yyyy-MM-dd HH:mm")
                name = self.ui.tb_deals_name.text()
                type = self.ui.cb_deals_type.currentText()
                object = self.ui.tb_deals_object.text()
                price = self.ui.tb_deals_cost.text()
                cpercent = self.ui.tb_deals_cpercent.text()
                csum = self.ui.tb_deals_csum.text()
                client = self.ui.tb_deals_client.text()
                status = self.ui.tb_deals_status.text()

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET "
                                            f"deal_date = '{date}', deal_name = '{name}', deal_type = '{type}', deal_object = {object}, "
                                            f"deal_price = {price}, deal_cpercent = {cpercent}, deal_csum = {csum}, deal_client = {client},"
                                            f" deal_status = '{status}' WHERE deal_id = {id}")

            case "Deals_c":
                id = self.ui.tb_deals_id.text()
                date = (self.ui.dtpicker_deals_datetime.dateTime()).toString("yyyy-MM-dd HH:mm")
                name = self.ui.tb_deals_name.text()
                type = self.ui.cb_deals_type.currentText()
                object = self.ui.tb_deals_object.text()
                price = self.ui.tb_deals_cost.text()
                cpercent = self.ui.tb_deals_cpercent.text()
                csum = self.ui.tb_deals_csum.text()
                buyer = self.ui.tb_deals_client.text()
                status = self.ui.tb_deals_status.text()

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET "
                                            f"deal_date = '{date}', deal_name = '{name}', deal_type = '{type}', deal_object = {object}, "
                                            f"deal_price = {price}, deal_cpercent = {cpercent}, deal_csum = {csum}, deal_buyer = {buyer},"
                                            f" deal_status = '{status}' WHERE deal_id = {id}")

            case "Objects_C":

                id = self.ui.tb_objectsc_id.text()
                owner = self.ui.tb_objectsc_owner.text()
                name = self.ui.tb_objectsc_name.text()
                type = self.ui.cb_objectsc_type.currentText()
                square = self.ui.tb_objectsc_square.text()
                rooms = self.ui.sb_objectsc_rooms.text()
                price = self.ui.tb_objectsc_price.text()
                adddate = (self.ui.dtpicker_objectsc_addate.date()).toString("yyyy-MM-dd")
                target = self.ui.cb_objectsc_type.currentText()
                status = self.ui.cb_objectsc_status.currentText()
                address = self.ui.tb_objectsc_address.text()
                desc = self.ui.tb_objectsc_desc.toPlainText()

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET obj_owner = {owner}, obj_name = '{name}', "
                                            f"obj_type = '{type}', obj_square  = {square}, obj_rooms = {rooms}, "
                                            f"obj_price  = {price}, obj_adddate  = '{adddate}', obj_target  = '{target}', "
                                            f"obj_status = '{status}', obj_address = '{address}', obj_desc = '{desc}' WHERE obj_id = {id}")


            case "Guests":
                id = self.ui.tb_guests_id.text()
                fullname = self.ui.tb_guests_fullname.text()
                phone = self.ui.tb_guests_phone.text()
                blacklist = str(self.ui.cb_guests_blacklist.isChecked())

                self.SendQueryWithoutAnswer(f"UPDATE {self.currentTable} SET gue_fullname = '{fullname}', "
                                            f"gue_phone = '{phone}', gue_blacklist = {blacklist} WHERE gue_id = {id}")


    def DeleteDataFromCurrentRow(self):
        """Удалить выбранную строку"""
        try:
            # ID Записи в БД
            id = self.ui.tableWidget_main.item(self.ui.tableWidget_main.currentRow(), 0).text()
            cur = self.connect_pg()

            # Формирование запроса с текущей таблицей и нужной записью
            self.sqlquery = F"DELETE FROM {self.currentTable} CASCADE WHERE {self.ui.tableWidget_main.horizontalHeaderItem(0).text()} = {id}"

            # Подтверждение удаления записи
            self.show_questionMessage('Подтвердите действие',
                                      F'Из таблицы {self.currentTable} будет удалена запись с уникальным идентификатором {id}.'
                                                         F'Это так же приведет к удалению других связанных записей. Вы уверены?')

            # Отказ
            if self.msg.exec() == QMessageBox.StandardButton.No:
                return
            # Согласие
            else:
                cur.execute(self.sqlquery)
                self.connection.commit()

        except(psycopg2.OperationalError):
            self.show_errorMessage('Произошла ошибка',
                              'Произошла ошибка выполнения запроса к базе данных.')


    def ShowAddDialog(self, Ui_Dialog):
        """Алгоритмы работы диалогов добавления записей"""
        try:
            if self.currentTable == 'Deals_c':
                Ui_Dialog = Ui_Dialog_Deals_c_add()

            # Установка типа окна
            app = QtWidgets.QDialog()
            Ui_Dialog.setupUi(app)

            # Проверка на принадлженость классу интерфейса добавления объектов
            if isinstance(Ui_Dialog, Ui_Dialog_Objects_add):
                Ui_Dialog.bt_upload_files.clicked.connect(lambda: self.OpenObjectPictures())

            # Запуск окна
            app.setStyleSheet(open('stylesDialogs.qss').read())
            app.show()
            app.exec()


            match(Ui_Dialog):
                case Ui_Dialog_Clients_registration():
                    v1 = Ui_Dialog.te_cl_fname.toPlainText() # Имя
                    v2 = Ui_Dialog.te_cl_lname.toPlainText() # Фамилия
                    v3 = Ui_Dialog.te_cl_patr.toPlainText() # Отчество
                    v4 = Ui_Dialog.te_cl_passport.toPlainText() # Паспорт
                    v5 = Ui_Dialog.te_cl_phone.toPlainText() # Телефон
                    v6 = Ui_Dialog.te_cl_email.toPlainText() # Эл почта
                    v7 = Ui_Dialog.te_cl_address.toPlainText() # Адрес

                    # Проверка на пустой ввод
                    if not v1 or not v2 or not v3 or not v4 or not v5 or not v6 or not v7:
                        self.show_errorMessage('Произошла ошибка',
                                               'Одно или несколько из вводимых значений пустые. '
                                               'Проверьте правильность ввода.')
                        return

                    #  Массив столбцов для перевода его в строку
                    tmp_list = DataSets.TableWidgetContent.Clients.copy()

                    # Сборка значений
                    values = F"'{v1}', '{v2}', '{v3}', '{v4}', '{v5}', '{v6}', '{v7}'"

                    print(values) # Отладка


                case Ui_Dialog_Representatives_add():
                    v1 = Ui_Dialog.te_rep_fullname.toPlainText() # ФИО
                    v2 = Ui_Dialog.te_rep_phone.toPlainText() # Телефон
                    v3 = Ui_Dialog.te_rep_email.toPlainText() # Эл почта
                    v4 = Ui_Dialog.te_rep_website.toPlainText() # Вебсайт
                    v5 = Ui_Dialog.te_rep_telegram.toPlainText() # Телеграм
                    v6 = Ui_Dialog.te_rep_vk.toPlainText() # ВК

                    if not v1 or not v2:
                        self.show_errorMessage('Произошла ошибка',
                                               'Одно или несколько из вводимых значений пустые. '
                                               'Проверьте правильность ввода.')

                    tmp_list = DataSets.TableWidgetContent.Representatives.copy()
                    values = F"'{v1}', '{v2}', '{v3}', '{v4}', '{v5}', '{v6}'"


                case Ui_Dialog_Meetings_add():
                    v1 = Ui_Dialog.dtpicker_met_datetime.text()
                    v2 = Ui_Dialog.te_met_name.toPlainText()
                    v3 = 'Ожидается'
                    v4 = Ui_Dialog.te_met_desc.toPlainText()

                    tmp_list = DataSets.TableWidgetContent.Meetings.copy()

                    values = F"'{v1}', '{v2}', '{v3}', '{v4}'"


                    if not v1 or not v2 or not v3 or not v4:
                        self.show_errorMessage('Произошла ошибка',
                                               'Одно или несколько из вводимых значений пустые. '
                                               'Проверьте правильность ввода.')


                case Ui_Dialog_ServiceHist_add():
                    v1 = Ui_Dialog.te_sh_client.toPlainText()
                    v2 = Ui_Dialog.dtpicker_sh_date.text()
                    v3 = Ui_Dialog.te_sh_service.toPlainText()
                    v4 = Ui_Dialog.te_sh_cost.toPlainText()

                    tmp_list = DataSets.TableWidgetContent.ServicesHist.copy()
                    values = F"{v1}, '{v2}', '{v3}', {v4}"


                    if not v1 or not v2 or not v3 or not v4:
                        self.show_errorMessage('Произошла ошибка',
                                               'Одно или несколько из вводимых значений пустые. '
                                               'Проверьте правильность ввода.')


                case Ui_Dialog_Requests_add():
                    v1 = Ui_Dialog.te_req_client.toPlainText()
                    v2 = Ui_Dialog.te_req_details.toPlainText()

                    tmp_list = DataSets.TableWidgetContent.Requests.copy()
                    values = F"'{v1}', '{v2}'"


                    if not v1 or not v2:
                        self.show_errorMessage('Произошла ошибка',
                                               'Одно или несколько из вводимых значений пустые. '
                                               'Проверьте правильность ввода.')

                case Ui_Dialog_Objects_add():

                    v1 = Ui_Dialog.te_obj_cadastral.text()
                    v2 = Ui_Dialog.te_obj_owner.text()
                    v3 = Ui_Dialog.te_obj_name.text()
                    v4 = Ui_Dialog.cb_obj_type.currentText()
                    v5 = Ui_Dialog.sp_obj_square.value()
                    v6 = Ui_Dialog.sp_obj_rooms.value()
                    v7 = Ui_Dialog.te_obj_price.text()
                    v8 = datetime.now()
                    v9 = Ui_Dialog.cb_obj_dtype.currentText()
                    v10 = "Актуально"
                    v11 = Ui_Dialog.te_obj_address.text()
                    v12 = Ui_Dialog.te_obj_desc.toPlainText()


                    tmp_list = DataSets.TableWidgetContent.ObjectsC.copy()

                    values = F"'{v1}', {v2}, '{v3}', '{v4}', {v5}, {v6}, {v7}, '{v8}', '{v9}', '{v10}', '{v11}', '{v12}', null"

                    if (not v1 or not v2 or not v3 or not v4 or not v5 or not v6
                            or not v7 or not v8 or not v9 or not v10 or not v11):
                        self.show_errorMessage('Произошла ошибка',
                                               'Одно или несколько из вводимых значений пустые. '
                                               'Проверьте правильность ввода.')


                    # Если доп.данные - отключено
                    if Ui_Dialog.cb_obj_needAP.isChecked() == True:
                        del tmp_list[12]
                    else:
                        valuesAP = f"{Ui_Dialog.sp_obj_bathrooms.value()}, " if Ui_Dialog.sp_obj_bathrooms.value() else "null, "
                        valuesAP += f"{Ui_Dialog.sp_obj_floor.value()}, " if Ui_Dialog.sp_obj_floor.value() else "null, "
                        valuesAP += "True, " if Ui_Dialog.cb_obj_logic.isChecked() == True else "False, "
                        valuesAP += "True, " if Ui_Dialog.cb_obj_landplot.isChecked() == True else "False, "
                        valuesAP += "True, " if Ui_Dialog.cb_obj_garage.isChecked() == True else "False, "
                        valuesAP += f"{Ui_Dialog.sp_obj_ldsquare.value()}, " if Ui_Dialog.sp_obj_ldsquare.value() == True else "null, "
                        valuesAP += f"{Ui_Dialog.sp_obj_parking.value()}, " if Ui_Dialog.sp_obj_parking.value() else "null, "
                        valuesAP += f"{Ui_Dialog.dtpicker_obj_buildyear.text()}, " if Ui_Dialog.dtpicker_obj_buildyear.text() else "null, "
                        valuesAP += "True, " if Ui_Dialog.cb_obj_basement.isChecked() == True else "null, "
                        valuesAP += f"'{datetime.now()}', "
                        valuesAP += f"{Ui_Dialog.sp_obj_kitchensquare.value()}, " if Ui_Dialog.sp_obj_kitchensquare.value() else "null, "
                        valuesAP += "True, " if Ui_Dialog.cb_obj_garbagech.isChecked() == True else "False, "
                        valuesAP += f"'{Ui_Dialog.cb_obj_btype.currentText()}', " if Ui_Dialog.cb_obj_btype.currentText() else "null, "
                        valuesAP += f"{Ui_Dialog.sp_obj_cheight.value()}, " if Ui_Dialog.sp_obj_cheight.value() else "null, "
                        valuesAP += "True, " if Ui_Dialog.cb_obj_accidentrate.isChecked() == True else "null, "
                        valuesAP += f"'{Ui_Dialog.te_obj_repair.toPlainText()}'" if Ui_Dialog.te_obj_repair.toPlainText() else "null"

                        print(valuesAP) # Для отладки

                        # Создание массива названий столбцов без ключевого
                        tmp_listAP = DataSets.TableWidgetContent.Object_addproperties.copy()
                        del tmp_listAP[0]

                        column_listAP = ', '.join(tmp_listAP) # Конвертирвоание массива строк в цельную строку

                        # Добавление доп.свойств для объекта
                        self.SendQueryWithoutAnswer(f"INSERT INTO Object_addproperties({column_listAP}) VALUES({valuesAP})")

                case Ui_Dialog_Deals_add():
                    v1 = datetime.now()
                    v2 = Ui_Dialog.te_deal_name.toPlainText()
                    v3 = Ui_Dialog.cb_deal_type.currentText()
                    v4 = Ui_Dialog.te_deal_object.toPlainText()
                    v5 = Ui_Dialog.te_deal_cost.toPlainText()
                    v6 = Ui_Dialog.sp_deal_cpercent.value()
                    v7 = Ui_Dialog.te_deal_csum.toPlainText()
                    v8 = Ui_Dialog.te_deal_client.toPlainText()
                    v9 = 'null'


                    tmp_list = DataSets.TableWidgetContent.Deals.copy()
                    values = F"'{v1}', '{v2}', '{v3}', {v4}, {v5}, {v6}, {v7}, {v8}, {v9}"

                case Ui_Dialog_Deals_c_add():
                    v1 = datetime.now()
                    v2 = Ui_Dialog.te_deal_c_name.toPlainText()
                    v3 = Ui_Dialog.cb_deal_c_type.currentText()
                    v4 = Ui_Dialog.te_deal_c_object.toPlainText()
                    v5 = Ui_Dialog.te_deal_c_cost.toPlainText()
                    v6 = Ui_Dialog.sp_deal_c_cpercent.value()
                    v7 = Ui_Dialog.te_deal_c_csum.toPlainText()
                    v8 = Ui_Dialog.te_deal_c_buyer.toPlainText()
                    v9 = 'null'


                    tmp_list = DataSets.TableWidgetContent.Deals_c.copy()
                    values = F"'{v1}', '{v2}', '{v3}', {v4}, {v5}, {v6}, {v7}, {v8}, {v9}"

                case Ui_Dialog_Impressions_add():
                    v1 = Ui_Dialog.dtpicker_imp_datetime.text()
                    v2 = Ui_Dialog.te_imp_object.toPlainText()
                    v3 = Ui_Dialog.te_imp_guest.toPlainText()
                    v4 = 'false'

                    if not v1 or not v2 or not v3:
                        self.show_errorMessage('Произошла ошибка',
                                               'Одно или несколько из вводимых значений пустые. '
                                               'Проверьте правильность ввода.')


                    tmp_list = DataSets.TableWidgetContent.Impressions.copy()
                    values = F"'{v1}', {v2}, {v3}, {v4}"

                case Ui_Dialog_Guests_add():
                    v1 = Ui_Dialog.te_gue_fullname.toPlainText()
                    v2 = datetime.now().date()
                    v3 = Ui_Dialog.te_gue_phone.toPlainText()
                    v4 = 'False'


                    tmp_list = DataSets.TableWidgetContent.Guests.copy()
                    values = F"'{v1}', '{v2}', '{v3}', {v4}"

            # Если массив с путями к фото не пуст - они добавляются в БД
            if self.file_paths.__len__() != 0:
                self.ImportPicturesToDB()

            del tmp_list[0]

            column_list = ', '.join(tmp_list)

            sqlquery = F"INSERT INTO {self.currentTable}({column_list}) VALUES({values})"
            self.SendQueryWithoutAnswer(sqlquery)

        except(AttributeError):
            pass

    def ExportGuestContacts(self):
        """Копировать контактные данные гостя в буфер обмена"""

        # Выделенная строка
        cur_row = self.ui.tableWidget_main.currentRow()

        # Переменная с контактами
        contacts = f"""
        ID Клиента: {self.ui.tableWidget_main.item(cur_row, 0).text()}
        ФИО: {self.ui.tableWidget_main.item(cur_row, 1).text()}
        Номер телефона: {self.ui.tableWidget_main.item(cur_row, 3).text()}
        """

        # Копирование строки в буфер обмена
        pyperclip.copy(contacts)


    def AddRemGuestToBlackList(self):
        "Добавить или удалить из ЧС гостя"

        # Текущая строка и ID
        cur_row = self.ui.tableWidget_main.currentRow()
        id = self.ui.tableWidget_main.item(cur_row, 0).text()

        # Проверка на черный список
        isBlackList = self.SendQueryWithOneRow(f'SELECT get_guest_blacklist_status({id})')

        # Если нет ЧС - ставится ЧС и наоборот
        if isBlackList == 'True':
            self.SendQueryWithoutAnswer(f"UPDATE Guests SET gue_blacklist = False WHERE gue_id = {id}")
        else:
            self.SendQueryWithoutAnswer(f"UPDATE Guests SET gue_blacklist = True WHERE gue_id = {id}")


    def ShowGuestsBlacklist(self):
        "Показать черный список гостей"

        self.ui.tableWidget_main.setRowCount(0)
        self.Show_Table('Guests WHERE gue_blacklist = True')


    def OpenObjectPictures(self):
        """Открыть диалоговое окно выбора
        фото и записать пути к ним в массив"""



        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_names = dialog.getOpenFileNames(self, "Выберите фото объекта")

        self.file_paths.clear() # Очистка путей
        self.file_paths = file_names[0] # Запись путей к файлам

        # Для отладки
        print(file_names[0])
        print(self.file_paths[1])


    def ImportPicturesToDB(self):
        """Импорт картинок в БД"""

        # Для каждого пусти в массиве путей
        for picture in range(self.file_paths.__len__()):

            # Путь к фото
            image_path = self.file_paths[picture]

            image = Image.open(image_path) # Открыть фото
            image_bytes = io.BytesIO() # Переменная для байт
            image.save(image_bytes, format("jpeg")) # Сохранение фото в байтах
            image_data = Binary(image_bytes.getvalue()) # Сохранение фото в бинарнике

        # ID Объекта будет передаваться
            self.SendQueryWithoutAnswer(f"INSERT INTO Objects_pictures(pic_object, pic_data) VALUES(1, {image_data})")

    def SwitchPic(self, id, offset):
        cur = self.connect_pg()


        cur.execute(f"SELECT pic_data FROM Objects_pictures WHERE pic_object = {id} OFFSET {offset}")
        result = cur.fetchone()[0]

        return result

    def ExportPicturesFromDB(self):
        """Тестовая функция отображения фото из БД"""

        id = self.ui.tb_objectsc_id.text()
        if(not id):
            return
        self.count = int(self.SendQueryWithOneRow(f'SELECT COUNT(pic_data) FROM Objects_pictures WHERE pic_object = {id}'))
        self.offset = 0
        dialog = Ui_Dialog_pictures()
        app = QtWidgets.QDialog()
        dialog.setupUi(app)
        app.setStyleSheet(open('stylesDialogs.qss').read())
        app.show()


        def pixmaplb():
            if (self.offset >= self.count or self.offset == 0):
                self.offset = 1
            image_data = self.SwitchPic(id, self.offset)

            # Загрузка фото в бинарнике в надпись
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            image = pixmap.toImage()
            image = image.convertToFormat(QImage.Format.Format_RGB888)

            dialog.lb_pix.setPixmap(QPixmap.fromImage(image))
            self.offset += 1



        def pixmaplb_back():
            if (self.offset >= self.count or self.offset <= 0):
                self.offset = 1
            image_data = self.SwitchPic(id, self.offset)

            # Загрузка фото в бинарнике в надпись
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            image = pixmap.toImage()
            image = image.convertToFormat(QImage.Format.Format_RGB888)

            dialog.lb_pix.setPixmap(QPixmap.fromImage(image))
            self.offset -= 1

        def delPhoto():
            self.SendQueryWithoutAnswer(F'DELETE FROM Objects_pictures WHERE pic_object '
                                        F'IN(SELECT pic_data FROM Objects_pictures WHERE pic_object = {self.id} OFFSET {self.offset - 1})')

        dialog.bt_next.clicked.connect(lambda: pixmaplb())
        dialog.bt_back.clicked.connect(lambda: pixmaplb_back())
        dialog.bt_delphoto.clicked.connect(lambda: delPhoto())

        # Запуск окна

        app.exec()

    def MakeReport(self):
        cur = self.connect_pg()

        cur.execute('SELECT ')


    def SendQueryWithoutAnswer(self, query):
        """Отправка запросов без ответа"""
        cur = self.connect_pg()
        cur.execute(query)
        self.connection.commit()



    def Mark_TableWidget_Clear(self):
        """Приводит TableWidget_main в исходное состояние"""
        self.ui.tableWidget_main.clear()
        self.ui.tableWidget_main.setRowCount(0)


    def Mark_TableWidget(self, columncount: int, TableName: list):
        """Разметка TableWidget_main для вывода записей из БД"""
        self.Mark_TableWidget_Clear()
        self.ui.tableWidget_main.setColumnCount(columncount)
        header = self.ui.tableWidget_main.horizontalHeader()
        self.ui.tableWidget_main.setHorizontalHeaderLabels(TableName)
        self.ui.tableWidget_main.verticalHeader().setDefaultSectionSize(30)

        # Установка ширины id-столбцов
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for i in range(1, columncount):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)


    def SendQueryWithOneRow(self, query):
        "Запрос с ответом в виде 1 строки"
        cur = self.connect_pg()

        cur.execute(query)
        result = cur.fetchone()
        result = str(result[0])

        return result

    def SendQueryWithSomeRow(self, query):
        "Запрос с ответом в виде 1 строки"
        cur = self.connect_pg()

        cur.execute(query)
        result = cur.fetchall()

        return result


    def Show_Table(self, table):
        """Собрать записи и вывести их в tablewidget"""
        try:
            self.checkTodaysImpressions()

            self.currentTable = table
            cur = self.connect_pg()

            self.sqlquery = F"SELECT * FROM {table}"

            cur.execute(self.sqlquery)
            result = cur.fetchall()

            for row_number, row_data in enumerate(result):
                self.ui.tableWidget_main.insertRow(row_number)
                for column_nmber, data in enumerate(row_data):
                    self.ui.tableWidget_main.setItem(row_number, column_nmber, QTableWidgetItem(str(data)))
        except(AttributeError):
            return


    def connect_pg(self):
        """Организует подключение к базе данных"""

        # В конечном варианте будет осуществляться почти вручную
        try:
            self.connection = psycopg2.connect(
                dbname = 'redbv3',
                user = 'postgres',
                password = 'password',
                host = '172.17.0.2',
                port = '5432'
            )

            cur = self.connection.cursor()
            return cur

        except psycopg2.OperationalError:
            self.show_errorMessage('Произошла ошибка',
                                   'При подключении к базе данных произошла ошибка. '
                                   'Проверьте подключение к интернету или обратитесь '
                                   'к своему системному администратору.')



    def show_questionMessage(self, QuestionTitle, QuestionDesc):
        """Вывести диалог с вопросом"""
        self.msg = QMessageBox()
        self.msg.setWindowTitle(QuestionTitle)
        self.msg.setText(QuestionDesc)
        self.msg.setIcon(QMessageBox.Icon.Question)
        self.msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        # self.msg.exec()


    def show_warningMessage(self, WarningTitle , WarningDesc):
        """Вывести диалог с предупреждением"""
        msg = QMessageBox()
        msg.setWindowTitle(WarningTitle)
        msg.setText(WarningDesc)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.exec()


    def show_errorMessage(self, ErrorTitle, ErrorDesc):
        """Вывести диалог с ошибкой"""
        msg = QMessageBox()
        msg.setWindowTitle(ErrorTitle)
        msg.setText(F"{ErrorDesc}")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()
        returnval = msg.exec()



if __name__ == '__main__':


    app = QApplication([])

    print(QStyleFactory.keys())
    auth_window = AuthorizationWindow()
    auth_window.show()
    window = MainWindow()
    window.setStyleSheet(open('styles2.qss').read())

    sys.exit(app.exec())

