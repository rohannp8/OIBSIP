import socket
import threading
from datetime import datetime
import os

HOST = '127.0.0.1'
PORT = 5000

clients = []
usernames = {}   # conn -> username mapping

USERS_FILE = "users.txt"
HISTORY_FILE = "history.txt"


# -------------- USER ACCOUNT SYSTEM --------------
def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                if ":" in line:
                    user, pwd = line.strip().split(":")
                    users[user] = pwd
    return users


def save_user(username, password):
    with open(USERS_FILE, "a") as f:
        f.write(f"{username}:{password}\n")


def login_or_register(conn):
    users = load_users()

    conn.send("Type 'login' or 'register': ".encode())
    choice = conn.recv(1024).decode().strip()

    # ----- LOGIN -----
    if choice.lower() == "login":
        conn.send("Username: ".encode())
        username = conn.recv(1024).decode().strip()

        conn.send("Password: ".encode())
        password = conn.recv(1024).decode().strip()

        if username in users and users[username] == password:
            conn.send("Login successful!\n".encode())
            return username
        else:
            conn.send("Invalid login. Try again.\n".encode())
            return login_or_register(conn)

    # ----- REGISTRATION -----
    elif choice.lower() == "register":
        conn.send("Choose username: ".encode())
        username = conn.recv(1024).decode().strip()

        if username in users:
            conn.send("Username already exists!\n".encode())
            return login_or_register(conn)

        conn.send("Choose password: ".encode())
        password = conn.recv(1024).decode().strip()

        save_user(username, password)
        conn.send("Registration successful! You can now chat.\n".encode())
        return username

    else:
        conn.send("Invalid choice.\n".encode())
        return login_or_register(conn)


# -------------- MESSAGE HISTORY --------------
def save_history(msg):
    with open(HISTORY_FILE, "a") as f:
        f.write(msg + "\n")


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        lines = f.readlines()

    return lines[-20:]  # last 20 messages


# -------------- BROADCAST SYSTEM --------------
def broadcast(message, sender_conn=None):
    save_history(message)  # save every message

    for client in clients:
        client.send(message.encode())


# -------------- CLIENT HANDLER --------------
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # LOGIN / REGISTER
    username = login_or_register(conn)
    usernames[conn] = username

    # send last 20 chat messages
    conn.send("\n----- Recent Chat History -----\n".encode())
    for line in load_history():
        conn.send(line.encode())
    conn.send("--------------------------------\n".encode())

    # notify others
    welcome_msg = f"[SERVER] {username} has joined the chat!"
    broadcast(welcome_msg, conn)

    # chat loop
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break

            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {username}: {msg}"

            broadcast(formatted_message, conn)

        except:
            break

    conn.close()
    clients.remove(conn)
    left_msg = f"[SERVER] {username} has left the chat."
    broadcast(left_msg, conn)
    print(f"[DISCONNECTED] {addr}")


# -------------- START SERVER --------------
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    start_server()

