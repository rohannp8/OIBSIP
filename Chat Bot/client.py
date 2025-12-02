import socket
import threading
from colorama import init, Fore, Style

init(autoreset=True)

HOST = '127.0.0.1'
PORT = 5000


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()

            if not message:
                continue

            # Print server messages in cyan
            print(Fore.CYAN + message + Style.RESET_ALL)

        except:
            print(Fore.RED + "[ERROR] Connection closed.")
            sock.close()
            break


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    print(Fore.GREEN + "[CONNECTED] Waiting for server...\n")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    # This loop sends user input to the server
    while True:
        msg = input("")
        client.send(msg.encode())


if __name__ == "__main__":
    start_client()
