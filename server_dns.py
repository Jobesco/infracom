'''
são 3 modulos distintos que devem interagir entre si através da rede,
- módulo servidor
- módulo cliente 
- módulo DNS simplificado

A comunicaçao entre o cliente e o servidor deverá ser implementada inicialmente utilizando o
protocolo TCP na camada de transporte. 

Em seguida, deverá ser implementada utilizando UDP, associando-o a um gerador de perdas
criado pela equipe para que seja possível tornar o protocolo mais “confiável”.

A comunicação entre cliente e DNS deverá ser implementada sempre utilizando UDP.
'''

import socket
import sys


print('Creating socket...',end='')
try: 
    s = socket.socket() 
    print ("Socket successfully created")
except socket.error as err: 
    print ("Socket creation failed with error %s" %(err))
#AF_INET refers to the address family ipv4. The SOCK_STREAM means connection oriented TCP protocol.

# default port for socket 
port = 4242

try:
    s.bind(('',port))
    print('Socket binded to %s' %(port))
    #After that we binded our server to the specified port.
    #Passing an empty string means that the server can listen to incoming connections from other computers as well.
    #If we would have passed 127.0.0.1 then it would have listened to only those calls made within the local computer.
except:
    print('Cant bind to port')
    sys.exit()

s.listen(5)
print('Socket is listening')
#5 here means that 5 connections are kept waiting if the server is busy and if a 6th socket trys to connect then the connection is refused


# first message to read, checks if it is a server wanting to register
# or a client wanting to get an IP
def get_intent():
    try:
        return c.recv(1024).decode()
    except InterruptedError:
        print('error',InterruptedError)
        # sys.quit()

def send_ack():
    try:
        c.send('ACK'.decode())
        print('sent ack!')
    except InterruptedError:
        print('error',InterruptedError)
        # sys.quit()

def get_ack():
    try:
        resp = c.recv(1024).decode()
        if resp == 'ACK':
            print('got ack!')
            return True
        else: 
            print('not ack\'ed!')            
            return False
    except InterruptedError:
        print('error',InterruptedError)
        # sys.quit()
#basic list of servers
server_list = {}


#TODO add timeouts??
#TODO add ACKs?
#TODO support for simultaneous connections
# ! MAIN RUN
while True: 

    # Establish connection with client. 
    c, addr = s.accept()      
    print ('Got connection from', addr)

    # gets intent
    intent = get_intent()
    send_ack()

    if intent == 'register':
        print('register intent, sending confirmation')

        # send protocol confirmation until ack'ed
        c.send('Protocol CH0B confirmed, register server intent'.encode())
        while not get_ack(): c.send('Protocol CH0B confirmed, register server intent'.encode())
        
        print('expecting response...')
        # reads server name to add to the list, sends ack afterwards
        name = c.recv(1024).decode()
        send_ack()

        #updates with name and IP(DOES NOT INCLUDES PORT)
        server_list.update({name: addr[0]})

        print('added', addr[0], 'from name', name, 'to list of servers')
        print(server_list)


    elif intent == 'client':
        print('client intent, sending confirmation')
        
        
        # send protocol confirmation until ack'ed
        c.send('Protocol CH0B confirmed, client intent'.encode())
        while not get_ack(): c.send('Protocol CH0B confirmed, client intent'.encode())

        print('expecting response...')
        # reads server name to fetch from list, send ack afterwards
        name = c.recv(1024).decode()
        send_ack()

        print('got',name)
        if name in server_list:
            #send until ack'ed
            c.send(server_list[name].encode())
            while not get_ack: c.send(server_list[name].encode())
        else: 
            #workaround for a no match case
            c.send('no-ip'.encode())
            while not get_ack: c.send('no-ip'.encode())
    else: pass #communication error
    
   #Se for servidor de aplicaçao, registra nome e IP
   #se for cliente, recebe nome de servidor, retornando o endereço IP do mesmo
   #como ele vai saber se é servidor ou cliente? por meio da mensagem, pois
   #os dados que ele recebe são apenas uma string em bytes :c

   #protocolo CH0B:
   #server aceita conexao
   #cliente envia informaçao de quem é
   #servidor recebe
   #cliente envia informacao mesmo
   #servidor filtra e responde de acordo
   #vao simbora

    # ? send a thank you message to the client. must be encoded
    c.send('Vai simbora'.encode()) 

    # Close the connection with the client 
    c.close() 


''' MÓDULO DNS
Nesta parte, devera ser implementado um servidor DNS local simplificado, que recebera do
cliente o nome de um servidor da aplicação, e retornará ao mesmo o endereço IP deste
servidor (correspondente a um  . Não é necessário implementar a sintaxe do
protocolo DNS. O servidor da aplicação ao ser inicializado deverá registrar o seu nome e o
correspondente endereço IP neste servidor DNS.
'''