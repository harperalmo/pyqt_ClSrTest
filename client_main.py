"""Responsible for connecting user interaction with gui with program actions

Contains the class ClientSocketChat, which connects the PyQt5 GUI dialog box
interface to the program operations. The imported client_socket_manager module
contains a ClientSocketManager class, an instance of which is created here to
manage the client side for one client of a multi-client/single-server
asynchronous communication system.
"""
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import client_socket_manager


class ClientSocketChat(QDialog):
    """
    Connects PyQt5 gui to internal operations for client socket comm
    
    Attributes
    ----------
    
    
    Methods
    ---------
    
    """
    
    def __init__(self):
        super(ClientSocketChat, self).__init__()
        loadUi('ClientDlg.ui', self)
        
        self._socket_mgr = client_socket_manager.ClientSocketManager()
        self._socket_mgr.set_connection_attempt_result_handler(self.connect_notify_handler)
        self._client_ip, self._client_port = self._socket_mgr.get_client_ip_and_port()
        
        #initial widget configuration
        self.lbl_client_ip.setText(self._client_ip)
        self.lbl_client_port.setText(self._client_port)
        self._status = "Not connected"
        self.lbl_status.setText(self._status)
        self.pBtn_connect_to_server.setEnabled(True) #should be checking ip,
        self.pBtn_disconnect_from_server.setEnabled(False)
        self.gBx_chat.setEnabled(False)
        #signal/slot hookup
        self.pBtn_connect_to_server.clicked.connect(self.connect_server)
        self.pBtn_disconnect_from_server.clicked.connect(self.disconnect_server)
        self.pBtn_send_msg.clicked.connect(self.send_msg)
        self.pBtn_close.clicked.connect(self.close_dlg)
        
                


    @pyqtSlot()
    def connect_server(self):
        result, message = self._socket_mgr.try_server_connection('127.0.0.1', 7011)
        if result:
            print(f'Connection processing - {message} - ')
        else:
            print(message)
            
    
    @pyqtSlot()
    def disconnect_server(self):
        pass
    
    
    @pyqtSlot()
    def send_msg(self):
        pass
                        
    @pyqtSlot()
    def close_dlg(self):
        self.reject()
        
    def connect_notify_handler(self, result):
        if result:
            print('got connection')
            self.gBx_chat.setEnabled(True)
        else:
            print('oh well, connection failed')
            
            
def main():
    app = QApplication(sys.argv)
    cDlg=ClientSocketChat()
    cDlg.show()
    sys.exit(app.exec ())

if __name__=="__main__":
    main()
