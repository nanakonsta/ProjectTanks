import logging
import socket
from _thread import *
import sys
import requests
from databaseHandler import DatabaseHandler
from gameManager import GameManager
import json
import time
from lobbyMode import LobbyMode
import pygame
from gameMode import GameMode

class ServerManager:


    def __init__(self, server_game_runner):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server = '0.0.0.0'
        self.port = 8080
        self.game_manager = GameManager() 
        # diaxeirizetai states kai data tou paixnidio duskolia score paixtes klp
        
        self.server_ip = socket.gethostbyname(self.server)
        self.game_runner = server_game_runner
        self.p1_in_game= False
        self.p2_in_game= False

        self.isInLobby = False
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
        self.s.listen()
        self.database_handler = DatabaseHandler()
        # diaxeirizetai erwthmata sthn vash 
        
    def get_public_ip(self):
        try:
            response = requests.get('https://httpbin.org/ip')
            return response.json()['origin']
        except requests.RequestException as e:
            return None
    
    def threaded_client(self, conn):
        # this is where we get the input from the players
          
        try:
            while True:
                data = conn.recv(2048)
                if not data:
                    conn.send(str.encode("Goodbye"))
                else:
                    data_decoded = data.decode('utf-8')
                    json_data = json.loads(data_decoded)
                    data_to_sent = self.receiveDataAndTakeAction(json_data)
                    conn.sendall(str.encode(data_to_sent))
        except Exception as e:
            logging.error(f"Error in threaded_client: {e}")
        finally:
            print("Connection Closed")
            conn.close()
        
        
    def receiveDataAndTakeAction(self, json_data):
        data_type = list(json_data.keys())[0]
        
        match data_type:
            case "player1":
                if self.game_runner.game_mode_initiated == False:
                    self.initiateGame()
                return self.setPlayersDataAndSentGameData(json_data, "p1")  
            case "player2":
                if self.game_runner.game_mode_initiated == False:
                    self.initiateGame()
                return self.setPlayersDataAndSentGameData(json_data, "p2")           
            case "cred_sign_in":
                return self.signIn(json_data)
            case "cred_sign_up":
                return self.signUp(json_data)
            case "fetch_lobby_data|p1":
                self.isInLobby = True
                if self.game_runner.lobby_mode_initiated == False:                    
                    self.initiateLobby()                    
                return self.get_instruction_and_send_lobbyData(json_data,"p1")            
            case "fetch_lobby_data|p2":
                self.isInLobby = True
                if self.game_runner.lobby_mode_initiated == False:                    
                    self.initiateLobby()                    
                return self.get_instruction_and_send_lobbyData(json_data,"p2")
            case "connected":
                pass
            
        json_data_empty = { "status": "wait"}
        
        return json.dumps(json_data_empty)
                
    def initiateLobby(self):
        self.game_runner.lobby_mode_initiated = True
        self.game_runner.mode = LobbyMode(self.game_runner.screen, self.game_manager, self.game_runner)
    
    def initiateGame(self):
        if self.game_runner.mode.lobby.bothPlayersLocked() == True:
            self.game_runner.game_mode_initiated = True
            self.game_runner.mode = GameMode(self.game_runner.screen, self.game_manager, self.game_runner)
                 
    def setPlayersDataAndSentGameData(self, json_data, p):
        if p == "p1":
           self.p1_in_game = True
           self.game_runner.mode.dataP1 = json_data

        elif p == "p2":
           self.p2_in_game = True
           self.game_runner.mode.dataP2 = json_data
           
        return self.game_runner.mode.getJSONgameModeData()
    
    def get_instruction_and_send_lobbyData(self, json_data, p):

        if p == "p1":
           self.game_runner.mode.dataP1 = json_data
        if p == "p2":
           self.game_runner.mode.dataP2 = json_data

        return self.game_runner.mode.lobby.getJSONLobbyData()
                        
    def signIn(self, json_data):
        username = json_data.get("cred_sign_in", {}).get("username")
        password = json_data.get("cred_sign_in", {}).get("password")
        p1OrP2 = ""
        if self.database_handler.authenticateUser(username, password):
            if self.game_manager.player1.username == username or self.game_manager.player2.username == username:
                return "User already signed in"
            
            if self.game_manager.player1.username is None:
                self.game_manager.player1.username = username
                p1OrP2 = "p1"
            else:
                self.game_manager.player2.username = username
                p1OrP2 = "p2"
            
            if p1OrP2 != "":
                return "200 OK|" + p1OrP2
            else:
                return "Max users for this Server"
        else:
            return "Authentication failed"
        
                   
    def signUp(self, json_data):
        username = json_data.get("cred_sign_up", {}).get("username")
        password = json_data.get("cred_sign_up", {}).get("password")
        if self.database_handler.userExists(username):
            return "User already exists"
        if self.database_handler.insertUser(username, password):
            return "200 OK"
        else:
            return "Registration failed"


