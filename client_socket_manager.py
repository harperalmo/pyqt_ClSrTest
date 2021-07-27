"""
Manages client side of client/server socket communication.


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
            self._socket.error.connect(self.on_error)
            self._socket.connected.connect(self.on_connected)
            self._socket.readyRead.connect(self.on_got_msg)
            return True
        else:
            #need custom exception and try except
            print('Old socket still exists!, No new connect')
            return False
        
        
    @pyqtSlot()    
    def on_error(self):
        """ captures any errors that occur to the socket"""
        print('In on_error')
        s = self._socket
        myerror = 0
        
        if myerror == QAbstractSocket.ConnectionRefusedError:
            print(f'Connection refused -- ip:port: <{s.peerAddress().toString()[7:]}>:<{s.peerPort()}>')
            self._server_connect_handler(False)
        else:
            print(s.errorString())
        del(s)
        self._socket=None
        print('leaving on_error')

    @pyqtSlot()
    def on_connected(self):
        print("We have a connection with the server!")
        self._server_connect_handler(True)
        
    @pyqtSlot()
    def on_got_msg(self):
        qba_msg = self._socket.readAll()
        str_msg = str(qba_msg.data(), encoding='utf-8')
        print(f'Message: <{str_msg}>')
    
    
    def send_msg(self, msg):
        """sends a message to the server"""
        b = bytearray(msg, encoding='utf-8')
        self._socket.write(b)
        self._socket.flush()
        
        
    def get_client_ip_and_port(self):
        print("NEED TO IMPLEMENT get_client_ip_and_port")
        return "127.0.0.1", "unknown"
    
    
    def try_server_connection(self, ip, s_port):
        """Attempts to connect to server. If this much of the attempt works,
        True is returned. If socket config fails, False is returned. Both of
        these returns have a message with them in this order: TorF, msg. The
        caller SHOULD NOT ASSUME CONNECTION IS COMPLETE - wait for call to their
        connection notification handler."""
        self.SERVER_IP = ip
        self.SERVER_LISTEN_PORT = s_port
        #create our socket and attempt connection
        
        if self.configure_socket():
            self._socket.connectToHost(ip, s_port)
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
    
         

        



        
