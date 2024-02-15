import sqlite3
import threading

class DatabaseHandler:
    def __init__(self):
        # Use thread-local storage for SQLite connections
        self.local = threading.local()

    def get_connection(self):
        # Create a new connection for each thread if it doesn't exist
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect('gamedatabase.db')
            self.create_table()
        return self.local.conn

    def create_table(self):
        #table twn players sth vash dedomenwn
        # Create 'players' table if not exists
        cursor = self.get_connection().cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.get_connection().commit()

    def userExists(self, username): #checks if the user is logged in
        cursor = self.get_connection().cursor()
        query = "SELECT * FROM players WHERE username = ?"
        parameters = (username,)
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        return len(result) > 0

    def authenticateUser(self, username, password): #sign in
        cursor = self.get_connection().cursor()
        query = "SELECT * FROM players WHERE username = ? AND password = ?"
        parameters = (username, password)
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        return result

    def insertUser(self, username, password): #register
        cursor = self.get_connection().cursor()
        query = "INSERT INTO players (username, password) VALUES (?, ?)"
        parameters = (username, password)
        cursor.execute(query, parameters)
        self.get_connection().commit()
        # if the user is created then this will return true
        return self.userExists(username)