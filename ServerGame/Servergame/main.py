import pygame
import socket
import threading
from _thread import start_new_thread

from serverManager import ServerManager
from serverGameRunner import ServerGameRunner

# Define an event to signal thread termination
exit_event = threading.Event()

def handle_connection(server_manager, conn):
    server_manager.threaded_client(conn)
    
def start_server(server_manager, exit_event):
    while not exit_event.is_set():
        try:
            conn, addr = server_manager.s.accept()
            start_new_thread(handle_connection, (server_manager, conn))
        except socket.error:
            # Handle socket errors as needed
            pass

if __name__ == "__main__":
    serverGameRunnerObj = ServerGameRunner() 
    serverManagerObj = ServerManager(serverGameRunnerObj) # upeuthinos gia na parei kai na dwsei dedomena sto paikth
    print('Server running: ' + serverManagerObj.get_public_ip())
    
    server_thread_obj = threading.Thread(target=start_server, args=(serverManagerObj, exit_event))
    server_thread_obj.start()
    pygame.init()
    serverGameRunnerObj.preRunServerWindow()
              
