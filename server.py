import socket
import sqlite3
import hashlib
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))

server.listen()


def handle_connection(c):
    c.send("Username: ".encode())
    username = c.recv(1024).decode()
    c.send("Password: ".encode())
    password = c.recv(1024)
    password = hashlib.sha256(password).hexdigest()
    
    conn = sqlite3.connect("userdata.db")
    curr = conn.cursor()
    
    curr.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

    if curr.fetchall():
        c.send("Login successful!".encode())
    else:
        c.send("Login failed!".encode())


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args= (client,)).start()