"""Responsible managing client side of client/server socket communication.


"""

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket



class ClientSocketManager(QtCore.QObject):
    """
    Handles all things tcp socket for client.
    
    Attributes
    ----------
    
    Methods
    ----------
    
    """
    def __init__(self):
        QtCore.QObject.__init__(self)
        
        self._socket = None
        self.SERVER_IP = None
        self.SERVER_LISTEN_PORT = None
        self._server_connect_handler = None
        

    def configure_socket(self):
        """Creates and configures our comm socket"""
        
        if self._socket == None:
            self._socket = QTcpSocket()
            self._socket.error.connect(self.on_errer)
            self._socket.connected.connect(self.on_connected)
            self._socket.readyRead.connect(self.on_got_data)
            return True
        else:
            #need custom exception and try except
            print('Old socket still exists!, No new connect')
            return False
        
        
    @pyqtSlot()    
    def on_error(self, error):
        """ captures any errors that occur to the socket"""
        s = self._socket
        
        if error == QAbstractSocket.ConnectionRefusedError:
            print(f'Connection refused -- ip:port {s.peerAddress()}:{s.peerPort()}')
            self._server_connect_handler(False)
        else:
            print(s.errorString())

    @pyqtSlot()
    def on_connected(self):
        "We have a connection with the server!"
        self._server_connect_handler(True)
        
    @pyqtSlot()
    def on_got_data(self):
        pass
        
       
    def try_server_connnection(self, ip, port):
        """Attempts to connect to server. If this much of the attempt works,
        True is returned. If socket config fails, False is returned. Both of
        these returns have a message with them in this order: TorF, msg. The
        caller SHOULD NOT ASSUME CONNECTION IS COMPLETE - wait for call to their
        connection notification handler."""
        self.SERVER_IP = ip
        self.SERVER_LISTEN_PORT = port
        #create our socket and attempt connection
        if self.configure_socket():
            self._socket.connectToHost(self.SERVER_IP, self.port)
            return True, "Attempting connection..."
        else:
            return False, "Socket config failed, aborting connection attempt"


    def set_connection_attempt_result_handler(self, handler):
        """Used to get a notification whether or not the
        server connection attempt was successful. The
        passed in handler function should be of the form
        <handler_name>( result:boolean)"""
        self._server_connect_handler = handler
            
            
    def disconnect_from_server(self):
        print("NEED TO IMPLEMENT disconnect_from_server")
    
         
    def get_client_ip_and_port(self):
        print("NEED TO IMPLEMENT get_client_ip_and_port")
        return "127.0.0.1", "unknown"
        



        
