"""Responsible for connecting user interaction with gui with program actions

Contains the class ServerSocketChat, which connects the PyQt5 GUI dialog box
interface to the program operations. The imported server_socket_manager module
contains a ServerSocketManager class, an instance of which is created here to
manage the server side of a multi-client/single-server asynchronous
communication system.
"""

import sys
from PyQt5.QtCore import pyqtSlot, QDataStream, QIODevice, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
import server_socket_manager



class ServerSocketChat(QDialog):
    """Dialog for managing multiple client asynchronous communication chats.

    Attributes
    ----------
    
    Methods
    ---------
    
    
    
    """
    
    def __init__(self):
        super(ServerSocketChat, self).__init__()
        loadUi('ServerDlg.ui', self)


        
        self._status = "Not listening"

        self.client_msg_count = 0
        
        #initial widget configuration
        self.gBx_chat.setEnabled(False)
        self.lbl_status.setText(self._status)
        
        self._server = None
       # self.configure_server()
        self._server = server_socket_manager.ServerSocketManager()
        self._ip_addr, self._port = self._server.get_server_ip_and_port()
        self._server.notify_about_new_connection(self.new_client_handler)

        
        self._max_client_count = self._server.SERVER_MAX_CONNECTIONS
        self.configure_connection_table()
        #signals and slots
        self.pBtn_listen.clicked.connect(self.begin_listening)
        self.pBtn_listen.clicked.connect(self._server.on_start_server)
        self.pBtn_send_msg.clicked.connect(self.send_msg_to_client)
        self.pBtn_close.clicked.connect(self.close_dlg)
 
 
    def new_client_handler(self):
        print('NEED TO DEFINE new_client_handler')
        client_id, ip, port = self._server.get_new_client_info()
  
    
    def configure_connection_table(self):
        header_list = ['Client','IPAddress','Port',]
        t = self.tbl_connection_list
        t.setHorizontalHeaderLabels(header_list)
     
        for c in range(len(header_list)):
            for r in range( self._max_client_count):
                item = QTableWidgetItem()
                item.setFlags( item.flags() & ~(Qt.ItemIsEditable | Qt.ItemIsSelectable)) 
                t.setItem(r,c, item)

 
                    
      #  t.setItem(0,0, QTableWidgetItem('Client X'))
       # t.setItem(0,1, QTableWidgetItem('127.0.0.1'))
        #t.setItem(0,2, QTableWidgetItem('7701'))
       # item= t.item(0,0)
       # self.le_msg_from_client.setText(item.text())
        
        
    @pyqtSlot()
    def begin_listening(self):
        self._status="Listening..."
        self.lbl_status.setText(self._status)
        
    
    
    @pyqtSlot()
    def send_msg_to_client(self):
        msg = self.le_msg_to_client.text()
        print(f'Msg: <{msg}>')
        self.client_msg_count += 1
        self.le_msg_from_client.setText(f"pseudo message {self.client_msg_count}")
    
    @pyqtSlot()
    def close_dlg(self):
        self.reject()
        
    
    
def main():
    app = QApplication(sys.argv)
    dlg=ServerSocketChat()
    dlg.show()
    sys.exit(app.exec ())

if __name__=="__main__":
    main()