"""Responsible managing server side of client/server socket communication.

Contains 2 classes, ClientConnection and ServerSocketManager.

ServerSocketManager is responsible for managing connections with clients that
connect. These are asynchronous peer-peer communications.

ClientConnection is a helper class used by ServerSocketManager that stores
client connection information for a connnected client.
"""
from PyQt5 import QtCore, QtNetwork
from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

class ClientConnection:
    """ stores connection info for active clients that have connected to the
server"""
    def __init__(self, socket=None):
        self.socket = socket
        self.ip_addr = socket.peerAddress()
        self.port = socket.peerPort
        self.client_id = socket.peerName

class ServerSocketManager(QtCore.QObject):
    """Handles all things tcp sockets for the server. This consists of setting
up a listening csocket, managing connections, deciding which clients to send
messages to, and acting on their messages if needed."""
    def __init__(self):
        QtCore.QObject.__init__(self)
        
        self.SERVER_IP = "127.0.0.1"
        self.SERVER_LISTEN_PORT = 7011
        self.SERVER_MAX_CONNECTIONS = 5
        self._new_client_notification_handler = None
        
        self._active_client_list = [] #type: ClientConnection
        
        self._server = QtNetwork.QTcpServer()
        self._server.setMaxPendingConnections(self.SERVER_MAX_CONNECTIONS)
        self._server.newConnection.connect(self.on_new_connection)
        
    @pyqtSlot()
    def on_start_server(self):
        print('starting server')
        if self._server.listen( QtNetwork.QHostAddress.Any, self.SERVER_LISTEN_PORT):
            print(f'Listening at {self.SERVER_IP}:{self.SERVER_LISTEN_PORT}')
        else:
            print(f'Server listen broken')
        
    @pyqtSlot()    
    def on_new_connection(self):
        print('got new connection')
        if len(self._active_server_list) >= self.SERVER_MAX_CONNECTIONS:
            print("TOO MANY CONNECTIONS - need to raise an exception")
        else:
            client_socket = self._listen_server.nextPendingConnection()
            new_client = ClientConnection(client_socket)
            self._active_client_list.append(new_client)
    
    def get_server_ip_and_port(self):
        return self.SERVER_IP, self.SERVER_LISTEN_PORT


    def notify_about_new_connection(self, handler):
        """Cheesy way to let the main dialog know we have a new client
        connection. This needs to be a signal emit for the main body"""
        self._new_client_notification_handler = handler
        #see next function
        
    def get_new_client_info(self):
        """the handler for new client should call this routine"""
        new_client = self._active_client_list[-1]
        return new_client.client_id, new_client.ip_addr, new_client.port

            
       
       