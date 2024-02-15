#This file defines the ClientNetworkManager class, 
# which handles socket communication with the server. 
# The manager initializes a socket, sets the host and port, 
# and connects to the server upon request. 
# It also provides methods for sending and receiving JSON data.

# Import necessary modules

import socket
import json
# gia na pairnei kai an dinei data mesa sto diadiktei kai n sundetai 
# Class for managing client-side network communication
# 
class ClientNetworkManager:
    def __init__(self):
         # Initialize the client socket and connection details
        # Initialize the client network manager with socket, host, and port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ""  
        self.port = 8080
        self.addr = (self.host, self.port)
        self.id = None

    def connect(self):
        # Attempt to establish a connection to the server
        # Connect to the server
        try:
            print(self.addr)
            self.client.connect(self.addr)
            
            return True
        except socket.error as e: 
            print(f"Error connecting to the server: {e}")
            return False

    def setHost(self, _host):
         # Set the host address
        self.host = _host
        self.addr = (self.host, self.port)

    def getHost(self):
        # Get the current host address
        return self.host
    
    def send(self, data):
        # Send data to the server in JSON format
        # Send JSON-encoded data to the server
        try:
            json_data = json.dumps(data)
            self.client.sendall(str.encode(json_data))

        except socket.error as e:
            return str(e)
        
    def sendJSON(self, data):
        # Send raw JSON data to the server
        try:
            self.client.sendall(str.encode(data))

        except socket.error as e:
            return str(e)
        
    def receive(self):
        # Receive data from the server
        # Receive and decode data from the server
        try:
            data = self.client.recv(2048).decode("utf-8")
            return data
        except socket.error as e:
            return str(e)