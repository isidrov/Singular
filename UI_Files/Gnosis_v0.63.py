# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Gnosis_v0.63.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Gnosis(object):
    def setupUi(self, Gnosis):
        Gnosis.setObjectName("Gnosis")
        Gnosis.resize(891, 874)
        Gnosis.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(Gnosis)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.globalwidget = QtWidgets.QTabWidget(Gnosis)
        self.globalwidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.globalwidget.setToolTip("")
        self.globalwidget.setInputMethodHints(QtCore.Qt.ImhSensitiveData)
        self.globalwidget.setObjectName("globalwidget")
        self.tab_SQL = QtWidgets.QWidget()
        self.tab_SQL.setObjectName("tab_SQL")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_SQL)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.SQLquery = QtWidgets.QPlainTextEdit(self.tab_SQL)
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
        self.verticalLayout_4.addWidget(self.SQLquery)
        self.SQLresponse = QtWidgets.QPlainTextEdit(self.tab_SQL)
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
        self.verticalLayout_4.addWidget(self.SQLresponse)
        self.widget_SQL_options = QtWidgets.QWidget(self.tab_SQL)
        self.widget_SQL_options.setMinimumSize(QtCore.QSize(0, 119))
        self.widget_SQL_options.setObjectName("widget_SQL_options")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_SQL_options)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget_credentials_sql = QtWidgets.QWidget(self.widget_SQL_options)
        self.widget_credentials_sql.setObjectName("widget_credentials_sql")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_credentials_sql)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_13 = QtWidgets.QWidget(self.widget_credentials_sql)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.widget_13)
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_ip_address_sql = QtWidgets.QLabel(self.widget_13)
        self.label_ip_address_sql.setObjectName("label_ip_address_sql")
        self.verticalLayout_13.addWidget(self.label_ip_address_sql)
        self.label_username_sql = QtWidgets.QLabel(self.widget_13)
        self.label_username_sql.setObjectName("label_username_sql")
        self.verticalLayout_13.addWidget(self.label_username_sql)
        self.label_password_sql = QtWidgets.QLabel(self.widget_13)
        self.label_password_sql.setObjectName("label_password_sql")
        self.verticalLayout_13.addWidget(self.label_password_sql)
        self.horizontalLayout_4.addWidget(self.widget_13)
        self.widget_15 = QtWidgets.QWidget(self.widget_credentials_sql)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_15.sizePolicy().hasHeightForWidth())
        self.widget_15.setSizePolicy(sizePolicy)
        self.widget_15.setObjectName("widget_15")
        self.lineEdit_ipaddress = QtWidgets.QLineEdit(self.widget_15)
        self.lineEdit_ipaddress.setGeometry(QtCore.QRect(9, 9, 133, 20))
        self.lineEdit_ipaddress.setObjectName("lineEdit_ipaddress")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_15)
        self.lineEdit_2.setGeometry(QtCore.QRect(9, 35, 133, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_password = QtWidgets.QLineEdit(self.widget_15)
        self.lineEdit_password.setGeometry(QtCore.QRect(9, 61, 133, 20))
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.horizontalLayout_4.addWidget(self.widget_15)
        self.horizontalLayout_5.addWidget(self.widget_credentials_sql)
        self.widget_executeSql = QtWidgets.QWidget(self.widget_SQL_options)
        self.widget_executeSql.setObjectName("widget_executeSql")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_executeSql)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButton_sql_execute = QtWidgets.QPushButton(self.widget_executeSql)
        self.pushButton_sql_execute.setObjectName("pushButton_sql_execute")
        self.verticalLayout_5.addWidget(self.pushButton_sql_execute)
        self.horizontalLayout_5.addWidget(self.widget_executeSql)
        self.widget_6 = QtWidgets.QWidget(self.widget_SQL_options)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5.addWidget(self.widget_6, 0, QtCore.Qt.AlignBottom)
        self.verticalLayout_4.addWidget(self.widget_SQL_options)
        self.globalwidget.addTab(self.tab_SQL, "")
        self.tab_cli = QtWidgets.QWidget()
        self.tab_cli.setObjectName("tab_cli")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.tab_cli)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.toolBox = QtWidgets.QToolBox(self.tab_cli)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 849, 758))
        self.page.setObjectName("page")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.page)
        self.horizontalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.widget_30 = QtWidgets.QWidget(self.page)
        self.widget_30.setMaximumSize(QtCore.QSize(600, 169865))
        self.widget_30.setObjectName("widget_30")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.widget_30)
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.widget_42 = QtWidgets.QWidget(self.widget_30)
        self.widget_42.setMaximumSize(QtCore.QSize(16777215, 32))
        self.widget_42.setObjectName("widget_42")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.widget_42)
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.UCMPub_Label = QtWidgets.QLabel(self.widget_42)
        self.UCMPub_Label.setObjectName("UCMPub_Label")
        self.horizontalLayout_25.addWidget(self.UCMPub_Label)
        self.UCMPub_IP_CLI_line = QtWidgets.QLineEdit(self.widget_42)
        self.UCMPub_IP_CLI_line.setMinimumSize(QtCore.QSize(0, 17))
        self.UCMPub_IP_CLI_line.setMaximumSize(QtCore.QSize(125, 16777215))
        self.UCMPub_IP_CLI_line.setObjectName("UCMPub_IP_CLI_line")
        self.horizontalLayout_25.addWidget(self.UCMPub_IP_CLI_line)
        self.verticalLayout_10.addWidget(self.widget_42)
        self.widget_43 = QtWidgets.QWidget(self.widget_30)
        self.widget_43.setMaximumSize(QtCore.QSize(16777215, 32))
        self.widget_43.setObjectName("widget_43")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout(self.widget_43)
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.UCMPubCLI_username_label = QtWidgets.QLabel(self.widget_43)
        self.UCMPubCLI_username_label.setObjectName("UCMPubCLI_username_label")
        self.horizontalLayout_26.addWidget(self.UCMPubCLI_username_label)
        self.UCMPub_Username_CLI_line = QtWidgets.QLineEdit(self.widget_43)
        self.UCMPub_Username_CLI_line.setMinimumSize(QtCore.QSize(117, 17))
        self.UCMPub_Username_CLI_line.setMaximumSize(QtCore.QSize(125, 16777215))
        self.UCMPub_Username_CLI_line.setObjectName("UCMPub_Username_CLI_line")
        self.horizontalLayout_26.addWidget(self.UCMPub_Username_CLI_line)
        self.verticalLayout_10.addWidget(self.widget_43)
        self.widget_44 = QtWidgets.QWidget(self.widget_30)
        self.widget_44.setMaximumSize(QtCore.QSize(16777215, 32))
        self.widget_44.setObjectName("widget_44")
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout(self.widget_44)
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_22 = QtWidgets.QLabel(self.widget_44)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_27.addWidget(self.label_22)
        self.UCMPub_Password_CLI_line = QtWidgets.QLineEdit(self.widget_44)
        self.UCMPub_Password_CLI_line.setMinimumSize(QtCore.QSize(117, 17))
        self.UCMPub_Password_CLI_line.setMaximumSize(QtCore.QSize(125, 16777215))
        self.UCMPub_Password_CLI_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.UCMPub_Password_CLI_line.setObjectName("UCMPub_Password_CLI_line")
        self.horizontalLayout_27.addWidget(self.UCMPub_Password_CLI_line)
        self.verticalLayout_10.addWidget(self.widget_44)
        self.widget_45 = QtWidgets.QWidget(self.widget_30)
        self.widget_45.setMinimumSize(QtCore.QSize(0, 35))
        self.widget_45.setMaximumSize(QtCore.QSize(16777215, 40))
        self.widget_45.setObjectName("widget_45")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.widget_45)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.pushButton_discover_nodes_UCM = QtWidgets.QPushButton(self.widget_45)
        self.pushButton_discover_nodes_UCM.setMinimumSize(QtCore.QSize(20, 20))
        self.pushButton_discover_nodes_UCM.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_discover_nodes_UCM.setObjectName("pushButton_discover_nodes_UCM")
        self.horizontalLayout_13.addWidget(self.pushButton_discover_nodes_UCM)
        self.verticalLayout_10.addWidget(self.widget_45)
        self.widget_46 = QtWidgets.QWidget(self.widget_30)
        self.widget_46.setObjectName("widget_46")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.widget_46)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.tableWidget_ucm_cluster_cli = QtWidgets.QTableWidget(self.widget_46)
        self.tableWidget_ucm_cluster_cli.setAlternatingRowColors(True)
        self.tableWidget_ucm_cluster_cli.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_ucm_cluster_cli.setShowGrid(False)
        self.tableWidget_ucm_cluster_cli.setColumnCount(6)
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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_ucm_cluster_cli.setHorizontalHeaderItem(5, item)
        self.tableWidget_ucm_cluster_cli.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_ucm_cluster_cli.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout_17.addWidget(self.tableWidget_ucm_cluster_cli)
        self.verticalLayout_10.addWidget(self.widget_46)
        self.horizontalLayout_30.addWidget(self.widget_30)
        self.widget_47 = QtWidgets.QWidget(self.page)
        self.widget_47.setObjectName("widget_47")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.widget_47)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.widget_49 = QtWidgets.QWidget(self.widget_47)
        self.widget_49.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_49.setObjectName("widget_49")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.widget_49)
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.treeWidget_ucm_cli = QtWidgets.QTreeWidget(self.widget_49)
        self.treeWidget_ucm_cli.setToolTip("")
        self.treeWidget_ucm_cli.setStatusTip("")
        self.treeWidget_ucm_cli.setObjectName("treeWidget_ucm_cli")
        self.verticalLayout_20.addWidget(self.treeWidget_ucm_cli)
        self.verticalLayout_12.addWidget(self.widget_49)
        self.widget_50 = QtWidgets.QWidget(self.widget_47)
        self.widget_50.setMinimumSize(QtCore.QSize(0, 50))
        self.widget_50.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_50.setObjectName("widget_50")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.widget_50)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.pushButton_execute_cli_ucm = QtWidgets.QPushButton(self.widget_50)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_execute_cli_ucm.sizePolicy().hasHeightForWidth())
        self.pushButton_execute_cli_ucm.setSizePolicy(sizePolicy)
        self.pushButton_execute_cli_ucm.setObjectName("pushButton_execute_cli_ucm")
        self.verticalLayout_14.addWidget(self.pushButton_execute_cli_ucm)
        self.pushButton_stop_cli_ucm = QtWidgets.QPushButton(self.widget_50)
        self.pushButton_stop_cli_ucm.setObjectName("pushButton_stop_cli_ucm")
        self.verticalLayout_14.addWidget(self.pushButton_stop_cli_ucm)
        self.verticalLayout_12.addWidget(self.widget_50)
        self.horizontalLayout_30.addWidget(self.widget_47)
        self.toolBox.addItem(self.page, "")
        self.generic_VOS_QWidget = QtWidgets.QWidget()
        self.generic_VOS_QWidget.setGeometry(QtCore.QRect(0, 0, 483, 231))
        self.generic_VOS_QWidget.setObjectName("generic_VOS_QWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.generic_VOS_QWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(self.generic_VOS_QWidget)
        self.widget.setObjectName("widget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget_11 = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy)
        self.widget_11.setObjectName("widget_11")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_11)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.widget_5 = QtWidgets.QWidget(self.widget_11)
        self.widget_5.setMinimumSize(QtCore.QSize(0, 82))
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_7 = QtWidgets.QWidget(self.widget_5)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.widget_8 = QtWidgets.QWidget(self.widget_7)
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_8)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_ip_vos_gen = QtWidgets.QLabel(self.widget_8)
        self.label_ip_vos_gen.setObjectName("label_ip_vos_gen")
        self.verticalLayout_6.addWidget(self.label_ip_vos_gen)
        self.label_username_vos_gen = QtWidgets.QLabel(self.widget_8)
        self.label_username_vos_gen.setObjectName("label_username_vos_gen")
        self.verticalLayout_6.addWidget(self.label_username_vos_gen)
        self.label_password_vos_gen = QtWidgets.QLabel(self.widget_8)
        self.label_password_vos_gen.setObjectName("label_password_vos_gen")
        self.verticalLayout_6.addWidget(self.label_password_vos_gen)
        self.horizontalLayout_8.addWidget(self.widget_8)
        self.widget_9 = QtWidgets.QWidget(self.widget_7)
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_9)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lineEdit_vos_gen_ip_address = QtWidgets.QLineEdit(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_vos_gen_ip_address.sizePolicy().hasHeightForWidth())
        self.lineEdit_vos_gen_ip_address.setSizePolicy(sizePolicy)
        self.lineEdit_vos_gen_ip_address.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_vos_gen_ip_address.setObjectName("lineEdit_vos_gen_ip_address")
        self.verticalLayout_7.addWidget(self.lineEdit_vos_gen_ip_address)
        self.lineEdit_vos_gen_username = QtWidgets.QLineEdit(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_vos_gen_username.sizePolicy().hasHeightForWidth())
        self.lineEdit_vos_gen_username.setSizePolicy(sizePolicy)
        self.lineEdit_vos_gen_username.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_vos_gen_username.setObjectName("lineEdit_vos_gen_username")
        self.verticalLayout_7.addWidget(self.lineEdit_vos_gen_username)
        self.lineEdit_vos_gen_password = QtWidgets.QLineEdit(self.widget_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_vos_gen_password.sizePolicy().hasHeightForWidth())
        self.lineEdit_vos_gen_password.setSizePolicy(sizePolicy)
        self.lineEdit_vos_gen_password.setMinimumSize(QtCore.QSize(0, 20))
        self.lineEdit_vos_gen_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_vos_gen_password.setObjectName("lineEdit_vos_gen_password")
        self.verticalLayout_7.addWidget(self.lineEdit_vos_gen_password)
        self.horizontalLayout_8.addWidget(self.widget_9)
        self.horizontalLayout_2.addWidget(self.widget_7)
        self.widget_10 = QtWidgets.QWidget(self.widget_5)
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_12 = QtWidgets.QWidget(self.widget_10)
        self.widget_12.setObjectName("widget_12")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_12)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_product_vos_gen = QtWidgets.QLabel(self.widget_12)
        self.label_product_vos_gen.setObjectName("label_product_vos_gen")
        self.horizontalLayout_7.addWidget(self.label_product_vos_gen)
        self.comboBox_product_vos_gen = QtWidgets.QComboBox(self.widget_12)
        self.comboBox_product_vos_gen.setObjectName("comboBox_product_vos_gen")
        self.comboBox_product_vos_gen.addItem("")
        self.comboBox_product_vos_gen.addItem("")
        self.comboBox_product_vos_gen.addItem("")
        self.comboBox_product_vos_gen.addItem("")
        self.horizontalLayout_7.addWidget(self.comboBox_product_vos_gen)
        self.verticalLayout_3.addWidget(self.widget_12)
        self.pushButton_add_node_vos_gen = QtWidgets.QPushButton(self.widget_10)
        self.pushButton_add_node_vos_gen.setObjectName("pushButton_add_node_vos_gen")
        self.verticalLayout_3.addWidget(self.pushButton_add_node_vos_gen)
        self.horizontalLayout_2.addWidget(self.widget_10)
        self.verticalLayout_11.addWidget(self.widget_5)
        self.widget_14 = QtWidgets.QWidget(self.widget_11)
        self.widget_14.setObjectName("widget_14")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout(self.widget_14)
        self.horizontalLayout_28.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.tableWidget_vos_gen = QtWidgets.QTableWidget(self.widget_14)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_vos_gen.sizePolicy().hasHeightForWidth())
        self.tableWidget_vos_gen.setSizePolicy(sizePolicy)
        self.tableWidget_vos_gen.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_vos_gen.setAlternatingRowColors(True)
        self.tableWidget_vos_gen.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_vos_gen.setShowGrid(False)
        self.tableWidget_vos_gen.setColumnCount(4)
        self.tableWidget_vos_gen.setObjectName("tableWidget_vos_gen")
        self.tableWidget_vos_gen.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_vos_gen.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_vos_gen.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_vos_gen.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_vos_gen.setHorizontalHeaderItem(3, item)
        self.tableWidget_vos_gen.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_vos_gen.horizontalHeader().setStretchLastSection(False)
        self.horizontalLayout_28.addWidget(self.tableWidget_vos_gen)
        self.verticalLayout_11.addWidget(self.widget_14)
        self.verticalLayout_8.addWidget(self.widget_11)
        self.horizontalLayout.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(self.generic_VOS_QWidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.treeWidget_vos_gen_cli = QtWidgets.QTreeWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget_vos_gen_cli.sizePolicy().hasHeightForWidth())
        self.treeWidget_vos_gen_cli.setSizePolicy(sizePolicy)
        self.treeWidget_vos_gen_cli.setToolTip("")
        self.treeWidget_vos_gen_cli.setStatusTip("")
        self.treeWidget_vos_gen_cli.setObjectName("treeWidget_vos_gen_cli")
        self.verticalLayout_9.addWidget(self.treeWidget_vos_gen_cli)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_execute_vos_gen = QtWidgets.QPushButton(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_execute_vos_gen.sizePolicy().hasHeightForWidth())
        self.pushButton_execute_vos_gen.setSizePolicy(sizePolicy)
        self.pushButton_execute_vos_gen.setObjectName("pushButton_execute_vos_gen")
        self.verticalLayout.addWidget(self.pushButton_execute_vos_gen)
        self.pushButton_stop_vos_gen = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_stop_vos_gen.setObjectName("pushButton_stop_vos_gen")
        self.verticalLayout.addWidget(self.pushButton_stop_vos_gen)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.horizontalLayout.addWidget(self.widget_2)
        self.toolBox.addItem(self.generic_VOS_QWidget, "")
        self.horizontalLayout_12.addWidget(self.toolBox)
        self.globalwidget.addTab(self.tab_cli, "")
        self.horizontalLayout_9.addWidget(self.globalwidget)

        self.retranslateUi(Gnosis)
        self.globalwidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Gnosis)

    def retranslateUi(self, Gnosis):
        _translate = QtCore.QCoreApplication.translate
        Gnosis.setWindowTitle(_translate("Gnosis", "Gnosis"))
        self.SQLquery.setPlainText(_translate("Gnosis", "select name, description from device where name like \'SEP%\'"))
        self.label_ip_address_sql.setText(_translate("Gnosis", "IP address"))
        self.label_username_sql.setText(_translate("Gnosis", "Username"))
        self.label_password_sql.setText(_translate("Gnosis", "Password"))
        self.pushButton_sql_execute.setText(_translate("Gnosis", "Execute Query"))
        self.globalwidget.setTabText(self.globalwidget.indexOf(self.tab_SQL), _translate("Gnosis", "SQL"))
        self.UCMPub_Label.setText(_translate("Gnosis", "PUB IP"))
        self.UCMPubCLI_username_label.setText(_translate("Gnosis", "Username"))
        self.label_22.setText(_translate("Gnosis", "Password"))
        self.pushButton_discover_nodes_UCM.setText(_translate("Gnosis", "Discover Cluster"))
        self.tableWidget_ucm_cluster_cli.setSortingEnabled(True)
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(0)
        item.setText(_translate("Gnosis", "address"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(1)
        item.setText(_translate("Gnosis", "role"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(2)
        item.setText(_translate("Gnosis", "type"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(3)
        item.setText(_translate("Gnosis", "dbRole"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(4)
        item.setText(_translate("Gnosis", "hostname"))
        item = self.tableWidget_ucm_cluster_cli.horizontalHeaderItem(5)
        item.setText(_translate("Gnosis", "status"))
        self.treeWidget_ucm_cli.headerItem().setText(0, _translate("Gnosis", "CLI Commands"))
        self.pushButton_execute_cli_ucm.setText(_translate("Gnosis", "START"))
        self.pushButton_stop_cli_ucm.setText(_translate("Gnosis", "STOP"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("Gnosis", "UCM/IMP autodiscovery"))
        self.label_ip_vos_gen.setText(_translate("Gnosis", "IP address"))
        self.label_username_vos_gen.setText(_translate("Gnosis", "Username"))
        self.label_password_vos_gen.setText(_translate("Gnosis", "Password"))
        self.label_product_vos_gen.setText(_translate("Gnosis", "Product"))
        self.comboBox_product_vos_gen.setItemText(0, _translate("Gnosis", "UCM"))
        self.comboBox_product_vos_gen.setItemText(1, _translate("Gnosis", "IMP"))
        self.comboBox_product_vos_gen.setItemText(2, _translate("Gnosis", "CUC"))
        self.comboBox_product_vos_gen.setItemText(3, _translate("Gnosis", "CER"))
        self.pushButton_add_node_vos_gen.setText(_translate("Gnosis", "Add node"))
        self.tableWidget_vos_gen.setSortingEnabled(True)
        item = self.tableWidget_vos_gen.horizontalHeaderItem(0)
        item.setText(_translate("Gnosis", "address"))
        item = self.tableWidget_vos_gen.horizontalHeaderItem(1)
        item.setText(_translate("Gnosis", "user"))
        item = self.tableWidget_vos_gen.horizontalHeaderItem(2)
        item.setText(_translate("Gnosis", "password"))
        item = self.tableWidget_vos_gen.horizontalHeaderItem(3)
        item.setText(_translate("Gnosis", "role"))
        self.treeWidget_vos_gen_cli.headerItem().setText(0, _translate("Gnosis", "CLI Commands"))
        self.pushButton_execute_vos_gen.setText(_translate("Gnosis", "START"))
        self.pushButton_stop_vos_gen.setText(_translate("Gnosis", "STOP"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.generic_VOS_QWidget), _translate("Gnosis", "Add VOS nodes manually"))
        self.globalwidget.setTabText(self.globalwidget.indexOf(self.tab_cli), _translate("Gnosis", "Platform"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Gnosis = QtWidgets.QDialog()
    ui = Ui_Gnosis()
    ui.setupUi(Gnosis)
    Gnosis.show()
    sys.exit(app.exec_())
