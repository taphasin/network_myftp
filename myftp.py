from socket import *
from getpass import *
current_ip_address = ""
buff_size = 2047

connect_status = False
current_ftp_host = ""

data_socket_status = False      




def send_recv_print_cmd(cmd: str):
    client_command_socket.send(cmd.encode())
    response = client_command_socket.recv(buff_size).decode()
    print(response, end='')
    return response




while True:

    user_input = input("ftp> ").strip()
    user_input = user_input.split(" ")

    command = user_input[0]

    if command == "quit":
        if connect_status == True:
            resp = send_recv_print_cmd("QUIT\r\n")
            if resp[0:3] == "221":
                client_command_socket.close()
                connect_status = False
                current_ftp_host = ""
        else:
            pass
        break


    elif command == "ascii":
        send_recv_print_cmd("TYPE A\r\n")
    
    elif command == "binary":
        send_recv_print_cmd("TYPE I\r\n")

    elif command == "bye":
        if connect_status == True:
            resp = send_recv_print_cmd("QUIT\r\n")
            if resp == "221 Closing session.\r\n":
                client_command_socket.close()
                connect_status = False
                current_ftp_host = ""
        else:
            pass
        break
    
    elif command == "cd":
        try:
            input_path = user_input[1]
        except IndexError:              # case user didn't type "path"
            input_path = input("Remote directory ")
        
        send_recv_print_cmd(f"CWD {input_path}\r\n")


    elif command == "close":        #close session and return to FTP
        if connect_status == True:
            resp = send_recv_print_cmd("QUIT\r\n")
            if resp[0:3] == "221":                  # 221 goodbye || 221 closing session
                client_command_socket.close()
                connect_status = False 
                current_ftp_host = ""
        else:
            print("Not connected.")
        

    elif command == "delete":
        remote_file = ""
        try:
            remote_file = user_input[1]
        except IndexError:
            remote_file = input("Remote file ")

        send_recv_print_cmd(f"DELE {remote_file}\r\n")

    elif command == "disconnect":    #close session and return to FTP
        if connect_status == True:
            resp = send_recv_print_cmd("QUIT\r\n")
            if resp == "221 Closing session.\r\n":
                client_command_socket.close()
                connect_status = False
                current_ftp_host = ""
        else:
            print("Not connected.")
        


    elif command == "open":     # open [ip] [port]
        if connect_status == True:
            print(f"Already connected to {current_ftp_host}, use disconnect first.")
            continue
        else:
            #create tcp socket
            client_command_socket = socket(AF_INET, SOCK_STREAM)
            #connect to ftp server port 21
            try:
                server_command_port = int(user_input[2])
            except IndexError:
                server_command_port = 21
            else:
                server_command_port = 21

            try:
                client_command_socket.connect((user_input[1], server_command_port))
                command_socket_info = client_command_socket.getsockname()
                current_ip_address = command_socket_info[0]
            except gaierror:
                print(f"Unknow host {user_input[1]}.")
                continue
            except OSError:
                print("> ftp: connect :Connection refused")
                continue

            connection_response_message = client_command_socket.recv(2047).decode()
            if connection_response_message[0:3] == "220":
                print(f"Connected to {user_input[1]}.")
            print(connection_response_message, end='')
            connect_status = True
            current_ftp_host = user_input[1]

            # if connectiob is established -> OPTS UTF8 ON 
            if connection_response_message[0:3] == "220":
                send_recv_print_cmd("OPTS UTF8 ON\r\n")

            # if connectiob is established -> LOGIN 
            if connection_response_message[0:3] == "220":
                username = input(f"User ({user_input[1]}:(none)): ")
                resp = send_recv_print_cmd(f"USER {username}\r\n")

                if resp[0:3] == "331":     # 331 password required
                    password = getpass()
                    resp = send_recv_print_cmd(f"PASS {password}\r\n")

                    if resp[0:3] == "230":     # LOGIN SUCCESS
                        pass
                    elif resp[0:3] == "530":    # 530 Authentication rejected 
                        print("Login failed.") 

                elif resp[0:3] == "501":    # 501 User name not specified
                    print("Login failed.") 

                    



    elif command == "user":
        if connect_status == True:
            username = ''
            password = ''
            accout = ''
            try:
                username = user_input[1]
            except IndexError:
                username = input("Username ")
                if username == "\n":
                    print("Usage: User username [password] [account]")
                    continue
            user_resp = send_recv_print_cmd(f"USER {username}\r\n")

            if user_resp[0:3] == "331":
                try:
                    password = user_input[2]
                except IndexError:
                    password = getpass()

                pass_resp = send_recv_print_cmd(f"PASS {password}\r\n")
            
            elif user_resp == "501 Disconnect first to re-login.\r\n":
                pass
                


        else:
            print("Not connected.")





    elif command == "ls":

        # if connection is established then give a new port number to ftp server for make data connection
        if connect_status == True:
            client_data_socket = socket(AF_INET, SOCK_STREAM)        # create data socket
            client_data_socket.bind(('', 0))
            client_data_socket.listen(1)


            #make PORT command
            data_socket_info = client_data_socket.getsockname()     # get ([ip], port)
            fragment_current_ip = current_ip_address.split('.')
            client_data_socket_port = int(data_socket_info[1])
            port_command = f"PORT {fragment_current_ip[0]},{fragment_current_ip[1]},{fragment_current_ip[2]},{fragment_current_ip[3]},{client_data_socket_port // 256},{client_data_socket_port % 256}\r\n"
            
            resp = send_recv_print_cmd(port_command)                # send data socket port to server


            if resp[0:3] == "200":     # if after send port and 200 PORT OK
                data_socket_status = True


            if data_socket_status == True:      # if after create data socket
                input_path = ""
                try:
                    input_path = user_input[1]
                except IndexError:
                    input_path = ""

                client_command_socket.send(f"NLST {input_path}\r\n".encode())
                connection_socket, ser_addr = client_data_socket.accept()      # wait 3 way hand shake from server
                cmd_rep = client_command_socket.recv(2047).decode()     # get recv response from ls command
                print(cmd_rep, end='')                                  # print ls command response
                data_income = connection_socket.recv(2047).decode()     # recv data
                data_income_lenght = len(data_income)                   # count data byte
                connection_socket.close()                               # close actual_data_socket
                cmd_rep_2 = client_command_socket.recv(2047).decode()   # recv respone "226 Transfer complete"

                try:                                    # case user type [local file]
                    local_file = user_input[2]
                    f = open(local_file, "w", newline='')
                    f.write(data_income)
                    f.close()
                    
                except IndexError:                       # case user didn't type [local file]
                    print(data_income, end="")                              #print data
                    
                print(cmd_rep_2, end=f'ftp> {data_income_lenght} bytes received in 0.00Seconds 10.00Kbytes/sec.\n') #print statistic



        else:
            print('Not connected.')


    elif command == "get":

        if connect_status == True:
            client_data_socket = socket(AF_INET, SOCK_STREAM)        # create data socket
            client_data_socket.bind(('', 0))
            client_data_socket.listen(1)


            #make PORT command
            data_socket_info = client_data_socket.getsockname()     # get ([ip], port)
            fragment_current_ip = current_ip_address.split('.')
            client_data_socket_port = int(data_socket_info[1])
            port_command = f"PORT {fragment_current_ip[0]},{fragment_current_ip[1]},{fragment_current_ip[2]},{fragment_current_ip[3]},{client_data_socket_port // 256},{client_data_socket_port % 256}\r\n"
            
            resp = send_recv_print_cmd(port_command)                # send data socket port to server




            if resp[0:3] == "200":     # if after send port and 200 PORT OK
                data_socket_status = True


            if data_socket_status == True:      # if after create data socket
                client_command_socket.send(f"RETR {user_input[1]}\r\n".encode())
                connection_socket, ser_addr  = client_data_socket.accept()      # wait 3 way hand shake from server
                cmd_rep = client_command_socket.recv(2047).decode()
                print(cmd_rep, end='')
                if cmd_rep != "550 No such file.\r\n":
                    data_income = connection_socket.recv(2047).decode()
                    data_income_lenght = len(data_income)
                    connection_socket.close()
                    cmd_rep_2 = client_command_socket.recv(2047).decode()
                    print(cmd_rep_2, end=f'ftp> {data_income_lenght} bytes received in 0.00Seconds 10.00Kbytes/sec.\n')

                    try:                                # case user type [local file]
                        filename = user_input[2]
                    except IndexError:
                        filename = user_input[1]        # case user didn't type [local file]
                    f = open(filename, "w", newline='')
                    f.write(data_income)
                    f.close()
                else:
                    connection_socket.close()

        else:
            print('Not connected.')

    elif command == "put":

        try:                                    # get local_file
            local_file = user_input[1]
        except IndexError:
            local_file = input("Local file ")

        try:                                    # check local_file
            f = open(local_file, "r")
            data_export = f.read()
            f.close()
        except OSError:
            print(f"{local_file}: File not found")
            continue


        client_data_socket = socket(AF_INET, SOCK_STREAM)        # create data socket
        client_data_socket.bind(('', 0))
        client_data_socket.listen(10)
        #make PORT command
        data_socket_info = client_data_socket.getsockname()     # get ([ip], port)
        fragment_current_ip = current_ip_address.split('.')
        client_data_socket_port = int(data_socket_info[1])
        port_command = f"PORT {fragment_current_ip[0]},{fragment_current_ip[1]},{fragment_current_ip[2]},{fragment_current_ip[3]},{client_data_socket_port // 256},{client_data_socket_port % 256}\r\n"
        resp = send_recv_print_cmd(port_command)                # send data socket port to server
        if resp[0:3] == "200":     # if after send port and 200 PORT OK
            data_socket_status = True

        try:
            remote_file = user_input[2]
        except IndexError:
            remote_file = user_input[1]
        client_command_socket.send(f"STOR {remote_file}\r\n".encode())          # send command STOR 
        stor_rep = client_command_socket.recv(2047).decode()                     # resp STOR
        print(stor_rep, end='')

        if stor_rep[0:3] == "150":
            
            connection_socket, ser_addr = client_data_socket.accept()      # wait 3 way hand shake from server

            if data_socket_status == True:      # if after create data socket -> send data

                connection_socket.send(data_export.encode())
                data_export_lenght = len(data_export)
                connection_socket.close()

                cmd_rep_2 = client_command_socket.recv(2047).decode()
                print(cmd_rep_2, end=f'ftp> {data_export_lenght} bytes received in 0.00Seconds 10.00Kbytes/sec.\n')


    elif command == "rename":
        try:
            old_name = user_input[1]
        except IndexError:
            old_name = input("From name ")

        try:
            new_name = user_input[2]
        except IndexError:
            new_name = input("To name ")

        RNFR_resp = send_recv_print_cmd(f"RNFR {old_name}\r\n")
        if RNFR_resp[0:3] == "550":
            continue
        else:
            send_recv_print_cmd(f"RNTO {new_name}\r\n")


    elif command == "pwd":
        send_recv_print_cmd("XPWD\r\n")

    else:
        print("Invalid command.")



                



        


            
            
            








