import socket
import threading

HOST = "127.0.0.1"
Port = 18983

USER_FILE = "users.txt"

# Helpers #

def load_users():
    #read users from txt file into a dict. Return dict{"Tom": "Tom11",...}
    users = {}
    try: 
        with open(USER_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 2:
                    users[parts[0]] = parts[1]
    except FileNotFoundError:
        pass #if fnf, start empty
    return users

def save_users(users):
    #wrtie current user dict to txt file (do I want overwrite?)
    with open(USER_FILE, "w") as f:
        for u, p in users.items():
            f.write(f"{u},{p}\n")

def client_action(conn, addr, users):
    print(f"[CONNECTED] {addr}")
    logged_user = None

    conn.sendall(b"Welcome to the chat server!\n")

    while True:
        try:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split(" ", 2)
            command = parts[0].lower()

            #login part
            if command == "login":
                if len(parts) != 3:
                    conn.sendall(b"Should be form: login <username> <password>\n")
                elif logged_user:
                    conn.sendall(b"Already logged in.\n")
                else:
                    user, pwd = parts[1], parts[2]
                    if user in users and users[user] == pwd:
                        logged_user = user
                        conn.sendall(f"Login successful. Welcom {user}!\n".encode())
                    else:
                        conn.sendall(b"Invalid username or password.\n")

            #new user
            elif command == "newuser":
                if len(parts) != 3:
                    conn.sendall(b"Should be form: newuser <username> <password>\n")
                else:
                    user, pwd = parts[1], parts[2]
                    if user in users:
                        conn.sendall(b"User already exists. \n")
                    else:
                        users[user] = pwd
                        save_users(users)
                        conn.sendall(b"User created!\n")

            #send message
            elif command == "send":
                if not logged_user:
                    conn.sendall(b"You must be logged in first.\n")
                elif len(parts) < 2:
                    conn.sendall(b"Should be form: send <message>\n")
                else:
                    message = parts[1] if len(parts) == 2 else parts[1] + " " + parts[2]
                    conn.sendall(f"[{logged_user}]: {message}\n".encode())
            
            #logout
            elif command == "logout":
                conn.sendall(f"Goodbye, {logged_user}!\n")
                break

            else:
                conn.sendall(b"Unknown command.\n")
        
        except ConnectionResetError:
            break

    conn.close()
    print(f"[DISCONNECTED] {addr}")

def main():

"""#make socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 18983))

server_socket.listen()
print("Server is now listening")

#accept connection
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

data = conn.recv(1024).decode()
print("Client says:", data)

conn.send("Hello from server!".encode())

conn.close()
server_socket.close()"""