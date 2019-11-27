import socket
import sys

# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 4242                
  
# connect to the server on local computer 
try:
    s.connect(('127.0.0.1', port))
    print('connected to', socket.AF_INET) 
except socket.timeout:
    print('socket timeout')

resp = input('registrar - 1\npegar ip - 2')
if resp == '1':
    print('qaa')
    s.send('register'.encode())
    if s.recv(1024).decode() == 'Protocol CH0B confirmed, register server intent':
        s.send('tester'.encode())
    else: raise Exception('Protocol error!')
elif resp == '2':
    s.send('client'.encode())
    print('sent client intent')
    if s.recv(1024).decode() == 'Protocol CH0B confirmed, client intent':
        print('protocol confirmed')
        s.send('tester'.encode())
        resp = s.recv(1024).decode()
        print(resp)
    else:
        print('AAAAAAA') 
        raise Exception('Protocol error!')
else: pass
# receive data from the server 
print(s.recv(1024).decode())
# close the connection

s.close()