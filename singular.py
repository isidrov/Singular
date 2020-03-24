#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem,QSplitter
from PyQt5.QtCore import QRunnable,QObject,pyqtSignal, pyqtSlot, QThreadPool,Qt
import traceback
import os
import time
import sys
from tabulate import tabulate
import logging.config
from AXLPlugin import UcmAXLConnection
from AXLPlugin import UcmRisPortToolkit

from webex import Webex
from axapi import Axapi
from PawsPlugin import PawsPlugin
from cli_expect import CliExpect
import json
import csv
import requests
#from requests_toolbelt.multipart.encoder import MultipartEncoder
import yaml
import pprint
import logging, re
from shutil import copyfile
import errno
from syntaxhighlighter import Highlighter
from syntaxhighlighterJSON import Highlighter as HighlighterJSON
import base64
import html
import ipaddress
from flask import Flask, render_template, request
import threading
from cryptography.fernet import Fernet
import http.server
import socketserver
import xml.etree.ElementTree as ET
from http_multithreaded import ThreadedHTTPServer
from httpServer import MyHttpServer

from http.server import HTTPServer, CGIHTTPRequestHandler
import webbrowser
import threading
import os
#from test import PerhapsMyHttpServer
from helper_functions import calc_sha512

from csv import reader

# Paths initialization

key = 'ZHsQaz82ylxBUYk8nwH750qHHnDMrNJurqLD8IhlFno='

frozen = ''

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    dir_project = sys._MEIPASS
    dir_executable = os.path.dirname(sys.argv[0])
    print('we are running in a bundle')

else:
    # we are running in a normal Python environment
    dir_project = os.path.dirname(os.path.abspath(__file__))
    dir_executable = dir_project
    print('we are running in a normal Python environment')



#print('os.path.dirname(os.path.abspath(__file__): ' + dir_project)
#print( 'sys.argv[0] is: ', sys.argv[0] )
#print( 'sys.executable is: ', sys.executable )
#print( 'os.getcwd is: ', os.getcwd() )
#print('dir_project ' + dir_project)  # THIS IS THE TEMPORARY FOLDER
print('dir_executable ' + dir_executable)

outputPath = os.path.join(dir_executable, 'output')

print('OutputPath ' + outputPath)

try:
    print('creating Output folder')
    os.makedirs(outputPath)
except OSError as e:

    if e.errno == errno.EEXIST:
        print('folder already exists')
    else:
        raise


try:
    print('creating output/debugs folder')
    os.makedirs(os.path.join(outputPath, 'debugs'))
except OSError as e:
    if e.errno == errno.EEXIST:
        print('folder already exists')
    else:
        raise

debugsPath = os.path.join(outputPath, 'debugs')

try:
    print('creating output/CLI folder')
    os.makedirs(os.path.join(outputPath, 'CLI/'))
except OSError as e:
    if e.errno == errno.EEXIST:
        print('folder already exists')
    else:
        raise

cliPath = os.path.join(outputPath, 'cli')

try:
    print('creating output/telepresence folder')
    os.makedirs(os.path.join(outputPath, 'telepresence'))
except OSError as e:
    if e.errno == errno.EEXIST:
        print('folder already exists')
    else:
        raise

tpPath = os.path.join(outputPath, 'telepresence')


logFileName = 'Nautilus_' + time.strftime('%Y%m%d-%H%M%S' + '.log')

logFilePath = os.path.join(debugsPath, logFileName)

schemaPath = os.path.join(dir_project,'schema')

CLICollectorPath = os.path.join(dir_project,'CLICollector')

axlCollectorPath = os.path.join(dir_project,'AXLCollector')
axlQueries = os.path.join(axlCollectorPath, 'axlQueries.json')

file_path = os.path.join(dir_executable, 'log_file.txt') #Encrypted webex token

# set up logging to file

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-5s %(levelname)-5s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename= logFilePath,
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr

console = logging.StreamHandler()
console.setLevel(logging.INFO)


# set a format which is simpler for console use

formatter = logging.Formatter('%(asctime)s %(name)-5s: %(levelname)-5s %(message)s')

# tell the handler to use this format

console.setFormatter(formatter)

# add the handler to the root logger

logging.getLogger('').addHandler(console)


logging.info('installPath ' + dir_project)
logging.info('executablePath ' + dir_executable)
logging.info('debugsPath ' + debugsPath)
logging.info('logFileName ' + logFileName)
logging.info('logFilePath ' + logFilePath)
logging.info('schema path' + schemaPath)
logging.info("Logging initializated")

from PyQt5 import QtCore, QtGui, QtWidgets




class Ui_Nautilus(object):
    def setupUi(self, Nautilus):
        Nautilus.setObjectName("Nautilus")
        Nautilus.resize(1187, 819)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(254, 254, 254))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(254, 254, 254))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        Nautilus.setPalette(palette)
        Nautilus.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.gridLayout_2 = QtWidgets.QGridLayout(Nautilus)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.globalwidget = QtWidgets.QTabWidget(Nautilus)
        self.globalwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(200, 200, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(88, 88, 88))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(200, 200, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(200, 200, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(200, 200, 200))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.globalwidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.globalwidget.setFont(font)
        self.globalwidget.setToolTip("")
        self.globalwidget.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.globalwidget.setObjectName("globalwidget")
        self.tab_SQL = QtWidgets.QWidget()
        self.tab_SQL.setObjectName("tab_SQL")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_SQL)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_5 = QtWidgets.QWidget(self.tab_SQL)
        self.widget_5.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_5.setMaximumSize(QtCore.QSize(275, 16777215))
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widget_3 = QtWidgets.QWidget(self.widget_5)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_ip_address_sql = QtWidgets.QLabel(self.widget_3)
        self.label_ip_address_sql.setObjectName("label_ip_address_sql")
        self.verticalLayout.addWidget(self.label_ip_address_sql)
        self.label_username_sql = QtWidgets.QLabel(self.widget_3)
        self.label_username_sql.setMinimumSize(QtCore.QSize(0, 0))
        self.label_username_sql.setObjectName("label_username_sql")
        self.verticalLayout.addWidget(self.label_username_sql)
        self.label_password_sql = QtWidgets.QLabel(self.widget_3)
        self.label_password_sql.setObjectName("label_password_sql")
        self.verticalLayout.addWidget(self.label_password_sql)
        self.horizontalLayout_7.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_5)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit_ipaddress_sql = QtWidgets.QLineEdit(self.widget_4)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_ipaddress_sql.setPalette(palette)
        self.lineEdit_ipaddress_sql.setText("")
        self.lineEdit_ipaddress_sql.setObjectName("lineEdit_ipaddress_sql")
        self.verticalLayout_2.addWidget(self.lineEdit_ipaddress_sql)
        self.lineEdit_username_sql = QtWidgets.QLineEdit(self.widget_4)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_username_sql.setPalette(palette)
        self.lineEdit_username_sql.setText("")
        self.lineEdit_username_sql.setObjectName("lineEdit_username_sql")
        self.verticalLayout_2.addWidget(self.lineEdit_username_sql)
        self.lineEdit_password_sql = QtWidgets.QLineEdit(self.widget_4)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_password_sql.setPalette(palette)
        self.lineEdit_password_sql.setText("")
        self.lineEdit_password_sql.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password_sql.setObjectName("lineEdit_password_sql")
        self.verticalLayout_2.addWidget(self.lineEdit_password_sql)
        self.horizontalLayout_7.addWidget(self.widget_4)
        self.verticalLayout_4.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(self.tab_SQL)
        self.widget_6.setObjectName("widget_6")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(self.widget_6)
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.SQLquery = QtWidgets.QPlainTextEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SQLquery.sizePolicy().hasHeightForWidth())
        self.SQLquery.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.SQLquery.setFont(font)
        self.SQLquery.setObjectName("SQLquery")
        self.horizontalLayout_4.addWidget(self.SQLquery)
        self.verticalLayout_3.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.widget_6)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.SQLresponse = QtWidgets.QPlainTextEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SQLresponse.sizePolicy().hasHeightForWidth())
        self.SQLresponse.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.SQLresponse.setFont(font)
        self.SQLresponse.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.SQLresponse.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.SQLresponse.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.SQLresponse.setPlainText("")
        self.SQLresponse.setObjectName("SQLresponse")
        self.horizontalLayout_3.addWidget(self.SQLresponse)
        self.verticalLayout_3.addWidget(self.widget_2)
        self.verticalLayout_4.addWidget(self.widget_6)
        self.widget_executeSql = QtWidgets.QWidget(self.tab_SQL)
        self.widget_executeSql.setObjectName("widget_executeSql")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_executeSql)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_sql_execute = QtWidgets.QPushButton(self.widget_executeSql)
        self.pushButton_sql_execute.setMinimumSize(QtCore.QSize(0, 31))
        self.pushButton_sql_execute.setMaximumSize(QtCore.QSize(141, 16777215))
        self.pushButton_sql_execute.setObjectName("pushButton_sql_execute")
        self.horizontalLayout_6.addWidget(self.pushButton_sql_execute)
        self.verticalLayout_4.addWidget(self.widget_executeSql)
        self.globalwidget.addTab(self.tab_SQL, "")
        self.tab_cli = QtWidgets.QWidget()
        self.tab_cli.setObjectName("tab_cli")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.tab_cli)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.toolBox = QtWidgets.QToolBox(self.tab_cli)
        self.toolBox.setObjectName("toolBox")
        self.page_VOS = QtWidgets.QWidget()
        self.page_VOS.setGeometry(QtCore.QRect(0, 0, 1145, 700))
        self.page_VOS.setObjectName("page_VOS")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.page_VOS)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.widget_30 = QtWidgets.QWidget(self.page_VOS)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_30.sizePolicy().hasHeightForWidth())
        self.widget_30.setSizePolicy(sizePolicy)
        self.widget_30.setMinimumSize(QtCore.QSize(660, 0))
        self.widget_30.setMaximumSize(QtCore.QSize(600, 169865))
        self.widget_30.setObjectName("widget_30")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_30)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget_25 = QtWidgets.QWidget(self.widget_30)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_25.sizePolicy().hasHeightForWidth())
        self.widget_25.setSizePolicy(sizePolicy)
        self.widget_25.setObjectName("widget_25")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_25)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.groupBox = QtWidgets.QGroupBox(self.widget_25)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(240, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(230, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.groupBox.setPalette(palette)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget_24 = QtWidgets.QWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_24.sizePolicy().hasHeightForWidth())
        self.widget_24.setSizePolicy(sizePolicy)
        self.widget_24.setMaximumSize(QtCore.QSize(16777215, 108))
        self.widget_24.setObjectName("widget_24")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_24)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_15 = QtWidgets.QWidget(self.widget_24)
        self.widget_15.setObjectName("widget_15")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.widget_15)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.UCMPub_Label = QtWidgets.QLabel(self.widget_15)
        self.UCMPub_Label.setObjectName("UCMPub_Label")
        self.verticalLayout_18.addWidget(self.UCMPub_Label)
        self.UCMPubCLI_username_label = QtWidgets.QLabel(self.widget_15)
        self.UCMPubCLI_username_label.setObjectName("UCMPubCLI_username_label")
        self.verticalLayout_18.addWidget(self.UCMPubCLI_username_label)
        self.label_22 = QtWidgets.QLabel(self.widget_15)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_18.addWidget(self.label_22)
        self.horizontalLayout.addWidget(self.widget_15)
        self.widget_19 = QtWidgets.QWidget(self.widget_24)
        self.widget_19.setObjectName("widget_19")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_19)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.UCMPub_IP_CLI_line = QtWidgets.QLineEdit(self.widget_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UCMPub_IP_CLI_line.sizePolicy().hasHeightForWidth())
        self.UCMPub_IP_CLI_line.setSizePolicy(sizePolicy)
        self.UCMPub_IP_CLI_line.setMinimumSize(QtCore.QSize(117, 17))
        self.UCMPub_IP_CLI_line.setMaximumSize(QtCore.QSize(23, 16777215))
        self.UCMPub_IP_CLI_line.setText("")
        self.UCMPub_IP_CLI_line.setObjectName("UCMPub_IP_CLI_line")
        self.verticalLayout_6.addWidget(self.UCMPub_IP_CLI_line)
        self.UCMPub_Username_CLI_line = QtWidgets.QLineEdit(self.widget_19)
        self.UCMPub_Username_CLI_line.setMinimumSize(QtCore.QSize(117, 17))
        self.UCMPub_Username_CLI_line.setMaximumSize(QtCore.QSize(125, 16777215))
        self.UCMPub_Username_CLI_line.setText("")
        self.UCMPub_Username_CLI_line.setObjectName("UCMPub_Username_CLI_line")
        self.verticalLayout_6.addWidget(self.UCMPub_Username_CLI_line)
        self.UCMPub_Password_CLI_line = QtWidgets.QLineEdit(self.widget_19)
        self.UCMPub_Password_CLI_line.setMinimumSize(QtCore.QSize(117, 17))
        self.UCMPub_Password_CLI_line.setMaximumSize(QtCore.QSize(125, 16777215))
        self.UCMPub_Password_CLI_line.setText("")
        self.UCMPub_Password_CLI_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.UCMPub_Password_CLI_line.setObjectName("UCMPub_Password_CLI_line")
        self.verticalLayout_6.addWidget(self.UCMPub_Password_CLI_line)
        self.horizontalLayout.addWidget(self.widget_19)
        self.widget_19.raise_()
        self.widget_15.raise_()
        self.verticalLayout_8.addWidget(self.widget_24)
        self.widget_10 = QtWidgets.QWidget(self.groupBox)
        self.widget_10.setMaximumSize(QtCore.QSize(16777215, 30))
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.pushButton_discover_nodes_UCM = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_discover_nodes_UCM.sizePolicy().hasHeightForWidth())
        self.pushButton_discover_nodes_UCM.setSizePolicy(sizePolicy)
        self.pushButton_discover_nodes_UCM.setMinimumSize(QtCore.QSize(20, 20))
        self.pushButton_discover_nodes_UCM.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_discover_nodes_UCM.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_discover_nodes_UCM.setAutoFillBackground(True)
        self.pushButton_discover_nodes_UCM.setObjectName("pushButton_discover_nodes_UCM")
        self.verticalLayout_15.addWidget(self.pushButton_discover_nodes_UCM)
        self.verticalLayout_8.addWidget(self.widget_10)
        self.horizontalLayout_8.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget_25)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.widget_7 = QtWidgets.QWidget(self.groupBox_2)
        self.widget_7.setObjectName("widget_7")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.widget_7)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.widget_9 = QtWidgets.QWidget(self.widget_7)
        self.widget_9.setObjectName("widget_9")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_9)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.widget_16 = QtWidgets.QWidget(self.widget_9)
        self.widget_16.setObjectName("widget_16")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.widget_16)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.UCMPub_Label_2 = QtWidgets.QLabel(self.widget_16)
        self.UCMPub_Label_2.setObjectName("UCMPub_Label_2")
        self.verticalLayout_19.addWidget(self.UCMPub_Label_2)
        self.UCMPubCLI_username_label_2 = QtWidgets.QLabel(self.widget_16)
        self.UCMPubCLI_username_label_2.setObjectName("UCMPubCLI_username_label_2")
        self.verticalLayout_19.addWidget(self.UCMPubCLI_username_label_2)
        self.label_23 = QtWidgets.QLabel(self.widget_16)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_19.addWidget(self.label_23)
        self.horizontalLayout_9.addWidget(self.widget_16)
        self.widget_20 = QtWidgets.QWidget(self.widget_9)
        self.widget_20.setMinimumSize(QtCore.QSize(130, 0))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.widget_20.setPalette(palette)
        self.widget_20.setObjectName("widget_20")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_20)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.UCMPub_IP_CLI_line_2 = QtWidgets.QLineEdit(self.widget_20)
        self.UCMPub_IP_CLI_line_2.setMinimumSize(QtCore.QSize(110, 17))
        self.UCMPub_IP_CLI_line_2.setMaximumSize(QtCore.QSize(125, 16777215))
        self.UCMPub_IP_CLI_line_2.setText("")
        self.UCMPub_IP_CLI_line_2.setObjectName("UCMPub_IP_CLI_line_2")
        self.verticalLayout_7.addWidget(self.UCMPub_IP_CLI_line_2)
        self.UCMPub_Username_CLI_line_2 = QtWidgets.QLineEdit(self.widget_20)
        self.UCMPub_Username_CLI_line_2.setMinimumSize(QtCore.QSize(110, 17))
        self.UCMPub_Username_CLI_line_2.setMaximumSize(QtCore.QSize(125, 16777215))
        self.UCMPub_Username_CLI_line_2.setText("")
        self.UCMPub_Username_CLI_line_2.setObjectName("UCMPub_Username_CLI_line_2")
        self.verticalLayout_7.addWidget(self.UCMPub_Username_CLI_line_2)
        self.UCMPub_Password_CLI_line_2 = QtWidgets.QLineEdit(self.widget_20)
        self.UCMPub_Password_CLI_line_2.setMinimumSize(QtCore.QSize(110, 17))
        self.UCMPub_Password_CLI_line_2.setMaximumSize(QtCore.QSize(125, 16777215))
        self.UCMPub_Password_CLI_line_2.setText("")
        self.UCMPub_Password_CLI_line_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.UCMPub_Password_CLI_line_2.setObjectName("UCMPub_Password_CLI_line_2")
        self.verticalLayout_7.addWidget(self.UCMPub_Password_CLI_line_2)
        self.horizontalLayout_9.addWidget(self.widget_20)
        self.widget_8 = QtWidgets.QWidget(self.widget_9)
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.widget_26 = QtWidgets.QWidget(self.widget_8)
        self.widget_26.setObjectName("widget_26")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_26)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButton_vos_sub = QtWidgets.QRadioButton(self.widget_26)
        self.radioButton_vos_sub.setChecked(True)
        self.radioButton_vos_sub.setObjectName("radioButton_vos_sub")
        self.horizontalLayout_2.addWidget(self.radioButton_vos_sub)
        self.radioButton_vos_pub = QtWidgets.QRadioButton(self.widget_26)
        self.radioButton_vos_pub.setChecked(False)
        self.radioButton_vos_pub.setObjectName("radioButton_vos_pub")
        self.horizontalLayout_2.addWidget(self.radioButton_vos_pub)
        self.verticalLayout_14.addWidget(self.widget_26)
        self.widget_21 = QtWidgets.QWidget(self.widget_8)
        self.widget_21.setMinimumSize(QtCore.QSize(0, 38))
        self.widget_21.setObjectName("widget_21")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_21)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_product_vos_gen = QtWidgets.QLabel(self.widget_21)
        self.label_product_vos_gen.setObjectName("label_product_vos_gen")
        self.horizontalLayout_10.addWidget(self.label_product_vos_gen)
        self.comboBox_product_vos_gen = QtWidgets.QComboBox(self.widget_21)
        self.comboBox_product_vos_gen.setObjectName("comboBox_product_vos_gen")
        self.comboBox_product_vos_gen.addItem("")
        self.comboBox_product_vos_gen.addItem("")
        self.comboBox_product_vos_gen.addItem("")
        self.comboBox_product_vos_gen.addItem("")
        self.horizontalLayout_10.addWidget(self.comboBox_product_vos_gen)
        self.verticalLayout_14.addWidget(self.widget_21)
        self.widget_21.raise_()
        self.widget_26.raise_()
        self.horizontalLayout_9.addWidget(self.widget_8)
        self.verticalLayout_13.addWidget(self.widget_9)
        self.widget_27 = QtWidgets.QWidget(self.widget_7)
        self.widget_27.setMinimumSize(QtCore.QSize(0, 38))
        self.widget_27.setObjectName("widget_27")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.widget_27)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButton_add_node = QtWidgets.QPushButton(self.widget_27)
        self.pushButton_add_node.setObjectName("pushButton_add_node")
        self.horizontalLayout_11.addWidget(self.pushButton_add_node)
        self.verticalLayout_13.addWidget(self.widget_27)
        self.verticalLayout_9.addWidget(self.widget_7)
        self.horizontalLayout_8.addWidget(self.groupBox_2)
        self.verticalLayout_10.addWidget(self.widget_25)
        self.widget_46 = QtWidgets.QWidget(self.widget_30)
        self.widget_46.setMinimumSize(QtCore.QSize(621, 0))
        self.widget_46.setObjectName("widget_46")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.widget_46)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.tableWidget_ucm_cluster_cli = QtWidgets.QTableWidget(self.widget_46)
        self.tableWidget_ucm_cluster_cli.setAlternatingRowColors(False)
        self.tableWidget_ucm_cluster_cli.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_ucm_cluster_cli.setShowGrid(False)
        self.tableWidget_ucm_cluster_cli.setColumnCount(5)
        self.tableWidget_ucm_cluster_cli.setObjectName("tableWidget_ucm_cluster_cli")
        self.tableWidget_ucm_cluster_cli.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_ucm_cluster_cli.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_ucm_cluster_cli.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_ucm_cluster_cli.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_ucm_cluster_cli.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_ucm_cluster_cli.setHorizontalHeaderItem(4, item)
        self.tableWidget_ucm_cluster_cli.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_ucm_cluster_cli.horizontalHeader().setHighlightSections(True)
        self.tableWidget_ucm_cluster_cli.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_ucm_cluster_cli.verticalHeader().setHighlightSections(True)
        self.verticalLayout_17.addWidget(self.tableWidget_ucm_cluster_cli)
        self.verticalLayout_10.addWidget(self.widget_46)
        self.widget_46.raise_()
        self.widget_25.raise_()
        self.horizontalLayout_30.addWidget(self.widget_30)
        self.widget_47 = QtWidgets.QWidget(self.page_VOS)
        self.widget_47.setObjectName("widget_47")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.widget_47)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.widget_49 = QtWidgets.QWidget(self.widget_47)
        self.widget_49.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_49.setObjectName("widget_49")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.widget_49)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.widget_50 = QtWidgets.QWidget(self.widget_49)
        self.widget_50.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_50.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_50.setObjectName("widget_50")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_50)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_execute_cli_ucm = QtWidgets.QPushButton(self.widget_50)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_execute_cli_ucm.sizePolicy().hasHeightForWidth())
        self.pushButton_execute_cli_ucm.setSizePolicy(sizePolicy)
        self.pushButton_execute_cli_ucm.setObjectName("pushButton_execute_cli_ucm")
        self.horizontalLayout_5.addWidget(self.pushButton_execute_cli_ucm)
        self.pushButton_stop_cli_ucm = QtWidgets.QPushButton(self.widget_50)
        self.pushButton_stop_cli_ucm.setObjectName("pushButton_stop_cli_ucm")
        self.horizontalLayout_5.addWidget(self.pushButton_stop_cli_ucm)
        self.pushButton_refresh_cli_ucm = QtWidgets.QPushButton(self.widget_50)
        self.pushButton_refresh_cli_ucm.setObjectName("pushButton_refresh_cli_ucm")
        self.horizontalLayout_5.addWidget(self.pushButton_refresh_cli_ucm)
        self.verticalLayout_20.addWidget(self.widget_50)
        self.treeWidget_ucm_cli = QtWidgets.QTreeWidget(self.widget_49)
        self.treeWidget_ucm_cli.setToolTip("")
        self.treeWidget_ucm_cli.setStatusTip("")
        self.treeWidget_ucm_cli.setAutoExpandDelay(0)
        self.treeWidget_ucm_cli.setObjectName("treeWidget_ucm_cli")
        self.verticalLayout_20.addWidget(self.treeWidget_ucm_cli)
        self.verticalLayout_12.addWidget(self.widget_49)
        self.horizontalLayout_30.addWidget(self.widget_47)
        self.toolBox.addItem(self.page_VOS, "")
        self.horizontalLayout_12.addWidget(self.toolBox)
        self.globalwidget.addTab(self.tab_cli, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.widget_38 = QtWidgets.QWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_38.sizePolicy().hasHeightForWidth())
        self.widget_38.setSizePolicy(sizePolicy)
        self.widget_38.setObjectName("widget_38")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout(self.widget_38)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.widget_11 = QtWidgets.QWidget(self.widget_38)
        self.widget_11.setMaximumSize(QtCore.QSize(16777215, 150))
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.groupBox_21 = QtWidgets.QGroupBox(self.widget_11)
        self.groupBox_21.setMaximumSize(QtCore.QSize(300, 16777215))
        self.groupBox_21.setObjectName("groupBox_21")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout(self.groupBox_21)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.label_8 = QtWidgets.QLabel(self.groupBox_21)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_27.addWidget(self.label_8)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_27.addItem(spacerItem)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_username_tp = QtWidgets.QLabel(self.groupBox_21)
        self.label_username_tp.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_username_tp.setFont(font)
        self.label_username_tp.setObjectName("label_username_tp")
        self.horizontalLayout_19.addWidget(self.label_username_tp)
        self.lineEdit_username_tp = QtWidgets.QLineEdit(self.groupBox_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_username_tp.sizePolicy().hasHeightForWidth())
        self.lineEdit_username_tp.setSizePolicy(sizePolicy)
        self.lineEdit_username_tp.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_username_tp.setMaximumSize(QtCore.QSize(150, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.lineEdit_username_tp.setPalette(palette)
        self.lineEdit_username_tp.setText("")
        self.lineEdit_username_tp.setObjectName("lineEdit_username_tp")
        self.horizontalLayout_19.addWidget(self.lineEdit_username_tp)
        self.verticalLayout_27.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_password_tp = QtWidgets.QLabel(self.groupBox_21)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_password_tp.setFont(font)
        self.label_password_tp.setObjectName("label_password_tp")
        self.horizontalLayout_20.addWidget(self.label_password_tp)
        self.lineEdit_password_tp = QtWidgets.QLineEdit(self.groupBox_21)
        self.lineEdit_password_tp.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_password_tp.setMaximumSize(QtCore.QSize(150, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_password_tp.setPalette(palette)
        self.lineEdit_password_tp.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password_tp.setObjectName("lineEdit_password_tp")
        self.horizontalLayout_20.addWidget(self.lineEdit_password_tp)
        self.verticalLayout_27.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem1)
        self.label_concurrent_tp = QtWidgets.QLabel(self.groupBox_21)
        self.label_concurrent_tp.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_concurrent_tp.setFont(font)
        self.label_concurrent_tp.setObjectName("label_concurrent_tp")
        self.horizontalLayout_14.addWidget(self.label_concurrent_tp)
        self.lineEdit_concurrent_tp = QtWidgets.QLineEdit(self.groupBox_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_concurrent_tp.sizePolicy().hasHeightForWidth())
        self.lineEdit_concurrent_tp.setSizePolicy(sizePolicy)
        self.lineEdit_concurrent_tp.setMinimumSize(QtCore.QSize(0, 0))
        self.lineEdit_concurrent_tp.setMaximumSize(QtCore.QSize(40, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_concurrent_tp.setPalette(palette)
        self.lineEdit_concurrent_tp.setObjectName("lineEdit_concurrent_tp")
        self.horizontalLayout_14.addWidget(self.lineEdit_concurrent_tp)
        self.verticalLayout_27.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_22.addWidget(self.groupBox_21)
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget_11)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_28.addWidget(self.label_9)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_10 = QtWidgets.QLabel(self.groupBox_3)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.label_10.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setOpenExternalLinks(True)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_17.addWidget(self.label_10)
        self.label_12 = QtWidgets.QLabel(self.groupBox_3)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_17.addWidget(self.label_12)
        self.lineEdit_webex_token = QtWidgets.QLineEdit(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_webex_token.sizePolicy().hasHeightForWidth())
        self.lineEdit_webex_token.setSizePolicy(sizePolicy)
        self.lineEdit_webex_token.setMaximumSize(QtCore.QSize(16777215, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_webex_token.setPalette(palette)
        self.lineEdit_webex_token.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_webex_token.setObjectName("lineEdit_webex_token")
        self.horizontalLayout_17.addWidget(self.lineEdit_webex_token)
        self.verticalLayout_28.addLayout(self.horizontalLayout_17)
        self.verticalLayout_29 = QtWidgets.QVBoxLayout()
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.label_11 = QtWidgets.QLabel(self.groupBox_3)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(63, 63, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.label_11.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setOpenExternalLinks(True)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_29.addWidget(self.label_11)
        self.verticalLayout_28.addLayout(self.verticalLayout_29)
        self.horizontalLayout_22.addWidget(self.groupBox_3)
        self.verticalLayout_30.addWidget(self.widget_11)
        self.widget_12 = QtWidgets.QWidget(self.widget_38)
        self.widget_12.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_12.setObjectName("widget_12")
        self.formLayout = QtWidgets.QFormLayout(self.widget_12)
        self.formLayout.setObjectName("formLayout")
        self.pushButton_run_TP_commands = QtWidgets.QPushButton(self.widget_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_run_TP_commands.sizePolicy().hasHeightForWidth())
        self.pushButton_run_TP_commands.setSizePolicy(sizePolicy)
        self.pushButton_run_TP_commands.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_run_TP_commands.setMaximumSize(QtCore.QSize(141, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(179, 255, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(179, 255, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(179, 255, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.pushButton_run_TP_commands.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.pushButton_run_TP_commands.setFont(font)
        self.pushButton_run_TP_commands.setObjectName("pushButton_run_TP_commands")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pushButton_run_TP_commands)
        self.verticalLayout_30.addWidget(self.widget_12)
        self.groupBox_41 = QtWidgets.QGroupBox(self.widget_38)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_41.sizePolicy().hasHeightForWidth())
        self.groupBox_41.setSizePolicy(sizePolicy)
        self.groupBox_41.setObjectName("groupBox_41")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout(self.groupBox_41)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.splitter = QtWidgets.QSplitter(self.groupBox_41)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_11.addWidget(self.label)
        self.plainTextEdit_tp_data = QtWidgets.QPlainTextEdit(self.layoutWidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.plainTextEdit_tp_data.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit_tp_data.setFont(font)
        self.plainTextEdit_tp_data.setObjectName("plainTextEdit_tp_data")
        self.verticalLayout_11.addWidget(self.plainTextEdit_tp_data)
        self.layoutWidget_2 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_16.addWidget(self.label_2)
        self.plainTextEdit_tp_commands = QtWidgets.QPlainTextEdit(self.layoutWidget_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.plainTextEdit_tp_commands.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit_tp_commands.setFont(font)
        self.plainTextEdit_tp_commands.setPlainText("")
        self.plainTextEdit_tp_commands.setObjectName("plainTextEdit_tp_commands")
        self.verticalLayout_16.addWidget(self.plainTextEdit_tp_commands)
        self.layoutWidget_3 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_23.addWidget(self.label_4)
        self.textEdit_TP_output = QtWidgets.QPlainTextEdit(self.layoutWidget_3)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textEdit_TP_output.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_TP_output.setFont(font)
        self.textEdit_TP_output.setObjectName("textEdit_TP_output")
        self.verticalLayout_23.addWidget(self.textEdit_TP_output)
        self.horizontalLayout_28.addWidget(self.splitter)
        self.verticalLayout_30.addWidget(self.groupBox_41)
        self.horizontalLayout_16.addWidget(self.widget_38)
        self.globalwidget.addTab(self.tab, "")
        self.tab_cms = QtWidgets.QWidget()
        self.tab_cms.setObjectName("tab_cms")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_cms)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_22 = QtWidgets.QWidget(self.tab_cms)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_22.sizePolicy().hasHeightForWidth())
        self.widget_22.setSizePolicy(sizePolicy)
        self.widget_22.setMaximumSize(QtCore.QSize(16777215, 120))
        self.widget_22.setObjectName("widget_22")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.widget_22)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.frame = QtWidgets.QFrame(self.widget_22)
        self.frame.setMaximumSize(QtCore.QSize(240, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.widget_28 = QtWidgets.QWidget(self.frame)
        self.widget_28.setMaximumSize(QtCore.QSize(80, 80))
        self.widget_28.setObjectName("widget_28")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.widget_28)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.label_username_tp_2 = QtWidgets.QLabel(self.widget_28)
        self.label_username_tp_2.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_username_tp_2.setFont(font)
        self.label_username_tp_2.setObjectName("label_username_tp_2")
        self.verticalLayout_21.addWidget(self.label_username_tp_2)
        self.label_password_tp_2 = QtWidgets.QLabel(self.widget_28)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_password_tp_2.setFont(font)
        self.label_password_tp_2.setObjectName("label_password_tp_2")
        self.verticalLayout_21.addWidget(self.label_password_tp_2)
        self.horizontalLayout_15.addWidget(self.widget_28)
        self.widget_29 = QtWidgets.QWidget(self.frame)
        self.widget_29.setMaximumSize(QtCore.QSize(150, 80))
        self.widget_29.setObjectName("widget_29")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.widget_29)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.lineEdit_username_tp_2 = QtWidgets.QLineEdit(self.widget_29)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_username_tp_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_username_tp_2.setSizePolicy(sizePolicy)
        self.lineEdit_username_tp_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.lineEdit_username_tp_2.setObjectName("lineEdit_username_tp_2")
        self.verticalLayout_22.addWidget(self.lineEdit_username_tp_2)
        self.lineEdit_password_tp_2 = QtWidgets.QLineEdit(self.widget_29)
        self.lineEdit_password_tp_2.setMaximumSize(QtCore.QSize(130, 16777215))
        self.lineEdit_password_tp_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password_tp_2.setObjectName("lineEdit_password_tp_2")
        self.verticalLayout_22.addWidget(self.lineEdit_password_tp_2)
        self.horizontalLayout_15.addWidget(self.widget_29)
        self.horizontalLayout_13.addWidget(self.frame)
        self.widget_23 = QtWidgets.QWidget(self.widget_22)
        self.widget_23.setObjectName("widget_23")
        self.horizontalLayout_13.addWidget(self.widget_23)
        self.verticalLayout_5.addWidget(self.widget_22)
        self.widget_17 = QtWidgets.QWidget(self.tab_cms)
        self.widget_17.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_17.setObjectName("widget_17")
        self.pushButton = QtWidgets.QPushButton(self.widget_17)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_5.addWidget(self.widget_17)
        self.widget_18 = QtWidgets.QWidget(self.tab_cms)
        self.widget_18.setObjectName("widget_18")
        self.verticalLayout_5.addWidget(self.widget_18)
        self.globalwidget.addTab(self.tab_cms, "")
        self.tab_UCM_AXL = QtWidgets.QWidget()
        self.tab_UCM_AXL.setEnabled(True)
        self.tab_UCM_AXL.setObjectName("tab_UCM_AXL")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.tab_UCM_AXL)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.widget_UCM_AXL_Global = QtWidgets.QWidget(self.tab_UCM_AXL)
        self.widget_UCM_AXL_Global.setObjectName("widget_UCM_AXL_Global")
        self.verticalLayout_33 = QtWidgets.QVBoxLayout(self.widget_UCM_AXL_Global)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.widget_UCM_AXL_Credentials = QtWidgets.QWidget(self.widget_UCM_AXL_Global)
        self.widget_UCM_AXL_Credentials.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_UCM_AXL_Credentials.setMaximumSize(QtCore.QSize(275, 108))
        self.widget_UCM_AXL_Credentials.setObjectName("widget_UCM_AXL_Credentials")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.widget_UCM_AXL_Credentials)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.widget_31 = QtWidgets.QWidget(self.widget_UCM_AXL_Credentials)
        self.widget_31.setObjectName("widget_31")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.widget_31)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.label_ip_address_axl = QtWidgets.QLabel(self.widget_31)
        self.label_ip_address_axl.setObjectName("label_ip_address_axl")
        self.verticalLayout_24.addWidget(self.label_ip_address_axl)
        self.label_username_axl = QtWidgets.QLabel(self.widget_31)
        self.label_username_axl.setMinimumSize(QtCore.QSize(0, 0))
        self.label_username_axl.setObjectName("label_username_axl")
        self.verticalLayout_24.addWidget(self.label_username_axl)
        self.label_password_axl = QtWidgets.QLabel(self.widget_31)
        self.label_password_axl.setObjectName("label_password_axl")
        self.verticalLayout_24.addWidget(self.label_password_axl)
        self.horizontalLayout_21.addWidget(self.widget_31)
        self.widget_32 = QtWidgets.QWidget(self.widget_UCM_AXL_Credentials)
        self.widget_32.setObjectName("widget_32")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.widget_32)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.lineEdit_ipaddress_axl = QtWidgets.QLineEdit(self.widget_32)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_ipaddress_axl.setPalette(palette)
        self.lineEdit_ipaddress_axl.setText("")
        self.lineEdit_ipaddress_axl.setObjectName("lineEdit_ipaddress_axl")
        self.verticalLayout_25.addWidget(self.lineEdit_ipaddress_axl)
        self.lineEdit_username_axl = QtWidgets.QLineEdit(self.widget_32)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_username_axl.setPalette(palette)
        self.lineEdit_username_axl.setText("")
        self.lineEdit_username_axl.setObjectName("lineEdit_username_axl")
        self.verticalLayout_25.addWidget(self.lineEdit_username_axl)
        self.lineEdit_password_axl = QtWidgets.QLineEdit(self.widget_32)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEdit_password_axl.setPalette(palette)
        self.lineEdit_password_axl.setText("")
        self.lineEdit_password_axl.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password_axl.setObjectName("lineEdit_password_axl")
        self.verticalLayout_25.addWidget(self.lineEdit_password_axl)
        self.horizontalLayout_21.addWidget(self.widget_32)
        self.verticalLayout_33.addWidget(self.widget_UCM_AXL_Credentials)
        self.widget_13 = QtWidgets.QWidget(self.widget_UCM_AXL_Global)
        self.widget_13.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_13.setObjectName("widget_13")
        self.formLayout_2 = QtWidgets.QFormLayout(self.widget_13)
        self.formLayout_2.setObjectName("formLayout_2")
        self.pushButton_run_AXL_commands = QtWidgets.QPushButton(self.widget_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_run_AXL_commands.sizePolicy().hasHeightForWidth())
        self.pushButton_run_AXL_commands.setSizePolicy(sizePolicy)
        self.pushButton_run_AXL_commands.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_run_AXL_commands.setMaximumSize(QtCore.QSize(141, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(179, 255, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(179, 255, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(179, 255, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.pushButton_run_AXL_commands.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.pushButton_run_AXL_commands.setFont(font)
        self.pushButton_run_AXL_commands.setObjectName("pushButton_run_AXL_commands")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.pushButton_run_AXL_commands)
        self.verticalLayout_33.addWidget(self.widget_13)
        self.groupBox_42 = QtWidgets.QGroupBox(self.widget_UCM_AXL_Global)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_42.sizePolicy().hasHeightForWidth())
        self.groupBox_42.setSizePolicy(sizePolicy)
        self.groupBox_42.setObjectName("groupBox_42")
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout(self.groupBox_42)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.splitter_3 = QtWidgets.QSplitter(self.groupBox_42)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter_4 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.layoutWidget_4 = QtWidgets.QWidget(self.splitter_4)
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_26.addWidget(self.label_3)
        self.plainTextEdit_axl_data = QtWidgets.QPlainTextEdit(self.layoutWidget_4)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.plainTextEdit_axl_data.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit_axl_data.setFont(font)
        self.plainTextEdit_axl_data.setObjectName("plainTextEdit_axl_data")
        self.verticalLayout_26.addWidget(self.plainTextEdit_axl_data)
        self.layoutWidget_5 = QtWidgets.QWidget(self.splitter_4)
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.verticalLayout_31 = QtWidgets.QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_31.addWidget(self.label_5)
        self.plainTextEdit_axl_commands = QtWidgets.QPlainTextEdit(self.layoutWidget_5)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.plainTextEdit_axl_commands.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.plainTextEdit_axl_commands.setFont(font)
        self.plainTextEdit_axl_commands.setPlainText("")
        self.plainTextEdit_axl_commands.setObjectName("plainTextEdit_axl_commands")
        self.verticalLayout_31.addWidget(self.plainTextEdit_axl_commands)
        self.layoutWidget_6 = QtWidgets.QWidget(self.splitter_4)
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.verticalLayout_32 = QtWidgets.QVBoxLayout(self.layoutWidget_6)
        self.verticalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.label_6 = QtWidgets.QLabel(self.layoutWidget_6)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_32.addWidget(self.label_6)
        self.textEdit_axl_output = QtWidgets.QPlainTextEdit(self.layoutWidget_6)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(50, 50, 50))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textEdit_axl_output.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textEdit_axl_output.setFont(font)
        self.textEdit_axl_output.setObjectName("textEdit_axl_output")
        self.verticalLayout_32.addWidget(self.textEdit_axl_output)
        self.horizontalLayout_29.addWidget(self.splitter_3)
        self.verticalLayout_33.addWidget(self.groupBox_42)
        self.horizontalLayout_18.addWidget(self.widget_UCM_AXL_Global)
        self.globalwidget.addTab(self.tab_UCM_AXL, "")
        self.gridLayout_2.addWidget(self.globalwidget, 0, 0, 1, 1)

        self.retranslateUi(Nautilus)
        self.globalwidget.setCurrentIndex(4)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Nautilus)



        #### MANUAL ADDITIONS ###

        # Button actions

        self.buttonEvents(Nautilus)

        # Font, important to be unispace to show correctly SQL responses

        font = QtGui.QFont("Consolas")

        # Highlight SQL editor

        self.highlighter = Highlighter(self.SQLquery.document())

        #Highlight JSON Editor

        #self.highlighter2 = HighlighterJSON(self.textEdit_TP_output.document())

        # If Unix or Windows, size is set differently

        if os.name == 'posix':
            font.setPointSize(12)
            self.SQLquery.setFont(font)
            logging.info('running on Unix/linux/MacOS')

        else:
            font.setPointSize(9)
            print('windows')

        QtWidgets.QApplication.setFont(font, "QPlainTextEdit")

        # Copying neccesary files and folders to where executable is:


        def myCopy(source,destination):

            for dirpath, dirnames, filenames in os.walk(source):

                structure = os.path.join(destination, os.path.relpath(dirpath, source))

                if not os.path.isdir(structure):

                    os.mkdir(structure)

                else:
                    print("Folder does already exits!")

                for file in filenames:

                    destination_filePath = os.path.join(structure,file)

                    if not os.path.isfile(destination_filePath):

                        copyfile(os.path.join(dirpath,file), destination_filePath )

        #myCopy(os.path.join(dir_project, 'ReadMe'),dir_executable)

        myCopy(os.path.join(dir_project, 'static'), os.path.join(dir_executable,'octopussy'))

        myCopy(os.path.join(dir_project, 'static'), os.path.join(dir_executable))



        # Copying Release Notes to executable folder
        '''
        ReadMe_path = os.path.join(dir_project, 'ReadMe')
        readme_file = os.path.join(ReadMe_path, 'Release_Notes.txt')
        copyfile(readme_file, os.path.join(dir_executable, 'Release_Notes.txt'))
        '''

        # Default loading of CLI commands

        dir_yaml = os.path.join(CLICollectorPath, 'list_of_commands.yaml')

        #dir_yaml = os.path.join(dir_project,'CLICollector/list_of_commands.yaml')

        if os.path.isfile(os.path.join(dir_project,'list_of_commands.yaml')):
            logging.info('YAML command file found with executable!')
        else:
            logging.info('YAML command file not found, copying it to script path')
            copyfile(dir_yaml,os.path.join(dir_executable,'list_of_commands.yaml'))

        dir_yaml = os.path.join(dir_executable,'list_of_commands.yaml')

        logging.info('Openning YAML command file in directory' + dir_yaml)

        with open(dir_yaml, 'r') as fi:
            commandDictYaml = yaml.load(fi)


        # YAML to Dict command list iteration and we build the command tree out of it

        self.build_tree_from_dict(self.treeWidget_ucm_cli,commandDictYaml)


        # Multi - threading

        self.threadpool = QThreadPool()

        self.threadpool.setMaxThreadCount(1)

        self.cli_interrupt = False

        logging.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # Hide password column on VOS CLI tab

        self.tableWidget_ucm_cluster_cli.setColumnHidden(4,True)

        #Hide CLI tab

        #self.tab_cli.setVisible(False)

        self.globalwidget.removeTab(3)

    def retranslateUi(self, Nautilus):
        _translate = QtCore.QCoreApplication.translate
        Nautilus.setWindowTitle(_translate("Nautilus", "Singular 1.2 - By Pelea Networks - "))
        self.label_ip_address_sql.setText(_translate("Nautilus", "UCM publisher IP"))
        self.label_username_sql.setText(_translate("Nautilus", "AXL username    "))
        self.label_password_sql.setText(_translate("Nautilus", "AXL password     "))
        self.SQLquery.setPlainText(
            _translate("Nautilus", "select name, description from device where name like \'SEP%\'"))
        self.pushButton_sql_execute.setText(_translate("Nautilus", "Execute Query"))
        self.globalwidget.setTabText(self.globalwidget.indexOf(self.tab_SQL), _translate("Nautilus", "SQL"))
        self.UCMPub_Label.setText(_translate("Nautilus", "UCM Pub"))
        self.UCMPubCLI_username_label.setText(_translate("Nautilus", "OS user"))
        self.label_22.setText(_translate("Nautilus", "OS pass"))
        self.pushButton_discover_nodes_UCM.setText(_translate("Nautilus", "DISCOVER CLUSTER"))
        self.UCMPub_Label_2.setText(_translate("Nautilus", "IP addr"))
        self.UCMPubCLI_username_label_2.setText(_translate("Nautilus", "OS  user"))
        self.label_23.setText(_translate("Nautilus", "OS pass"))
        self.radioButton_vos_sub.setText(_translate("Nautilus", "Sub"))
        self.radioButton_vos_pub.setText(_translate("Nautilus", "Pub"))
        self.label_product_vos_gen.setText(_translate("Nautilus", "Product"))
        self.comboBox_product_vos_gen.setItemText(0, _translate("Nautilus", "UCM"))
        self.comboBox_product_vos_gen.setItemText(1, _translate("Nautilus", "IMP"))
        self.comboBox_product_vos_gen.setItemText(2, _translate("Nautilus", "CUC"))
        self.comboBox_product_vos_gen.setItemText(3, _translate("Nautilus", "CER"))
        self.pushButton_add_node.setText(_translate("Nautilus", "ADD NODE"))
        self.tableWidget_ucm_cluster_cli.setSortingEnabled(True)
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(0)
        item.setText(_translate("Nautilus", "address"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(1)
        item.setText(_translate("Nautilus", "product"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(2)
        item.setText(_translate("Nautilus", "role"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(3)
        item.setText(_translate("Nautilus", "username"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(4)
        item.setText(_translate("Nautilus", "password"))
        self.pushButton_execute_cli_ucm.setText(_translate("Nautilus", "START"))
        self.pushButton_stop_cli_ucm.setText(_translate("Nautilus", "STOP"))
        self.pushButton_refresh_cli_ucm.setText(_translate("Nautilus", "REFRESH"))
        self.treeWidget_ucm_cli.headerItem().setText(0, _translate("Nautilus", "CLI Commands"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_VOS), _translate("Nautilus", "VOS"))
        self.globalwidget.setTabText(self.globalwidget.indexOf(self.tab_cli), _translate("Nautilus", "Platform"))
        self.label_8.setText(_translate("Nautilus", "onPrem Telepresence credentials"))
        self.label_username_tp.setText(_translate("Nautilus", "TP username"))
        self.label_password_tp.setText(_translate("Nautilus", "TP password"))
        self.label_concurrent_tp.setText(_translate("Nautilus", "Concurrency"))
        self.lineEdit_concurrent_tp.setText(_translate("Nautilus", "20"))
        self.label_9.setText(_translate("Nautilus", "Webex Authentication"))
        self.label_10.setText(_translate("Nautilus",
                                         "<html><head/><body><p><a href=\"http://localhost:10060/\"><span style=\" text-decoration: underline; color:#0000ff;\">Webex login</span></a></p></body></html>"))
        self.label_12.setText(_translate("Nautilus", "       OR ENTER ACCESS TOKEN MANUALLY      "))
        self.label_11.setText(_translate("Nautilus",
                                         "<html><head/><body><p><a href=\"https://github.com/isidrov/Nautilus\"><span style=\" text-decoration: underline; color:#0000ff;\">Readme</span></a></p></body></html>"))
        self.pushButton_run_TP_commands.setText(_translate("Nautilus", "Run"))
        self.label.setText(_translate("Nautilus", "Data"))
        self.label_2.setText(_translate("Nautilus", "Commands"))
        self.label_4.setText(_translate("Nautilus", "JSON Output"))
        self.globalwidget.setTabText(self.globalwidget.indexOf(self.tab), _translate("Nautilus", "Video / Webex"))
        self.label_username_tp_2.setText(_translate("Nautilus", "  username    "))
        self.label_password_tp_2.setText(_translate("Nautilus", "  password     "))
        self.pushButton.setText(_translate("Nautilus", "Run"))
        self.globalwidget.setTabText(self.globalwidget.indexOf(self.tab_cms),
                                     _translate("Nautilus", "Cisco Meeting Server"))
        self.label_ip_address_axl.setText(_translate("Nautilus", "UCM publisher IP"))
        self.label_username_axl.setText(_translate("Nautilus", "AXL username    "))
        self.label_password_axl.setText(_translate("Nautilus", "AXL password     "))
        self.pushButton_run_AXL_commands.setText(_translate("Nautilus", "Run"))
        self.label_3.setText(_translate("Nautilus", "Data"))
        self.label_5.setText(_translate("Nautilus", "Commands"))
        self.label_6.setText(_translate("Nautilus", "JSON Output"))
        self.globalwidget.setTabText(self.globalwidget.indexOf(self.tab_UCM_AXL), _translate("Nautilus", "UCM AXL"))




    def buttonEvents(self, Nautilus):

        self.pushButton_sql_execute.clicked.connect(self.execute_sql)
        self.pushButton_discover_nodes_UCM.clicked.connect(self.discover_nodes)
        self.pushButton_execute_cli_ucm.clicked.connect(self.execute_cli_ucm)
        self.pushButton_refresh_cli_ucm.clicked.connect(self.refresh_cli_commands)
        self.pushButton_stop_cli_ucm.clicked.connect(self.destroy_cli_connection)
        self.pushButton_run_TP_commands.clicked.connect(self.run_tp_commands) # Run on TP pane
        self.pushButton_run_AXL_commands.clicked.connect(self.run_axl_commands)
        #self.pushButton_stop_vos_gen.clicked.connect(self.destroy_cli_connection)
        self.pushButton_add_node.clicked.connect(self.add_node_to_vos_gen)
        #self.pushButton_execute_vos_gen.clicked.connect(self.execute_cli_vos_gen)

    def refresh_cli_commands(self):

        logging.info('Refresh pressed on UCM CLI tab')
        logging.info('dir project: ' + dir_project)
        logging.info('dir_executable ' + dir_executable)

        self.treeWidget_ucm_cli.clear()

        # Default loading of CLI commands

        dir_yaml = os.path.join(dir_executable, 'list_of_commands.yaml')

        with open(dir_yaml, 'r') as fi:
            commandDictYaml = yaml.load(fi)

        self.build_tree_from_dict(self.treeWidget_ucm_cli, commandDictYaml)



    def build_tree_from_dict(self, tree_widget, dict_commands):

        key_list = list(dict_commands.keys())

        for x in range(len(key_list)):
            l1 = QtWidgets.QTreeWidgetItem([key_list[x]])
            command_list = dict_commands[key_list[x]]
            if command_list:
                for i in range(len(command_list)):
                    l1_child = QtWidgets.QTreeWidgetItem([command_list[i]])
                    l1_child.setCheckState(0,QtCore.Qt.Checked)
                    l1.addChild(l1_child)
            else:
                pass
            tree_widget.addTopLevelItem(l1)



    def find_checked(self, tr):

        checked_dict = dict()
        root = tr.invisibleRootItem()
        signal_count = root.childCount() # returns number of tree elements from the root

        for i in range(signal_count):

            signal = root.child(i) # element in a tree
            checked_commands = list()
            num_children = signal.childCount() # number of children under a tree element

            for n in range(num_children):
                child = signal.child(n)   # child under tree element

                if child.checkState(0) == QtCore.Qt.Checked:   # if command is checked
                    checked_commands.append(child.text(0))   # store the command in a list

            # Add the list of checked commands under the tree item in a dict

            checked_dict[signal.text(0)] = checked_commands

        return checked_dict

    def validate_ip(self, ip):

        logging.debug('validating ip')

        try:

            ipaddress.ip_address(ip)

            return True

        except Exception as ex:

            logging.info(ex)

            return False



    def add_node_to_vos_gen(self):

        logging.info("Pressed add node under Platform")

        user = self.UCMPub_Username_CLI_line_2.text()
        password = self.UCMPub_Password_CLI_line_2.text()
        ip = self.UCMPub_IP_CLI_line_2.text()

        if self.validate_ip(ip):

            product = self.comboBox_product_vos_gen.currentText()

            type = 'Subscriber'
            if self.radioButton_vos_pub.isChecked():
                type = 'Publisher'

            vos_node_info = [{'address': ip,'username': user, 'password':password, 'role':product,'type':type}]

            self.dict2QTable(self.tableWidget_ucm_cluster_cli, vos_node_info)

            #self.vos_gen_dict2QTable(self.tableWidget_ucm_cluster_cli,vos_node_info)

        else:

            logging.error('IP address invalid while adding a node under platform tab, please review and correct')



    def discover_nodes(self):

        logging.info("Pressed discover nodes button under UCM CLI")

        user = self.UCMPub_Username_CLI_line.text()
        password = self.UCMPub_Password_CLI_line.text()
        pub_ip = self.UCMPub_IP_CLI_line.text()

        if self.validate_ip(pub_ip) != None:

            logging.debug('username: ' + user)
            logging.info('PUB IP address for CLI: ' + pub_ip)
            logging.info('Creating PAWs object ')
            paws = PawsPlugin(user, password, pub_ip, False)

            cl_service = paws.create_service("ClusterNodesService")

            if cl_service:

                paws_clusterInfo = paws.get_cluster_status(cl_service)

                logging.info("Raw UCM cluster information from PAWS")
                logging.info(paws_clusterInfo)
                logging.info("Raw UCM cluster type from PAWS " + str(type(paws_clusterInfo)))
                logging.info("Raw paws_clusterInfo[0] type " + str(type(paws_clusterInfo[0])))
                logging.info(paws_clusterInfo)

                all_nodes_info = self.clean_clusterInfo_from_Paws(paws_clusterInfo,username = user, password = password)

                '''
                {'address': '10.85.141.28',
                 'username': 'cisco',
                 'password': 'blablabla',
                 'type': 'Subscriber',
                 'role': 'IMP'}
                '''

                self.dict2QTable(self.tableWidget_ucm_cluster_cli, all_nodes_info)

            else:
                logging.error("unable to create paws object")

            '''
            
            {
            'address': '10.85.141.8',
            'alias': 'JimCUCMPub',
            'dbRole': 'Primary',
            'hostname': 'JimCUCMPub.ottuc.com',
            'role': 'UCM',
            'status': 'online',
            'type': 'Publisher'
            }
            
            '''
        else:

            logging.error('IP address invalid while discovering nodes under platform tab, please review and correct')




    def dict2QTable(self, tableW, list_of_dicts):

        #row = 0

        rowPosition = tableW.rowCount()
        logging.info('raw position = ' + str(rowPosition))

        tableW.setRowCount(rowPosition + 1)

        # Set the number of rows in table for display based on the nodes found from PAWS

        #tableW.setRowCount(len(list_of_dicts))

        # Populate table for display based on dict built from PAWS

        node_counter = 0

        for node in list_of_dicts:

            node_counter += 1

            logging.info('raw position = ' + str(rowPosition))
            tableW.setItem(rowPosition, 0, QTableWidgetItem(node['address']))
            tableW.setItem(rowPosition, 1, QTableWidgetItem(node['role']))
            tableW.setItem(rowPosition, 2, QTableWidgetItem(node['type']))
            tableW.setItem(rowPosition, 3, QTableWidgetItem(node['username']))
            tableW.setItem(rowPosition, 4, QTableWidgetItem(node['password']))


            rowPosition += 1
            if node_counter < len(list_of_dicts):
                tableW.setRowCount(rowPosition + 1)

    def vos_gen_dict2QTable(self, tableW, vos_node_info):

        logging.info("Populating table vos_gen_dict2QTable")


        rowPosition = tableW.rowCount()


        # Set the number of rows in table for display based on the nodes found from PAWS

        tableW.setRowCount(rowPosition + 1)

        # Populate table for display based on dict built from self.add_node_to_vos_gen

        tableW.setItem(rowPosition, 0, QTableWidgetItem(vos_node_info['address']))
        tableW.setItem(rowPosition, 1, QTableWidgetItem(vos_node_info['username']))
        tableW.setItem(rowPosition, 2, QTableWidgetItem(vos_node_info['password']))
        tableW.setItem(rowPosition, 3, QTableWidgetItem(vos_node_info['role']))



    '''def thread_complete(self):
        print("THREAD COMPLETE!")'''

    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def execute_cli_ucm(self):

        logging.info("Pressed execute button under UCM CLI")

        self.cli_interrupt = False

        # Populate cluster info from table, in case user has updated some of the fields

        all_nodes_info  = self.build_listOfdicts_from_table(self.tableWidget_ucm_cluster_cli)

        # example of data structure of all_nodes_info below

        # <class 'list'>: [{'address': '10.87.99.211', 'product': 'UCM', 'role': 'Subscriber', 'username': 'admin', 'password': 'blablabla'}]

        # Ordered cluster (dict of lists)

        #orderedCluster = self.order_cluster(all_nodes_info)


        logging.info("orderedCluster ready for CLI execution")


        # checked commands (dict of lists)

        orderedCommands = self.find_checked(self.treeWidget_ucm_cli)

        logging.info("Checked commands read before executing CLI commands")
        logging.info('\n' + pprint.pformat(orderedCommands))

        # Threaded to allow the mouse pointer to be released while executing

        '''
        Multithreading

        from https://martinfitzpatrick.name/article/multithreading-pyqt-applications-with-qthreadpool/

        '''

        # CLI execution for UCM Publisher

        try:

            pub_commands = orderedCommands['global_commands'] + orderedCommands['ucm_commands'] + \
                           orderedCommands['ucm_pub_commands']
            sub_commands = orderedCommands['ucm_commands'] + orderedCommands['global_commands']
            imp_commands = orderedCommands['imp_commands'] + orderedCommands['global_commands']
            cuc_commands = orderedCommands['cuc_commands'] + orderedCommands['global_commands']
            cer_commands = orderedCommands['cer_commands'] + orderedCommands['global_commands']

            logging.info('Pub commands: ' + str(pub_commands))
            logging.info('sub commands: ' + str(sub_commands))
            logging.info('imp commands: ' + str(imp_commands))
            logging.info('cuc commands: ' + str(cuc_commands))
            logging.info('cer commands: ' + str(cer_commands))

        except KeyError as err:

            logging.error(err)
            logging.error('Verify list_of_commands.yaml file is formatted correcly')
            self.cli_interrupt = True

        if not self.cli_interrupt:

            for node in all_nodes_info:

                if node['product'] == 'UCM' and node['role'] == 'Publisher':
                    logging.info('running publisher cli commands')

                    self.worker_ucm_pub = Worker(self.run_vosplugin, node=node['address'],
                                user = node['username'], password = node['password'], commands=pub_commands)

                    self.threadpool.start(self.worker_ucm_pub)

                elif node['product'] == 'UCM' and node['role'] == 'Subscriber':

                    logging.info('running subscriber cli commands')

                    self.worker_ucm_sub = Worker(self.run_vosplugin, node=node['address'],
                                                  user=node['username'], password=node['password'],
                                                  commands=sub_commands)

                    self.threadpool.start(self.worker_ucm_sub)

                elif node['product'] == 'CER':

                    logging.info('running cer cli commands')

                    self.worker_cer = Worker(self.run_vosplugin, node=node['address'],
                                                  user=node['username'], password=node['password'],
                                                  commands=cer_commands)

                    self.threadpool.start(self.worker_cer)

                elif node['product'] == 'CUC':

                    logging.info('running cuc cli commands')

                    self.worker_cuc = Worker(self.run_vosplugin, node=node['address'],
                                                  user=node['username'], password=node['password'],
                                                  commands=cuc_commands)

                    self.threadpool.start(self.worker_cuc)

                elif node['product'] == 'IMP':

                    logging.info('running imp cli commands')

                    self.worker_imp = Worker(self.run_vosplugin, node=node['address'],
                                                  user=node['username'], password=node['password'],
                                                  commands=imp_commands)

                    self.threadpool.start(self.worker_imp)

                else:

                    logging.error('Node has been incorrectly classified: ' + node)


    # To interrupt CLI commands,

    def destroy_cli_connection(self):

        logging.info('Stop CLI execution button pressed')

        self.cli_interrupt = True


    def build_listOfdicts_from_table(self, tableW):

        final_list = list()

        columnCount = tableW.columnCount()
        rowCount = tableW.rowCount()

        for r in range(rowCount):
            temp_dict = dict()

            for c in range(columnCount):
                temp_dict[tableW.horizontalHeaderItem(c).text()] = tableW.item(r,c).text()

            final_list.append(temp_dict)

        return final_list



    def order_cluster(self, cluster_list):

        sorted_dict = dict()
        ucm_subs = list()
        imp_nodes = list()
        ucm_pubs = list()

        for node in cluster_list:
            temp_dict = dict(node)
            if node['role'] == 'Publisher':
                ucm_pubs.append(node)
            elif node['product'] == 'UCM' and node['role'] == 'Subscriber':
                ucm_subs.append(node)
            elif node['product'] == 'IMP':
                imp_nodes.append(node)
            else:
                logging.error('The below node could not be classified for cluster4CLI_execution')
                logging.error(node)
        sorted_dict['ucm_pubs'] = ucm_pubs
        sorted_dict['ucm_subs'] = ucm_subs
        sorted_dict['imp_nodes'] = imp_nodes

        return sorted_dict

    def order_cluster_vos_gen(self, cluster_list):

        sorted_dict = dict()
        ucm_nodes = list()
        imp_nodes = list()
        cer_nodes = list()
        cuc_nodes = list()

        for node in cluster_list:

            if node['role'] == 'UCM':
                ucm_nodes.append(node)
            elif node['role'] == 'CER':
                cer_nodes.append(node)
            elif node['role'] == 'IMP':
                imp_nodes.append(node)
            elif node['role'] == 'CUC':
                cuc_nodes.append(node)
            else:
                logging.error('The below node could not be classified for cluster4CLI_execution')
                logging.error(node)

        sorted_dict['ucm_nodes'] = ucm_nodes
        sorted_dict['cuc_nodes'] = cuc_nodes
        sorted_dict['cer_nodes'] = cer_nodes
        sorted_dict['imp_nodes'] = imp_nodes

        return sorted_dict

    def log_collection(self):

        logging.info("Pressed Export config under SQL tab")

        user = self.username_line.text()
        password = self.password_line.text()
        ucm_ip = self.ipAddress_line.text()

        axl = UcmLogCollection(user, password, ucm_ip, False)

        service_logs = [
            'Cisco CallManager',
            'Cisco CTIManager'
        ]

        system_logs = [

        ]

        relText = 'Minutes'
        relTime = '10'

        result = axl.get_file_names(service_logs,system_logs,relText,relTime)

        print(result)

    def export_config(self):

        logging.info("Pressed Export config under SQL tab")

        ucm_username = self.username_line.text()
        ucm_password = self.password_line.text()
        ucm_ip_address = self.ipAddress_line.text()

        logging.info('username: ' + ucm_username)
        logging.info('UCM IP address: ' + ucm_ip_address)
        logging.info('Creating UcmAXLConnection object for export config')

        # Create ZP object

        zp = UcmAXLConnection(ucm_ip_address, ucm_username, ucm_password,dir_project)

        # Read SQL queries for configuration export

        #zp.exportConfig(axlQueries,configOutputPath)

    def write_tp_output(self, data):

        #TODO Handle exception

        tpFilename = 'tp_output_' + time.strftime('%Y%m%d-%H%M%S' + '.json')

        tpfilePath = os.path.join(tpPath , tpFilename)

        try:

            with open(tpfilePath, mode='w+', newline="") as file:

                json.dump(data, file, indent = 4)

        except Exception as err:

            logging.error(err)



    def write_config(self, key, header, data, filename): #TODO not used, to be removed as we save already the output?

        # Write a json file with a specific key header (key)
        # this JSON key contains a list whose items are configs of endpoints


        if os.path.exists(filename):

            local_fav_json = {}

            with open(filename, mode='r', newline="") as file:


                # If the file exist we want to load existing contant to not overwrite it

                local_fav_json = json.load(file)

            with open(filename, mode='w', newline="") as file:

                local_fav_json[header][key] = data

                json.dump(local_fav_json, file, indent=4) # write the new json into the existing file

        else:

            with open(filename, mode='w+', newline="") as file:

                temp_dict = {}

                temp_dict[header] = {}

                print(temp_dict)

                temp_dict[header][key] = data

                print(temp_dict)

                json.dump(temp_dict, file, indent=4)

    def run_axl_commands(self):

        logging.info('Pressed "run commands" under UCM AXL tab')

        s = time.perf_counter()
        result = []
        axl_output_list = []
        all_good = True

        try:

            axl_username = self.lineEdit_username_axl.text()
            axl_password = self.lineEdit_password_axl.text()
            ucm_ipaddress = self.lineEdit_ipaddress_axl.text()


            axl = UcmAXLConnection(ip=ucm_ipaddress, usr=axl_username, psw=axl_password)
            ris = UcmRisPortToolkit(ip=ucm_ipaddress, usr=axl_username, psw=axl_password)
            logging.info('Default version: ' + axl.version)
            logging.info('WSDL ' + axl.wsdl)
            # get SQL query from UI box
            logging.info('UCMAXLConnection created! ')
            logging.info('UCMRisConnection created! ')

        except Exception as err:

            logging.error(err)

        # axl_dirty_data is a list of rows (each row is data in csv format)
        axl_dirty_data = self.plainTextEdit_axl_data.toPlainText().splitlines()

        axlinJsondata = self.csv2json_axl(axl_dirty_data)

        axl_cmd_list_dirty = self.plainTextEdit_axl_commands.toPlainText().splitlines()
        axl_cmd_list = []
        data_type = self.find_data_type(axl_dirty_data)

        if data_type == 'csv':

            column_size = len(axl_dirty_data[0].split(",")) # check csv number of values (columns)

            for row in axl_dirty_data:

                # confirm all rows have the same column values
                if column_size != len(row.split(",")):
                    result += [{'The following row does not have the same columns as the first row': row}]
                    all_good = False
                    break

        else:

            pass
            '''
            result = [f': Error classifying data field, execution will not start until corrected']

            axl_output_list = self.merge_tp_output_results(original=axl_output_list, addition=result)

            logging.error('Data is invalid, execution will not start until corrected')

            all_good = False
            '''

        if all_good:

            # we convert axl_dirty_data  to a list of lists, each value is a list item
            csv_reader = reader(axl_dirty_data)
            axl_data = list(csv_reader)

            for c in axl_cmd_list_dirty:
                if not c or c.startswith('#') or c.startswith(' '):
                    logging.info("ignoring the following command while cleaning the list :" + c)
                else:
                    axl_cmd_list.append(c)

            # supported commands below

            supported_commands = {
                'help': [
                    'update devicePoolInPhone()',
                    'add phone()',
                    'load addPhone()',
                    'show rejectedPhones()'
                ]
            }

            cmd_validation = self.validate_tp_command(supported_commands, axl_cmd_list)

            if cmd_validation['valid'] == False:

                all_good = False

                result = [{
                    cmd_validation['offendingCommand'] + ' not recognized , supported commands are': supported_commands}]

                logging.info(json.dumps(result , indent = 4))

                axl_output_list = self.merge_tp_output_results(original=axl_output_list, addition=result)

            else:

                logging.info('List of commands validated successfully')

        if all_good:

            for command in axl_cmd_list:

                logging.info('current command: ' + command)

                if command == 'help()':
                    result = [{'Supported commands are': supported_commands}]
                    axl_output_list = self.merge_tp_output_results(original=axl_output_list, addition=result)
                    break

                elif command.startswith('update'):

                    if command == "update devicePoolInPhone()":

                        for row in axl_data:

                            result.append(axl.update_dp_in_phone(row[0],row[1]))

                elif command.startswith('load'):

                    if command == "load addPhone()":

                        result.append(axl.load_phone())

                elif command.startswith('add'):

                    if command == "add phone()":

                        result.append(axl.add_phone(axlinJsondata))

                elif command.startswith('show'):

                    if command == "show rejectedPhones()":

                        selection_criteria = {
                            'DeviceClass': 'Any',
                            'SelectBy': 'Name',
                            'MaxReturnedDevices': '1000',
                            'Model': 255,
                            'Status': "Rejected",
                            'SelectItems': [
                                {
                                    'item': [
                                        'CSF*',  # Replace these with the devices you want to retrieve
                                    ]
                                }
                            ]
                        }

                        temp = ris.get_service().selectCmDevice(StateInfo='', CmSelectionCriteria=selection_criteria)

                else:
                    logging.error('Command ' + command + ' not recognized on TP execution')
                    result = [{command + ' not recognized , supported commands are': supported_commands}]

                axl_output_list = self.merge_tp_output_results(original=axl_output_list, addition=result)

            elapsed_paralell = time.perf_counter() - s  # Parallel execution comes here after commands are run
            elap = f'{elapsed_paralell:0.2f}'
            try:
                axl_output_list.insert(0, {'number of records': str(len(axl_dirty_data)), 'execution time': elap})
                logging.info(f'execution time: {elap}')
            except Exception as e:
                logging.error(str(e))
        else:
            axl_output_list = self.merge_tp_output_results(original=axl_output_list, addition=result)

        try:

            self.textEdit_axl_output.setPlainText(json.dumps(axl_output_list,indent = 4))
            self.write_tp_output(axl_output_list)

        except Exception as e:
            logging.error('Unable to write JSON in output pane')
            logging.error(str(e))

        logging.info('###### EXECUTION COMPLETED ######')




    def run_tp_commands(self):

        logging.info('Pressed "run commands" under Telepresence tab')

        s = time.perf_counter()

        try:

            tp_username = self.lineEdit_username_tp.text()
            tp_password = self.lineEdit_password_tp.text()
            tp_concurrent = int(self.lineEdit_concurrent_tp.text())
            data = self.plainTextEdit_tp_data.toPlainText().splitlines()
            webex_data = self.plainTextEdit_tp_data.toPlainText().splitlines()
            tp_cmd_list_dirty = self.plainTextEdit_tp_commands.toPlainText().splitlines()

            logging.debug('Collected IPs and credentials from GUI')

        except Exception as err:

            logging.error(err)

        all_good = True

        ip_list = []
        tp_output_list = []
        result = []

        axapi = Axapi(username=tp_username, password=tp_password, concurrent = tp_concurrent)

        data_type = self.find_data_type(data)

        if data_type == 'ip':

            ip_list = data
            ip_list = self.clean_ips(ip_list)
            axapi.data_column_size = 1

            #initialize endpoints in axapi

            for ip in ip_list:

                axapi.endpoints[ip] = {'ip' : ip }

        elif data_type == 'csv':

            column_size = len(data[0].split(",")) # check csv number of values (columns)
            for row in data:

                # confirm all rows have the same column values
                if column_size != len(row.split(",")):
                    result += [{'The following row does not have the same columns as the first row': row}]
                    all_good = False
                    break

            if all_good:

                axapi.exp_data = self.csv2json(data)

                for row in data:

                    values = row.split(",")
                    ip = values[0]
                    values.pop(0)
                    axapi.endpoints[ip] = {'ip': ip} #initialize endpoints with its ip
                    axapi.endpoints[ip]['data'] = values #store data on each endpoint
                    axapi.data_column_size = column_size

        elif data_type == 'empty':

            logging.info('No data entered')

        else:

            result = [f': Error classifying data field, execution will not start until corrected']

            tp_output_list = self.merge_tp_output_results(original=tp_output_list, addition=result)

            logging.error('Data is invalid, execution will not start until corrected')

            all_good = False



        # From the command list, remove commented lines starting by #, by space or new lines

        if all_good:

            tp_cmd_list = []

            for c in tp_cmd_list_dirty:
                if not c or c.startswith('#') or c.startswith(' '):
                    logging.info("ignoring the following command while cleaning the list :" + c)
                else:
                    tp_cmd_list.append(c)

            # supported commands below

            supported_commands = {
                'help': [
                    'help()'
                ],
                'run': [
                    'run migrate2cloud()',
                    'run tp backup()',
                    'run tp restore()'
                ],
                'show': [
                    'show status(<optional_status_item_filter>)',
                    'show commands(<optional_status_item_filter>)',
                    'show webex devices()',
                    'show webex devices status(<optional_filters, comma separated>)',
                    'show config(<optional_filter>)',
                    'show favorites()',
                    'show users()',
                    'show panels()',
                    'show webex places(<optional Place name>)'
                ],
                'test': [
                    'test migrate2cloud()'
                ],
                'set': [
                    'set config(<configuration as shown by show config>)',
                    'set password(<new_password>)',
                    'set systemName()'
                ],
                'add': [
                    'add contact(<name>,<number>)',
                    'add user(<username>,<password>,<role>)',
                    'add userRole(<username>,<role>)',
                    'add exp searchRules()'
                ],
                'upload': [
                    'upload brandingAwake(<image_file_name.ext>)',
                    'upload brandingHalfwake(<image_file_name.ext>)',
                    'upload brandingBackground(<image_file_name.ext>)',
                    'upload background(<image_file_name.ext>)',
                    'upload macro(<macro file>)',
                    'upload panel(<panel_file>)',
                    'upload wallpaper(<wallpaper_file>)'

                ],

                'delete': [
                    'delete itl()',
                    'delete webex places(<add place names, one on each line in the DATA pane>)',
                    'delete macro(<macro_name>)',
                    'delete user(<username>)',
                    'delete userRole(<username>,<role>)'
                ],
                'enable': [
                    'enable macroEditor()',
                    'enable macro(<macro_name>)'
                ],
                'disable': [
                    'disable macroEditor()',
                    'disable macro(<macro_name>)'
                ],
                'misc': [
                    'restart()',
                    'factoryReset()'
                ]
            }

            cmd_validation = self.validate_tp_command(supported_commands, tp_cmd_list)

            if cmd_validation['valid'] == False:

                all_good = False

                result = [{
                    cmd_validation['offendingCommand'] + ' not recognized , supported commands are': supported_commands}]

                logging.info(json.dumps(result , indent = 4))

                tp_output_list = self.merge_tp_output_results(original=tp_output_list, addition=result)

            else:

                logging.info('List of commands validated successfully')


        if all_good: # Async

            for command in tp_cmd_list:

                logging.info('current command: ' + command)

                if command == 'help()':

                    result = [{'Supported commands are': supported_commands}]
                    tp_output_list = self.merge_tp_output_results(original = tp_output_list, addition = result)
                    break

                elif command.startswith('show'):

                    if re.match('show config\((.*)\)', command) is not None:

                        logging.info('show config() command matched')
                        regex_result = re.search('show config\((.*)\)', command)
                        filter = regex_result.group(1)
                        command = 'show config()'
                        result = axapi.runIt(command=command, argument = filter)  # returns a list, each item is the result for each IP

                    elif re.match('show status\((.*)\)', command) is not None:

                        logging.info('show status() command matched')
                        regex_result = re.search('show status\((.*)\)', command)
                        filter = regex_result.group(1)
                        command = 'show status()'
                        result = axapi.runIt(command = command, argument = filter) # returns a List of dicts, each item is the result for each IP

                    elif re.match('show commands\((.*)\)', command) is not None:

                        logging.info('commands() command matched')
                        regex_result = re.search('show commands\((.*)\)', command)
                        filter = regex_result.group(1)
                        command = self.remove_arguments(command)
                        result = axapi.runIt(command = command, argument = filter) # returns a List of dicts, each item is the result for each IP

                    elif command == 'show favorites()':

                        logging.info('show favorites() command matched')
                        axapi.runIt(command='init sw()', argument='internal') # Need to init sw as TC and CE have different APIs
                        result = axapi.runIt(command=command) # returns a list, each item is the result for each IP

                    elif re.match('show users\((.*)\)', command) is not None:

                        logging.info(f"{command} command matched")
                        regex_result = re.search('show users\((.*)\)', command)
                        filter = [regex_result.group(1)]
                        axapi.runIt(command='init sw()', argument='internal')
                        command = self.remove_arguments(command)
                        result = axapi.runIt(command=command, argument = filter)

                    elif command == 'show panels()':

                        logging.info(f"{command} command matched")
                        axapi.runIt(command='init sw()', argument='internal')
                        command = self.remove_arguments(command)
                        result = axapi.runIt(command=command)

                    elif re.match('show webex places\((.*)\)', command) is not None:

                        logging.info('show webex places() command matched')
                        webexAccessToken = self.getwebexToken()

                        if webexAccessToken:

                            regex_result = re.search('show webex places\((.*)\)', command)
                            place = regex_result.group(1)
                            webex = Webex(webexAccessToken)
                            result = webex.runIt('show webex places()', place)

                        else:
                            result = [{'result': 'No Access token found, click on oAuth Webex link'}]

                    elif re.match('show webex devices\((.*)\)', command) is not None:

                        logging.info(f'{command} matched')
                        regex_result = re.search('show webex devices status\((.*)\)', command)
                        command = self.remove_arguments(command)
                        webexAccessToken = self.getwebexToken()

                        if webexAccessToken:

                            filters = []

                            if regex_result:

                                filter = regex_result.group(1)

                                if ',' in filter:
                                    filters = filter.split(',')

                                else:
                                    filters.append(filter)

                            webex = Webex(webexAccessToken)
                            webex.arguments =filters
                            result = webex.runIt(command)

                        else:
                            result = [{'result': 'No Access token found, click on oAuth Webex link'}]

                        pass

                    elif re.match('show webex devices status\((.*)\)', command) is not None:

                        logging.info(f'{command} matched')
                        regex_result = re.search('show webex devices status\((.*)\)', command)
                        command = self.remove_arguments(command)
                        webexAccessToken = self.getwebexToken()

                        if webexAccessToken:

                            filters = regex_result.group(1).split(',')
                            webex = Webex(webexAccessToken)
                            webex.filters =filters
                            result = webex.runIt(command)

                        else:
                            result = [{'result': 'No Access token found, click on oAuth Webex link'}]

                        pass


                elif command.startswith('set'):

                    if re.match('set config\((.*)\)', command) is not None:

                        logging.info('set config(<value>) command matched')
                        regex_result = re.search('set config\((.*)\)', command)
                        configuration = regex_result.group(1)
                        command = 'set config()'
                        result = axapi.runIt(command = command,
                                             argument = configuration)  # returns a list, each item is the result for each IP

                    elif re.match('set password\((.*)\)', command) is not None:

                        logging.info('set password(<value>) command matched')
                        axapi.runIt(command = 'init sw()', argument = 'internal') # by passing internal as argument, the output will be a dict easier to parse instead of an output to
                        regex_result = re.search('set password\((.*)\)', command)
                        password = regex_result.group(1)
                        command = 'set password()'
                        result = axapi.runIt(command = command, argument = password)  # returns a list, each item is the result for each IP

                    elif command == 'set systemName()':

                        logging.info('set systemName command matched')
                        result = axapi.runIt(command=command)

                    else:
                        result = [{
                            command + ' not recognized , supported commands are': supported_commands}]


                elif command == 'restart()':

                    logging.info('restart() command matched')
                    result = axapi.runIt(command=command)

                elif command.startswith('delete'):

                    if command == 'delete callHistory()':

                        result = axapi.runIt(command=command)

                    elif command == 'delete itl()':

                        logging.info('delete itl() command matched')
                        axapi.runIt(command='init sw()', argument='internal')
                        logging.info(f'sw versions discovered, running {command}')
                        result = axapi.runIt(command=command)

                    elif command == 'delete webex places()':

                        logging.info('delete webexPlaces() command matched')

                        webexAccessToken = self.getwebexToken()

                        if webexAccessToken:

                            webex = Webex(webexAccessToken)
                            webex.data = webex_data
                            result = webex.runIt('delete webex places()')

                        else:
                            result = [{'result':'No Access token found'}]

                    elif re.match('delete macro\((.*)\)', command) is not None:

                        logging.info('delete macro() command matched')
                        regex_result = re.search('delete macro\((.*)\)', command)
                        name = regex_result.group(1)
                        axapi.runIt(command='init sw()', argument='internal')
                        command = 'delete macro()'
                        result = axapi.runIt(command=command, argument=name)

                    elif re.match('delete user\((.*)\)', command) is not None:

                        logging.info('delete user() command matched')
                        regex_result = re.search('delete user\((.*)\)', command)
                        username = regex_result.group(1)
                        argument_list = [username]
                        command = self.remove_arguments(command)
                        axapi.runIt(command='init sw()', argument='internal')
                        result = axapi.runIt(command=command, argument=argument_list)

                    elif re.match('delete userRole\((.*),(.*)\)', command) is not None:

                        logging.info('delete userRole() command matched')
                        regex_result = re.search('delete userRole\((.*),(.*)\)', command)
                        username = regex_result.group(1)
                        role = regex_result.group(2)
                        arguments = [username, role]
                        command = self.remove_arguments(command)
                        axapi.runIt(command='init sw()', argument='internal')
                        result = axapi.runIt(command=command, argument=arguments)

                    else:
                        result = [{
                            command + ' not recognized , supported commands are': supported_commands}]

                elif command.startswith('add'):

                    if re.match('add contact\((.*),(.*)\)', command) is not None:

                        logging.info('add contact() command matched')
                        regex_result = re.search('add contact\((.*),(.*)\)', command)
                        name = regex_result.group(1)
                        number = regex_result.group(2)
                        command = self.remove_arguments(command)
                        result = axapi.runIt(command=command, argument=name, argument2=number)

                    elif re.match('add user\((.*),(.*),(.*)\)', command) is not None:

                        logging.info('add user() command matched')
                        regex_result = re.search('add user\((.*),(.*),(.*)\)', command)
                        username = regex_result.group(1)
                        password = regex_result.group(2)
                        role = regex_result.group(3)
                        argument_list = [username, password, role]
                        command = self.remove_arguments(command)
                        axapi.runIt(command='init sw()', argument='internal')
                        result = axapi.runIt(command=command, argument=argument_list)

                    elif re.match('add userRole\((.*),(.*)\)', command) is not None:

                        logging.info('add userRole() command matched')
                        regex_result = re.search('add userRole\((.*),(.*)\)', command)
                        username = regex_result.group(1)
                        role = regex_result.group(2)
                        arguments = [username, role]
                        command = self.remove_arguments(command)
                        axapi.runIt(command='init sw()', argument='internal')
                        result = axapi.runIt(command=command, argument=arguments)

                    elif command == 'add exp searchRules()':# TODO move to a expressway class

                        logging.info('add exp searchRules() command matched')
                        result = axapi.runIt(command=command)


                    else:
                        result = [{
                            command + ' not recognized , supported commands are': supported_commands}]


                elif command.startswith('run') or command.startswith('test'):

                    if command == 'run tp backup()':

                        try: #create folder where tp backups will be stored
                            logging.info('creating output/telepresence/backup folder')
                            tpPath = os.path.join(outputPath, 'telepresence')
                            bkPath = os.path.join(tpPath, 'backup')
                            os.makedirs(bkPath)

                        except OSError as e:
                            if e.errno == errno.EEXIST:
                                logging.info('folder already exists')
                            else:
                                raise

                        logging.info('run tp backup() command matched')
                        axapi.runIt(command='init sw()', argument='internal')
                        result = axapi.runIt(command=command, argument = bkPath)

                    elif command == 'run tp restore()':

                        logging.info('run tp restore() command matched')

                        tpPath = os.path.join(outputPath, 'telepresence')
                        bkPath = os.path.join(tpPath, 'backup')

                        if os.path.exists(bkPath):

                            # http_server = PerhapsMyHttpServer()

                            # self.threadpool.start(http_server)

                            axapi.runIt(command='init sw()', argument='internal')
                            result = axapi.runIt(command=command, argument=bkPath)



                        else:

                            error = 'backup folder not found \n please make sure output/telepresence/backup folder exist'
                            logging.info(error)
                            result =[error]

                    elif command == 'run migrate2cloud()' or command == 'test migrate2cloud()':

                        if command == 'test migrate2cloud()':
                            test = True
                            logging.info('test migrate2Cloud() command matched')

                        else:
                            test = False
                            logging.info('run migrate2Cloud() command matched')

                        webexAccessToken = self.getwebexToken()

                        if webexAccessToken:
                            axapi.runIt(command='init sw()', argument='internal')
                            logging.info(f'sw versions discovered, running {command}')
                            webex = Webex(webexAccessToken)
                            existing_webex_places = webex.runIt('show webex places()')[0]

                            try:
                                if existing_webex_places['show webex places()']['status'] != 'Error':
                                    axapi.canMigrate2cloud(existing_webex_places['show webex places()']['response']['items'])

                                    if not test:
                                        places = webex.runIt('add webexPlaces4migration()', axapi)
                                        self.addWebexPlaceId2Endpoint(places, axapi)
                                        codes = webex.runIt('get webexActivationCode4migration()', axapi)
                                        self.addWebexActivationCode2Endpoint(codes, axapi)
                                        results = axapi.runIt('run migrateEndpoints2cloud()')

                                        for r in results:
                                            for k,v in r.items():
                                                result.append({
                                                    k: {c: {'status': v['run migrateEndpoints2cloud()']['status'],
                                                            'response': v['run migrateEndpoints2cloud()']['response']}}})


                                        for k,v in axapi.endpoints.items():
                                            if ('canMigrate' in v) and ('migrationError' in v):
                                                if v['canMigrate'] == False:
                                                    result.insert(0,{k:{c:{'status':'Error','response':v['migrationError']}}})

                                    else: #test mode, we report endpoint status
                                        for k, v in axapi.endpoints.items():
                                            status = ''
                                            if ('canMigrate' in v) and ('migrationError' in v):
                                                if v['canMigrate'] == False:
                                                    result.append({
                                                        k: {c: {'status': 'ERROR', 'response': v['migrationError']}}})
                                                else:
                                                    result.append({
                                                        k: {c: {'status': 'OK', 'response': v['migrationError']}}})


                                else:
                                    result.append(existing_webex_places)

                            except Exception as err:
                                logging.error(err)

                        else:
                            result = [{command: 'No valid Webex token found'}]

                elif command.startswith('upload'):

                    if re.match('upload branding([^(]+)\((.*)\)',command) or re.match('upload background\((.*)\)', command) :

                        if re.match('upload branding([^(]+)\((.*)\)', command):
                            regex_result = re.search("upload branding([^(]+)\((.*)\)", command)
                            # Another solution to catch the file name between parenthesis
                            # string_result = command[command.find("(") + 1:command.rfind(")")]
                            type_tmp = regex_result.group(1)
                            file_name = regex_result.group(2)

                        else:
                            regex_result = re.search('upload background\((.*)\)', command)
                            file_name = regex_result.group(1)
                            type_tmp = 'background'

                        if type_tmp == 'Awake':
                            logging.info('upload brandingAwake command matched')
                            command = 'upload brandingAwake()'

                        elif type_tmp == 'Halfwake':
                            logging.info('upload brandingHalfwake command matched')
                            command = 'upload brandingHalfwake()'

                        elif type_tmp == 'Background':
                            logging.info('upload brandingBackground command matched')
                            command = 'upload brandingBackground()'

                        elif type_tmp == 'background':
                            logging.info('upload background() command matched')
                            command = 'upload background()'

                        else:
                            type = ''

                        image_path = os.path.join(dir_executable, file_name)
                        logging.info('Image path is : ' + image_path)

                        if os.path.exists(image_path):

                            logging.info('image file found successfully : ' + file_name)
                            axapi.runIt(command='init sw()', argument='internal')
                            encoded_image = ''

                            with open(image_path, "rb") as image_file:
                                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

                            result = axapi.runIt(command= command,
                                                 argument = file_name,argument2 = encoded_image)
                        else:
                            err = 'Image not found in path : ' + image_path
                            result = [{'code': 'ERROR', 'result': err}]
                            logging.error(err)

                    elif re.match('upload macro\((.*)\)', command) is not None:

                        logging.info('upload macro() command matched')

                        regex_result = re.search('upload macro\((.*)\)', command)

                        file_name = regex_result.group(1)

                        file_name_no_extension = file_name.split('.')[0]

                        macro_path = os.path.join(dir_executable, file_name)

                        logging.info('Macro path is : ' + macro_path)

                        if os.path.exists(macro_path):

                            logging.info('macro file found successfully : ' + file_name)
                            axapi.runIt(command='init sw()', argument='internal')

                            with open(macro_path, "rb") as macro_file:
                                macro_code = macro_file.read().decode(("utf-8"))
                                cleaned_code = html.escape(macro_code)

                            command = 'upload macro()'
                            result = axapi.runIt(command=command,
                                                 argument=file_name_no_extension, argument2=cleaned_code)
                        else:
                            err = 'Image not found in path : ' + macro_path
                            result = {'code': 'ERROR', 'result': err}
                            logging.error(err)

                    elif re.match('upload panel\((.*)\)', command) is not None:

                        logging.info('upload panel() command matched')

                        regex_result = re.search('upload panel\((.*)\)', command)

                        file_name = regex_result.group(1)

                        config_path = os.path.join(dir_executable, file_name)

                        logging.info('config file path is : ' + config_path)

                        if os.path.exists(config_path):

                            logging.info('config file found successfully : ' + file_name)

                            config_code = ""

                            with open(config_path, "rb") as config_file:
                                config_code = config_file.read().decode(("utf-8"))

                            # Retrieve PanelId
                            '''
                            panelId = ""
                            root = ET.fromstring(config_code)

                            for child in root.iter('PanelId'):
                                panelId = child.text 
                            '''
                            # XML breaks with &, needs to be replaced with its HTML code
                            # another way would be cleaned_code = macro_code.replace('&','&amp;')

                            cleaned_code = html.escape(config_code)
                            #axapi.runIt(command='show panels()')
                            command = self.remove_arguments(command)

                            axapi.runIt(command='init sw()', argument='internal')
#
                            result = axapi.runIt(command=command, argument = file_name, argument2=cleaned_code)

                        else:
                            err = 'Panel XML file not found in path : ' + config_path
                            result = [{'code': 'ERROR', 'result': err}]
                            logging.error(err)

                    elif re.match('upload wallpaper\((.*)\)', command) is not None:

                        logging.info('upload wallpaper() command matched')

                        regex_result = re.search('upload wallpaper\((.*)\)', command)

                        file_name = regex_result.group(1)

                        wallpaper_path = os.path.join(dir_executable, file_name)

                        logging.info('wallpaper path is : ' + wallpaper_path)

                        if os.path.exists(wallpaper_path):

                            logging.info('wallpaper file found successfully : ' + file_name)

                            command = self.remove_arguments(command)

                            axapi.runIt(command='init sw()', argument='internal')

                            arguments = [file_name]
                            result = axapi.runIt(command=command, argument=arguments)

                        else:
                            err = 'Panel XML file not found in path : ' + config_path
                            result = [{'code': 'ERROR', 'result': err}]
                            logging.error(err)


                    else:
                        result = [{
                            command + ' not recognized , supported commands are': supported_commands}]

                elif command.startswith('enable'):

                    if command == 'enable macroEditor()':

                        logging.info('enable macroEditor() command matched')
                        axapi.runIt(command='init sw()', argument='internal')
                        result = axapi.runIt(command=command)

                    elif re.match('enable macro\((.*)\)', command) is not None:

                        logging.info('enable_macro() command matched')
                        regex_result = re.search('enable macro\((.*)\)', command)
                        name = regex_result.group(1)
                        axapi.runIt(command='init sw()', argument='internal')
                        command = self.remove_arguments(command)
                        axapi.runIt(command='enable macro()')
                        result = axapi.runIt(command=command, argument = name)
                        logging.info('restarting macro')
                        axapi.runIt(command='restart macroRuntime()')

                elif command.startswith('disable'):

                    if command == 'disable macroEditor()':

                        logging.info('disable macroEditor() command matched')
                        axapi.runIt(command='init sw()', argument='internal')
                        result = axapi.runIt(command=command)

                    elif re.match('disable macro\((.*)\)', command) is not None:

                        logging.info('disable macro() command matched')
                        regex_result = re.search('disable macro\((.*)\)', command)
                        name = regex_result.group(1)
                        axapi.runIt(command='init sw()', argument='internal')
                        command = self.remove_arguments(command)
                        result = axapi.runIt(command=command, argument = name)

                    else:
                        result = [{
                            command + ' not recognized , supported commands are': supported_commands}]

                elif command == 'factoryReset()':
                    logging.info('factoryReset command command matched')
                    result = axapi.runIt(command=command)

                else:
                    logging.error('Command ' + command + ' not recognized on TP execution')
                    result = [{command + ' not recognized , supported commands are': supported_commands}]

                tp_output_list = self.merge_tp_output_results(original=tp_output_list, addition=result)

            elapsed_paralell = time.perf_counter() - s # Parallel execution comes here after commands are run
            elap = f'{elapsed_paralell:0.2f}'

            try:
                tp_output_list.insert(0,{'number of endpoints': str(len(ip_list)),'execution time': elap})
                logging.info(f'execution time: {elap}')

            except Exception as e:
                logging.error(str(e))
        else:

            tp_output_list = self.merge_tp_output_results(original=tp_output_list, addition=result)

        try:

            self.textEdit_TP_output.setPlainText(json.dumps(tp_output_list, indent=4))
            self.write_tp_output(tp_output_list)

        except Exception as e:

            logging.error('Unable to write JSON in output pane')
            logging.error(str(e))

        logging.info('###### EXECUTION COMPLETED ######')

    def clean_ips(self, ip_list): #clean spaces and newlines

        clean_list = []

        for ip in ip_list:  # cleaning up ip address list panel

            if ' ' in ip:  # remove any white spaces on an IP address

                ip = ip.replace(' ', '')
                clean_list.append(ip)

            elif ip == '':
                pass

            else:
                clean_list.append(ip)

        return clean_list

    def find_data_type(self, data):


        if len(data) == 0:
            return 'empty'

        elif self.validate_ip(data[0]): # check if the first entry from data is an IP
            return 'ip'

        elif "," in data[0]:
            return 'csv'

        elif not " " in data[0]:
            return 'csv'

        else:
            return 'unknown'



    def merge_tp_output_results(self, original, addition): # merge new list of dict with the last one matching on ip addresses


        try:
            return original + addition
        except Exception as err:
            logging.error(err)
            return ['Error merging tp output results']

    def addWebexPlaceId2Endpoint(self, results, axapi):

        try:

            for result in results:

                for k, v in result.items():

                    if 'id' in v['response'] and v['status'] == 200:

                        placeid = v['response']['id']
                        systemName = v['response']['displayName']

                        for ip_key, endpoint in axapi.endpoints.items():

                            if endpoint['canMigrate']:

                                if endpoint['name'] == systemName:

                                    endpoint['placeId'] = placeid

                    else:
                        logging.error('Unable to add WebexPlaceId on endpoint')
                        logging.error(v)

            return None

        except Exception as erro:

            logging.error('In addWebexPlaceId2Endpoint')
            logging.error(erro)

            return 'Error'


    def addWebexActivationCode2Endpoint(self, results, axapi):

        try:

            for result in results:

                for k, v in result.items():

                    if ('code' in v['response']) and(v['status'] == 200):

                        activationCode = v['response']['code']
                        placeId = v['response']['placeId']


                        for ip_key, endpoint in axapi.endpoints.items():

                            if ('placeId' in endpoint) and (endpoint['canMigrate'] == True):

                                if endpoint['placeId'] == placeId:

                                    endpoint['activationCode'] = activationCode

                    else:

                        logging.error(f'Issues obtaining the following code')
                        logging.error(v)

            return None

        except Exception as erro:

            logging.error('In addWebexActivationCode2Endpoint')
            logging.error(erro)

            return 'Error'


    def chunk_list(self,l,n):
        n = max(l, n)
        return (l[i:i + n] for i in range(0, len(l), n))

    def remove_arguments(self, command):

        try:
            if re.match('(.*)\((.*)\)', command) is not None:

                regex_result = re.search('(.*)\((.*)\)', command)

                return f'{regex_result.group(1)}()'

        except Exception as err:

            logging.error(err)

            return False

        return False

    def csv2json_axl(self,data):#TODO re-do when a different tab for expressways is don

        keyStr = data[0] #first line are always the headers
        keyList = keyStr.split(",")

        dict_data_list =[]
        row_counter = 0

        for row in data:
            if row_counter == 0:
                row_counter = row_counter + 1
            else:

                row_list = row.split(",")
                timer= len(keyList)
                data_counter = 0
                 #first row are headers
                temp_dict = {}

                while timer > 0:

                    key = keyList[data_counter]
                    value = row_list[data_counter]

                    timer = timer - 1
                    data_counter = data_counter +1

                    temp_dict[key] = value

                dict_data_list.append(temp_dict)

        return dict_data_list

    def csv2json(self,data):#TODO re-do when a different tab for expressways is don

        keyStr = data[0] #first line are always the headers
        keyList = keyStr.split(",")
        data.pop(0) #we won't need the heathers in data
        keyList.pop(0) #first item is the ipAddress, which we won't need here

        dict_data_list =[]

        for row in data:

            row_list = row.split(",")
            timer= len(keyList)
            counter = 0

            ip = row_list[0]
            row_list.pop(0) # removing the ip address
            temp_dict = {}
            temp_dict[ip] = {}
            while timer > 0:

                key = keyList[counter]
                value = row_list[counter]

                if key == "Priority":
                    value = int(value)

                temp_dict[ip][key] = value
                timer = timer - 1
                counter = counter +1

            dict_data_list.append(temp_dict)

        return dict_data_list


    def validate_tp_command(self, supported_commands, tp_cmd_list):

        logging.info('Validating commands...')

        for command in tp_cmd_list:

            is_good_command = False

            root_command = self.remove_arguments(command)

            if root_command is not None:

                for k, supported_cmd_list in supported_commands.items():

                    for supported_cmd in supported_cmd_list:

                        root_supported_cmd = self.remove_arguments(supported_cmd)

                        if root_command == root_supported_cmd:

                            is_good_command = True

                            break

                    if is_good_command:

                        break

                if is_good_command == False:


                    return {'valid': False, 'offendingCommand' : command}

                else:
                    pass

            else:

                return {'valid': False, 'offendingCommand': command}


        return {'valid': True, 'offendingCommand' : None}

    def getwebexToken(self):

        if os.path.exists(file_path):

            try:

                with open(file_path) as f:

                    encrypted_token = f.read()

                key = 'ZHsQaz82ylxBUYk8nwH750qHHnDMrNJurqLD8IhlFno='
                f = Fernet(key)

                webexAccessToken = f.decrypt(bytes(encrypted_token, encoding='utf-8')).decode('utf-8')
                return webexAccessToken

            except Exception as err:
                logging.error(err)
                return None

        if self.lineEdit_webex_token.text():

            webexAccessToken = self.lineEdit_webex_token.text()
            return webexAccessToken

        else:

            logging.error('No valid Webex token found, \n Please click the link for Webex Login authenticate in Webex')
            return None

    def execute_sql(self):

        logging.info("Pressed execute button under SQL tab")

        ucm_username = self.lineEdit_username_sql.text()
        ucm_password = self.lineEdit_password_sql.text()
        ucm_ip_address = self.lineEdit_ipaddress_sql.text()

        if self.validate_ip(ucm_ip_address) != None:


            logging.info('username: ' + ucm_username)
            logging.info('UCM IP address: ' + ucm_ip_address)
            logging.info('Creating UcmAXLConnection object for SQL execute ')

            # Create ZP object

            zp = UcmAXLConnection(ip = ucm_ip_address, usr = ucm_username,psw = ucm_password)

            logging.info('Default version: ' + zp.version)

            logging.info('WSDL ' + zp.wsdl)

            # get SQL query from UI box

            logging.info('UCMAXLConnection created! ')

            sql_query_text = self.SQLquery.toPlainText()

            logging.info('SQL query is: ' + sql_query_text)

            sql_response = zp.run_sql_query(sql_query_text)

            '''
            sql_result format
            {
                'num_rows': 19,
                'rows': [
                	{'name': 'CSF207CDBBE1F01',
                	'description': 'user1@canada.ca'},
                	{'name': 'CSF207CDBBE1F0D',
                	'description': 'user2@canada.ca'}
                	]
            }
            
            '''

            if sql_response != None:
                try:

                    if sql_response == '401':
                        logging.error('401 authentication failed, review and try again')
                        self.SQLresponse.setPlainText('401 authentication failed, review and try again')

                    if sql_response['rows'][0:5] == 'Error':
                        self.SQLresponse.setPlainText(sql_response['rows'])

                    elif sql_response['rows'] == 'None':
                        self.SQLresponse.setPlainText(sql_response['rows'])

                    elif 'The specified table' in sql_response['rows']:
                        self.SQLresponse.setPlainText(sql_response['rows'])

                    elif 'not found' in sql_response['rows']:
                        self.SQLresponse.setPlainText(sql_response['rows'])

                    else:
                        #show
                        self.SQLresponse.setPlainText(tabulate(sql_response['rows'], headers="keys"))

                except Exception as e:

                    logging.error(e)
                    sql_response = None

            else:
                logging.error('received None response from SQL query')

        else:
            logging.error('IP address: ' + ucm_ip_address + ' invalid, please correct and try again')
            self.SQLresponse.setPlainText('IP address: ' + ucm_ip_address + ' invalid, please correct and try again')



    def clean_clusterInfo_from_Paws(self, paws_cluster_info, username = '', password = ''):

        cleaned_cluster = list()


        for d in paws_cluster_info:

            logging.info('** d type ** ' + str(type(d)))

            temp_dict = dict()

            temp_dict['address'] = d['address']
            temp_dict['username'] = username
            temp_dict['password'] = password

            #temp_dict['hostname'] = d['hostname']
            #temp_dict['alias'] = d['alias']

            if d['type'] == 'cluster.node.type.primary':
                temp_dict['type'] = 'Publisher'

            elif d['type'] == 'cluster.node.type.secondary':
                temp_dict['type'] = 'Subscriber'

            elif d['type'] != 'cluster.node.type.secondary' and d['type'] != 'cluster.node.type.primary':
                temp_dict['type'] = 'unknown'
                logging.warning('cluster node type is not primary or secondary')

            if d['role'] == 1:
                temp_dict['role'] = 'UCM'

            elif d['role'] == 2:
                temp_dict['role'] = 'IMP'

            elif d['role'] != 1 and d['dbRole'] != 2:
                temp_dict['role'] = 'unknown'
                logging.warning('role is neither 1 or 2')

            '''
            if d['dbRole'] == 'cluster.node.type.primary':
                temp_dict['dbRole'] = 'Primary'
            elif d['dbRole'] == 'cluster.node.type.secondary':
                temp_dict['dbRole'] = 'Secondary'
            elif d['dbRole'] != 'cluster.node.type.primary' and d['dbRole'] != 'cluster.node.type.secondary':
                temp_dict['dbRole'] = 'unknown'
                logging.warning('dbRole is neither primary or secondary')

            if d['status'] == 'cluster.node.status.online':
                temp_dict['status'] = 'online'
            elif d['status'] == 'cluster.node.status.unknown':
                temp_dict['status'] = 'unknown'
            else:
                logging.error('Error on status, nether online nor unknown')
                temp_dict['status'] = d['status']
            '''

            cleaned_cluster.append(temp_dict)



        return cleaned_cluster

    #TODO move to a Webex Teams Plugin

    def setHeaders(self, token):
        accessToken_hdr = 'Bearer ' + token
        spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
        return spark_header

    def listRooms(self, the_header):
        uri = 'https://api.ciscospark.com/v1/rooms'
        fullRoomList = requests.get(uri, headers=the_header)
        fullRoomListJson = fullRoomList.json()
        logging.info('Printing URL\n')
        logging.info(fullRoomList.url)
        return fullRoomListJson

    def getRoomInfoByName(self,the_header, roomName):

        fullRoomListJson = self.listRooms(the_header)

        for item in fullRoomListJson['items']:
            # print(json.dumps(item,indent=4))
            if item['title'] == roomName:
                print(json.dumps(item, indent=4))
                return item
            else:
                pass
        return None

    def send_cli_to_spark(self):

        logging.info("Pressed send to spark in cli")

        spark_room = self.lineEdit_spark_to_address.text()

        logging.info('spark_address: ' + spark_room)

        token= "NDI1YjRlNWItNzA0YS00YTIwLThiZTktYjI1MTVhZTU3OGJiNGJlZmFlNWItNDNh"  # put your access token between the quotes
        header = self.setHeaders(token)

        room_info = self.getRoomInfoByName(header, spark_room)

        logging.info(room_info)

        cli_out_dir = cliPath


        iter = 1

        for filename in os.listdir(cli_out_dir):

            logging.info(os.listdir(cli_out_dir))
            logging.info(str(len(os.listdir(cli_out_dir))))
            logging.info(filename)

            file_path = os.path.join(cli_out_dir,filename)

            m = MultipartEncoder({'roomId': room_info['id'],
                                  'text': 'Attaching file ' + str(iter) + ' of ' + str(len(os.listdir(cli_out_dir))),
                                  'files': (file_path, open(file_path, 'rb'), 'text/txt')})

            r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                              headers={
                                  'Authorization': 'Bearer NDI1YjRlNWItNzA0YS00YTIwLThiZTktYjI1MTVhZTU3OGJiNGJlZmFlNWItNDNh',
                                  'Content-Type': m.content_type})

            logging.info(r.text)

            iter += 1

    def manualConnect(self):

        logging.info("Pressed connect button under Connection tab")

        # Pop up message init

        connect_message = QMessageBox()

        ucm_username = self.username_line.text()
        ucm_password = self.password_line.text()
        ucm_ip_address = self.ipAddress_line.text()
        nickname = self.nickname_line.text()

        logging.info('username: ' + ucm_username)
        logging.info('UCM IP address: ' + ucm_ip_address)
        logging.info('Nickname' + nickname)

        zp = UcmAXLConnection(ucm_ip_address,ucm_username,ucm_password)
        try:
            ucmVersion = zp.getCucmVersion()
        except ConnectionError:
            logging.error('Connection Error')

        if ucmVersion[0:5] == 'Error':
            connect_message.setText(ucmVersion)
            connect_message.exec_()
        else:
            # convert from list of 1 dict to a dict
            ucmVersion = ucmVersion[0]
            logging.info('UCM version: \n' + ucmVersion['cmversion'])
            connect_message.setText(ucmVersion['cmversion'])
            connect_message.exec_()

    def run_vosplugin(self,node, user, password, commands):

        logging.info('Running "run_vosplugin"')

        if self.cli_interrupt is not True:

            connection_error = False

            # if STOP button is pressed, stop

            if self.cli_interrupt:
                logging.warning('Interrupted!')

            file_out_path = os.path.join(cliPath, node + '_vos_cli' + '.txt')
            if os.path.exists(file_out_path):
                append_write = 'ab+'  # append if already exists
            else:
                append_write = 'wb+'  # make a new file if not


            connection = CliExpect()
            connection_str = connection.connect(node, user, password)

            if connection_str is not None and self.cli_interrupt is not True:
                with open(file_out_path, append_write) as f:
                    session_delimiter = '# Nautilus_' + time.strftime('%Y%m%d-%H%M\n\n')
                    f.write(session_delimiter.encode())
                    f.write(connection_str.encode())
                    if 1 + 1 == 3:
                        print('Really?')
                    else:
                        for cmd in commands:
                            # if STOP button is pressed, stop
                            if self.cli_interrupt:
                                logging.warning('Interrupted!')

                            r = connection.execute(cmd)
                            f.write(r.encode())
                            file_view_cmds = re.findall('file view activelog [^"\' ]+', r)
                            for cmd in file_view_cmds:
                                # if STOP button is pressed, stop
                                if self.cli_interrupt:
                                    logging.warning('Interrupted...')

                                logging.info('Found file view commands to execute')
                                res = connection.execute(cmd)
                                f.write(res.encode())
                        logging.info('An execution for a set of commands for ' + node + ' completed!')
            else:
                logging.info('Output not saved because previous connection failed')
        else:
            logging.info('Execution stopped because STOP CLI execution button was pressed')

    def start_server(self, path, port=8000):
        '''Start a simple webserver serving path on port'''
        os.chdir(path)
        httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
        httpd.serve_forever()

class ConsolePanelHandler(logging.Handler):

    def __init__(self, parent):
        logging.Handler.__init__(self)
        self.parent = parent

    def emit(self, record):
        self.parent.write(self.format(record))

'''
Multithreading

from https://martinfitzpatrick.name/article/multithreading-pyqt-applications-with-qthreadpool/

'''

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, node,user, password, commands,*args, **kwargs):

        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.node = node
        self.user = user
        self.password = password
        self.commands = commands
        self.signals = WorkerSignals()
        self.interrupted = False

        # Add the callback to our kwargs
        #kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them

        try:
            result = self.fn(self.node, self.user, self.password, self.commands, *self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done



class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    '''

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    stopit = pyqtSignal()

#Flask

# Old ClientID
# clientID = "Caea6a0b3da173f6643bad8ffd8efe0e789edd3225e6d0b3f20bf4bd01fe2c877"

#New ClientID

clientID = "C6940a8599ff65b3f5a678116acaef8737eac701ac87eb5999da971012d712587"

# Old secret ID
#secretID = "fec4f77a4ae4a40e41846136c7af676d26c740d82534a93e604922a54236a457"

# New Secret ID
secretID = "aa7d1dfcf943cc45ea926b243971cd75d575ab35697b6614120e8afa2c610e20"


redirectURI = "http://localhost:10060/oauth" #This could be different if you publicly expose this endpoint.
                                             # This is the redirect URI in my webex app

print('1. Starting Flask')

templates = os.path.join(dir_project, 'templates')
app = Flask(__name__, template_folder=templates)

def get_tokens(code):
    """Gets access token and refresh token"""
    logging.info('4. Obtaining access and refresh tokens')

    url = "https://api.ciscospark.com/v1/access_token"

    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}

    payload = (f"grant_type=authorization_code&client_id={clientID}&client_secret={secretID}"
               f"&code={code}&redirect_uri={redirectURI}")

    req = requests.post(url=url, data=payload, headers=headers)
    results = json.loads(req.text)
    access_token = results["access_token"]
    refresh_token = results["refresh_token"]

    return access_token, refresh_token

@app.route('/')
def index():

    print('2. Rendering main page')

    return render_template('index.html')

@app.route("/oauth") #Endpoint acting as Redirect URI.
def oauth():
    """Retrieves oauth code to generate tokens for users"""

    print('3. Obtaining authorization code')

    if "code" in request.args:

        state = request.args.get("state") #Captures value of the state.
        code = request.args.get("code") #Captures value of the code.

        access_token, refresh_token = get_tokens(code) #As you can see, get_tokens() uses the code and returns access and refresh tokens.


        print(f'###############################      WEBEX TOKEN      ##################################################')
        print(f'{access_token}')
        print(f'########################################################################################################')

        key = 'ZHsQaz82ylxBUYk8nwH750qHHnDMrNJurqLD8IhlFno=' #used to encrypt the Token (SALT)
        f = Fernet(key)

        encrypted_token = f.encrypt(bytes(access_token, encoding='utf-8')) #result is in bytes

        with open(file_path, 'w') as fout: #Encrypted webex token file path
            fout.write(encrypted_token.decode("utf-8")) #need to decode bytes to save as a String

        return render_template('granted.html')

    else:
        logging.info('in else in oauth')
        index_file = os.path.join(dir_project, 'templates\index.html')
        return render_template(index_file)

thread = threading.Thread(target=app.run, args=['localhost', 10060])
thread.daemon = True
thread.start()

if __name__ == "__main__":

    # Remove encrypted webex token if it exists, this forces new webex authentication each time the application is launched.
    print("Starting execution")
    try:
        os.remove(file_path)
    except OSError:
        pass

    logging.info('Executing')
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Nautilus()
    ui.setupUi(Dialog)
    Dialog.show()

    sys.exit(app.exec_())



