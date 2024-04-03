import socket
import struct
import sys
import os
from pathlib import Path
from socket_handle import *

import random

client_socket = None
locale_path = os.getcwd()

while (True):
    rand = int(random.random() * 20000 + 1000)
    
    inp = input("ftp> ").strip()
    args = inp.split()
    
    command = args[0]
    if (command == "quit" or command == "bye"):
        if (client_socket):
            client_socket.send("QUIT\r\n".encode("utf-8"))
            res = client_socket.recv(1024)
            print(res.decode())
            client_socket.close()
            break
        print()
        break

    elif (command == "disconnect" or command == "close"):
        if (client_socket):
            client_socket.send("QUIT\r\n".encode("utf-8"))
            res = client_socket.recv(1024)
            print(res.decode())
            client_socket.close()
        else:
            print("Not connected.")
    
    elif (command == "open") :
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(("test.rebex.net", 21))
            
            client_socket.settimeout(10)
            res = client_socket.recv(1024)
            print(res.decode())
            print("socket details: ",client_socket.getpeername())

        except:
            print(f"Unknown host {args[1]}.")
        
    elif (command == "user"):
        user = "anonymous"
        client_socket.send(f"USER {user}\r\n".encode("utf-8"))
        res = client_socket.recv(1024)
        print(res.decode())

        password = ""
        client_socket.send(f"PASS {password}\r\n".encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())
    
    elif (command == "lcd"):
        if (len(args) <= 1):
            locale_path = os.getcwd()
            print("Local directory now ", locale_path)

        elif (len(args) == 2):
            if (os.path.isabs(args[1])):
                locale_path = args[1]
                print("Local directory now ", locale_path)
            elif (os. path. isdir(args[1])):
                locale_path = os.path.join(locale_path, args[1])
                print("Local directory now ", locale_path)
            elif (os. path. isfile(args[1])):
                print(f"{args[1][0]}:Invalid argument")
            else:
                print(f"{args[1]}: File not found")

        else:
            print("lcd local directory.")
    
    elif (command == "ls"):
        if (not client_socket):
            print("Not connected.")
        else:
            port = curse_convert(hex(rand)[2::])
            ip_comma = ("192.168.1.174." + port).replace(".",",")
            print(ip_comma)
            
            client_socket.send((f"PORT {ip_comma}\r\n").encode("utf-8"))
            data = client_socket.recv(1024)
            print(data.decode())
            
            if (data.startswith(b"200")):
                try:
                    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    data_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    data_socket.bind(("192.168.1.174", rand))
                    data_socket.listen(1)
                    conn, addr = data_socket.accept()
                    
                    client_socket.send("NLST\r\n".encode("utf-8"))
                    data = client_socket.recv(1024)
                    print(data.decode())
                    
                    while True:
                        data_received = conn.recv(1024)
                        print("data_received ", data_received)
                        
                        if not data_received:
                            print("not data_received")
                            break
                        
                        print("Data received on data socket:", data_received.decode())

                finally:
                    conn.close()
                    data_socket.close()
                
                data = client_socket.recv(1024)
                print(data.decode())
                
        
    elif (command == "nlst"):
        client_socket.send("NLST\r\n".encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())
        print("Files on server:")
        
    elif (command == "ascii"):
        client_socket.send("TYPE A\r\n".encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())
        
    elif (command == "binary"):
        client_socket.send("TYPE I\r\n".encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())
        
    elif (command == "cd"):
        client_socket.send(f"CWD {args[1]}\r\n".encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())
        
    elif (command == "pwd"):
        client_socket.send("XPWD\r\n".encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())

    elif (command == "get"):
        ip_comma = "192.168.1.174.8.227".replace(".",",")
            
        client_socket.send((f"PORT {ip_comma}\r\n").encode("utf-8"))
        data = client_socket.recv(1024)
        print(data.decode())

        if data.startswith(b"200"):

            data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            data_socket.bind(("192.168.1.174", 2275))
            data_socket.listen(10)
            conn, addr = data_socket.accept()
            
            client_socket.send("RETR readme.txt\r\n".encode("utf-8"))
            data = client_socket.recv(1024)
            print(data.decode())

            while True:
                data_received = conn.recv(1024)
                if not data_received:
                    print("not data_received")
                    break
                print("Data received on data socket:", data_received.decode())
                
                with open("test_read_me.txt", 'wb') as file:
                        file.write(data_received)

                print("File downloaded successfully.")
                
            conn.close()
            data_socket.close()
            
            data = client_socket.recv(1024)
            print(data.decode())

        else:
            print(data.decode())