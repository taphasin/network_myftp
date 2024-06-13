#  myftp | ftp command terminal

myftp is a python script to emulate the ftp command in the terminal with a socket library. This script can send, receive, and output like a terminal.

### Tool
- vscode
- filezilla (server)
- wireshark (packet capture)

### example output
```
python .\tamyftp.py
ftp> open 127.0.0.1
Connected to 127.0.0.1
220-FileZilla Server 1.8.1
220 Please visit https://filezilla-project.org/
202 UTF8 mode is always enabled. No need to send this command
User (127.0.0.1:(none)): bob
331 Please, specify the password.
Password:
230 Login successful.
ftp> cd inred
250 CWD command successful
ftp> cd ..
250 CWD command successful
ftp> get 44
200 PORT command successful.
150 Starting data transfer.
226 Operation successful
```
### this script can run following ftp command
```
ascii             Set the file transfer type to ASCII, the default.
binary            Set the file transfer type to binary.
bye               End the FTP session and exit ftp
cd                Change the working directory on the remote host.
close             End the FTP session and return to the cmd prompt.
delete            Delete file on remote host.
disconnect        Disconnect from the remote host, retaining the ftp prompt.
get               Copy a remote file to the local PC.
ls                List a remote directory’s files and subdirectories.
open              Connects to the specified FTP server.
put               Copy a local file to the remote host.
pwd               Print Working Directory
quit              End the FTP session with the remote host and exit ftp.
rename            Rename remote files.
user              Specifes a user to the remote host.
