# coding: UTF-8
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


print('Creating socket...')
try: 
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
    print ("Socket successfully created")
    print('ip is',socket.gethostbyname(socket.gethostname()))
except socket.error as err: 
    print ("Socket creation failed with error %s" %(err))
#AF_INET refers to the address family ipv4. The SOCK_STREAM means connection oriented TCP protocol.

# default port for socket 
port = 4241

try:
    s.bind(('',port))
    print('Socket binded to %s' %(port))
    #After that we binded our server to the specified port.
    #Passing an empty string means that the server can listen to incoming connections from other computers as well.
    #If we would have passed 127.0.0.1 then it would have listened to only those calls made within the local computer.
except:
    print('Cant bind to port')
    sys.exit()

#basic list of servers
server_list = {}


#TODO add timeouts??
#TODO add ACKs?
# ! MAIN RUN
while True: 

    # Establish connection with client.
    print('Awaiting message')
    intent, clientAddress = s.recvfrom(2048)
    intent = intent.decode()
    print ('Got message from', clientAddress)
    # intent = intent.decode()
    print('message is',intent)
    if intent[0:8] == 'register':
        print('register intent')
        # print(type(intent.split(maxsplit=1)[1]))
        intent = intent.split(maxsplit=1)[1]

        #updates with name and IP(DOES NOT INCLUDES PORT)
        server_list.update({intent: clientAddress[0]})

        print('added', clientAddress[0], 'from name', intent, 'to list of servers')
        print(server_list)


    elif intent[0:6] == 'client':
        print('client intent')

        intent = intent.split(maxsplit=1)[1]

        print('got',intent)
        if intent in server_list:
            print('found!')
            s.sendto(server_list[intent].encode(),clientAddress)
        else: 
            #workaround for a no match case
            print('no match')
            s.sendto('no-ip'.encode(),clientAddress)
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


''' MÓDULO DNS
Nesta parte, devera ser implementado um servidor DNS local simplificado, que recebera do
cliente o nome de um servidor da aplicação, e retornará ao mesmo o endereço IP deste
servidor (correspondente a um  . Não é necessário implementar a sintaxe do
protocolo DNS. O servidor da aplicação ao ser inicializado deverá registrar o seu nome e o
correspondente endereço IP neste servidor DNS.
'''