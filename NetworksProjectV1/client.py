import socket
import sys

SERVER_IP = "127.0.0.1"
PORT = 18983

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        print(s.recv(1024).decode())

        while True:
            #read the user command
            command = input(">>> ").strip()
            if not command:
                continue #skip empty inputs

            #send command to server
            s.sendall(command.encode())

            #get server response
            data = s.recv(1024).decode()
            print(data, end="")

            #if end is sent
            if "Goodbye" in data:
                s.close()
                #sys.exit(0)
                break

if __name__=="__main__":
    main()









"""client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 18983))

client_socket.send("Hello",encode())

data = client_socket.recv(1024).decode()
print("Server says:", data)

client_socket.close() """