import socket
import random

isconnect = False

while True:
    line = input('ftp> ').strip()
    args = line.split()
    command = args[0]

    if command == 'open':
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server = args[1]
        except:
            server = input("To ")
        print(f"Connected to {server}")
        clientSocket.connect((f"{server}", 21))
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        print("202 UTF8 mode is always enabled. No need to send this command")

        user = input(f"User ({server}:(none)): ")
        clientSocket.send(f"USER {user}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

        password = input("Password:")
        clientSocket.send(f"PASS {password}\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")
        isconnect = True

    if (isconnect == False and command in ['ascii','binary','cd','close','delete','disconnect','get','ls','open','put','pwd','rename','user']):
        print("Not connected.")

    elif (command == 'quit' or command == 'bye'):
        try:
            clientSocket.send("QUIT\r\n".encode())
            resp = clientSocket.recv(1024)
            print(resp.decode(), end = "")
            clientSocket.close()
            isconnect = False
            break
        except:
            break

    elif (command == 'disconnect' or command == 'close'):
        clientSocket.send("QUIT\r\n".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")
        clientSocket.close()  
        isconnect = False  

    elif command == "user":
        if not args[1]:
            user = input("Username: ")
            if not user:
                print("Usage: user username [password] [account]")
                break
        # print("hasbeen here :)",clientSocket)
        clientSocket.send(f"USER {args[1]}".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")


        if not args[2]:
            password = input("Password: ")
        
        clientSocket.send(f"PASS {args[2]}".encode())
        resp = clientSocket.recv(1024)
        print(resp.decode(), end = "")

    
    else:
        print("Invalid command.")