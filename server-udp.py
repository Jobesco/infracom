'''
Nesta parte, devera ser implementado um servidor que, ao ser inicializado, envie ao servidor
DNS local seu nome e endereco IP. Em seguida, este servidor deve esperar por solicitacoes de
clientes na rede e ao receber, enviar o arquivo solicitado, ou informar a inexistencia do
mesmo. O cliente tambem podera requisitar os arquivos disponıveis no repositorio ou encerrar
a conexao.


1 - envia nome e endereço IP ao DNS local

2 - espera solicitacoes de clientes
3 - envia ou informa sobre o arquivo pedido. lista arquivos disponiveis ou encerra conexão

A comunicacao entre o cliente e o servidor devera ser implementada inicialmente utilizando o
protocolo TCP na camada de transporte, assegurando a confiabilidade dos dados. Em
seguida, devera ser implementada utilizando UDP, associando-o a um gerador de perdas
criado pela equipe para que seja possível tornar o protocolo mais “confiável”.
'''
import os.path
from socket import *


def conecta():
    pass


serverPort = 4242
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(((''), serverPort))
print ("O Servidor esta pronto para receber")

#TODO UDP aqui
try:
    serverSocket.connect(('127.0.0.1', serverPort))
    print('connected to', AF_INET) 
except socket.timeout:
    print('socket timeout')
serverSocket.send('register'.encode())
if serverSocket.recv(1024).decode() == 'Protocol CH0B confirmed, register server intent':
    serverSocket.send('tester'.encode())
else: raise Exception('Protocol error!')
serverSocket.close()


while True:

    #espera receber cliente
    #message, clientAddress = serverSocket.recvfrom(2048)  

    #Recebe 0 ou 1, e a solicitacao
    
    # modifiedMessage = message.upper()
    # serverSocket.sendto(modifiedMessage, clientAddress)

    bytesAddressPair = UDPServerSocket.recvfrom(2048)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)

    # while message[0] == '0': 

    #     bytesAddressPair = UDPServerSocket.recvfrom(2048)
    #     message = bytesAddressPair[0]
    #     address = bytesAddressPair[1]
    #     clientSocket.sendto('0',(adress,serverPort))

    while message[0] == '1':

        ack = message[0]
        bytesAddressPair = UDPServerSocket.recvfrom(2048)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientSocket.sendto('1',(adress,serverPort))

    #avance no processo de requisição

    if message[2] == '1':
        ack = message[0]
        clientSocket.sendto(ack,(adress,serverPort)) #manda o ack para confirmar que o client pode solicitar o arq desejado
        bytesAddressPair = UDPServerSocket.recvfrom(2048)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        #Abrir arquivo
        #flname = 'C:\\Program Files (x86)\\' + message[3]

        print ('abrindo arquivo')
        if os.path.exists(message[3]):

            arq=open(message[3],'rb')
        
            print ('enviado  arquivo')
            for i in arq:
                #print i
                clientSocket.sendto(i, (address, serverPort))
            
            print ('fechando arquivo')
            arq.close()
        
        else:
            clientSocket.sendto('Arquivo inexistente',(address,serverPort))
        pass

    elif message[2] == '2':
        
        ack = message[0]
        clientSocket.sendto(ack,(adress,serverPort)) #manda o ack para confirmar que vai ser enviado a lista p o client
        bytesAddressPair = UDPServerSocket.recvfrom(2048)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        print ('abrindo arquivo')
        arq1=open(lista.txt,'rb')
        print ('enviado  arquivo')
        for j in arq1:
            #print i
            clientSocket.sendto(j, (address, serverPort))
        
        print ('fechando arquivo')
        arq.close()
        

    elif message[2] == '3':
        
        ack = message[0]
        clientSocket.sendto(ack,(adress,serverPort)) #manda o ack para confirmar que vai ser enviado a lista p o client
        bytesAddressPair = UDPServerSocket.recvfrom(2048)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientSocket.sendto('Conexao encerrada',(address,serverPort))

    print(clientMsg)
    print(clientIP)



   

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)

    
    
    
    
    
    
    
    
    
    
    
    