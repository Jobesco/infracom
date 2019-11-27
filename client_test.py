import socket
import sys

def send_ack():
    try:
        s.send('ACK'.decode())
        print('sent ack!')
    except InterruptedError:
        print('error',InterruptedError)
        # sys.quit()

def get_ack():
    try:
        resp = s.recv(1024).decode()
        if resp == 'ACK':
            print('got ack!')
            return True
        else: 
            print('not ack\'ed!')
            return False
    except InterruptedError:
        print('error',InterruptedError)
        # sys.quit()

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

    #sending register intent until ack'ed
    print('sending register intent')
    s.send('register'.encode())
    while not get_ack: s.send('register'.encode())

    #reads protocol confirmation and ack's
    if s.recv(1024).decode() == 'Protocol CH0B confirmed, register server intent':
        send_ack()

        #sends name until ack'ed
        s.send('tester'.encode())
        while not get_ack(): s.send('tester'.encode())

    else: raise Exception('Protocol error!')


elif resp == '2':

    #sending client intent until ack'ed
    print('sent client intent')
    s.send('client'.encode())
    while not get_ack: s.send('client'.encode())

    #reads protocol confirmation and ack's
    if s.recv(1024).decode() == 'Protocol CH0B confirmed, client intent':
        send_ack()

        #sends name until ack'ed
        s.send('tester'.encode())
        while not get_ack(): s.send('tester'.encode())

        resp = s.recv(1024).decode()
        print(resp)
        send_ack()
    else:
        print('AAAAAAA') 
        raise Exception('Protocol error!')
else: pass
# receive data from the server 
print(s.recv(1024).decode())
# close the connection

s.close()