#  gui for dvic chatroom using PyQT
#  2023-01-27

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QComboBox, QCheckBox, QRadioButton, QButtonGroup, QGroupBox, QFileDialog, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMenu, QAction, QInputDialog, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QCursor
from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtNetwork import QTcpSocket, QHostAddress, QAbstractSocket

import dvic_chat.client as client

class paramSelectorWidget():
    #  this widgets is used to select the ip, port and username for the chatroom
    def __init__(self, parent):
        self.parent = parent
        self.widget = QWidget()
        self.widget.setWindowTitle("DVIC Chatroom")
        # self.widget.setWindowIcon(QIcon("dvic_chatroom.png"))
        self.widget.setFixedSize(300, 200)

        self.ipLabel = QLabel("IP:")
        self.ipLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ipInput = QLineEdit()
        self.ipInput.setText(" ")
        self.ipInput.setFixedWidth(150)

        self.portLabel = QLabel("Port:")
        self.portLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.portInput = QLineEdit()
        self.portInput.setText(" ")
        self.portInput.setFixedWidth(150)

        self.usernameLabel = QLabel("Username:")
        self.usernameLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.usernameInput = QLineEdit()
        self.usernameInput.setText(" ")
        self.usernameInput.setFixedWidth(150)

        self.connectButton = QPushButton("Connect")
        self.connectButton.clicked.connect(self.connect)

        self.layout = QGridLayout()
        self.layout.addWidget(self.ipLabel, 0, 0)
        self.layout.addWidget(self.ipInput, 0, 1)
        self.layout.addWidget(self.portLabel, 1, 0)
        self.layout.addWidget(self.portInput, 1, 1)
        self.layout.addWidget(self.usernameLabel, 2, 0)
        self.layout.addWidget(self.usernameInput, 2, 1)
        self.layout.addWidget(self.connectButton, 3, 0, 1, 2)

        self.widget.setLayout(self.layout)

    def connect(self):
        self.parent.ip = self.ipInput.text()
        self.parent.port = int(self.portInput.text())
        self.parent.username = self.usernameInput.text()
        self.parent.connect()
        self.widget.close()

class chatroomWidget():
    #  this widget is used to display the chatroom
    def __init__(self, parent):
        self.parent = parent
        self.widget = QWidget()
        self.widget.setWindowTitle("DVIC Chatroom")
        # self.widget.setWindowIcon(QIcon("dvic_chatroom.png"))
        self.widget.setFixedSize(800, 600)

        self.messages = QTableWidget()
        self.messages.setColumnCount(1)
        self.messages.setRowCount(0)
        self.messages.verticalHeader().setVisible(False)
        self.messages.horizontalHeader().setVisible(False)
        self.messages.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.messages.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.messages.setContextMenuPolicy(Qt.CustomContextMenu)
        self.messages.customContextMenuRequested.connect(self.messagesContextMenu)

        self.input = QLineEdit()
        self.input.returnPressed.connect(self.sendMessage)

        self.layout = QGridLayout()
        self.layout.addWidget(self.messages, 0, 0, 1, 2)
        self.layout.addWidget(self.input, 1, 0)
        self.widget.setLayout(self.layout)

    def messagesContextMenu(self, pos):
        menu = QMenu()
        copyAction = QAction("Copy", self.widget)
        copyAction.triggered.connect(self.copyMessage)
        menu.addAction(copyAction)
        menu.exec_(QCursor.pos())

    def copyMessage(self):
        selected = self.messages.selectedItems()
        if len(selected) > 0:
            QApplication.clipboard().setText(selected[0].text())

    def sendMessage(self):
        self.parent.sendMessage(self.input.text())
        self.input.setText("")
        self.input.setFocus()

class chatroom():
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.paramSelector = paramSelectorWidget(self)
        self.paramSelector.widget.show()

        self.chatroom = chatroomWidget(self)
        # self.chatroom.widget.show()

        self.client = None
        self.ip = None
        self.port = None
        self.username = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.receiveMessage)
        self.timer.start(10)



        self.app.exec_()

    def connect(self):
        if self.ip == None or self.port == None or self.username == None:
            return
        self.client = client.DVICChatClient(address=self.ip, port=self.port, username=self.username)
        if self.client.connect():
            self.chatroom.widget.show()

    def sendMessage(self, message):
        if self.client == None:
            print("Client not connected")
            return
        self.client.send_message(message)

    def receiveMessage(self):
        #  check client queue for new messages
        if self.client == None:
            return
        if self.client.received_messages.empty():
            return
        message = self.client.received_messages.get()
        #  add message to chatroom at the botoom
        self.chatroom.messages.insertRow(self.chatroom.messages.rowCount())
        self.chatroom.messages.setItem(self.chatroom.messages.rowCount()-1, 0, QTableWidgetItem(message))
        #  update scroll bar
        self.chatroom.messages.scrollToBottom()

if __name__ == "__main__":
    chatroom()

