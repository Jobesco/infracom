# coding: UTF-8

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
import os
from socket import *

dnsAddress = '172.22.71.12'
dnsPort = 4241

#TODO timeouts!
#seq = seq esperada / msg = msg completa / retorna msg toda
#manda ack se tiver na sequencia certa
def espera_seq(seq,msg,address):
    while msg[0] != seq: #manda seq contraria 
        serverSocket.sendto((msg[0]+';').encode(),(address,serverPort))

        msg, wannabeAddress = serverSocket.recvfrom(2048)
        msg = msg.decode()
        # ! chamar check client sempre que receber uma msg
        check_client(wannabeAddress,address) #TODO verificar a continuidade do loop caso nao seja o cliente certo
    serverSocket.sendto((seq+';').encode(),(address,serverPort))
    return msg


#se o endereco for diferente, ele diz q ta ocupado
def check_client(wannabe, address):
    if wannabe != address:
        serverSocket.sendto('busy'.encode(),wannabe)
        return False
    return True


serverPort = 4242
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("O Servidor esta pronto para receber")

#envia ao server DNS o nome do server
serverName = input('Qual o nome do server?\n')
serverSocket.sendto(('register ' + serverName).encode(),(dnsAddress,dnsPort))
print('enviado!')

while True:

    #espera receber cliente
    #message, clientAddress = serverSocket.recvfrom(2048)  

    #Recebe 0 ou 1, e a solicitacao
    
    # modifiedMessage = message.upper()
    # serverSocket.sendto(modifiedMessage, clientAddress)
    #TODO automatizar por aqui o numero de sequencia
    message, address = serverSocket.recvfrom(2048)
    message = message.decode()

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)

    #seq = seq esperada / mensagem = msg completa / retorna msg toda
    #garante que recebeu na sequencia certa e envia ack
    message = espera_seq('0',message, address[0])

    #avance no processo de requisição
    #no caso, message é a mensagem só, sem o numero de seq e ;
    if message[2] == '1':

        #espera receber nome do arquivo     
        message, address = serverSocket.recvfrom(2048)
        message = message.decode()

        message = espera_seq('1',message, address[0])

        #! Abrir arquivo - EXPERIMENTAL
        #flname = 'C:\\Program Files (x86)\\' + message[3]

        print ('abrindo arquivo')
        if os.path.exists(message[3]):

            arq=open(message[3],'rb')
        
            print ('enviado  arquivo')
            for i in arq:
                #print i
                clientSocket.sendto(i.encode(), (address, serverPort))
            
            print ('fechando arquivo')
            arq.close()
        
        else:
            clientSocket.sendto('Arquivo inexistente'.encode(),(address,serverPort))
        pass

    elif message[2] == '2':

        #criando arquivo com os nomes dos caminhos que temos disponiveis
        arquivos = os.listdir('./files/')
        print(arquivos)

        #! ABSTRAÇÃO: nome do arquivo nao é maior q 2048 caracteres

        
        

    elif message[2] == '3':

        bytesAddressPair = UDPServerSocket.recvfrom(2048)
        message = bytesAddressPair[0].decode()
        address = bytesAddressPair[1]
        clientSocket.sendto('Conexao encerrada'.encode(),(address,serverPort))

    print(clientMsg)
    print(clientIP)


    
    
    
    
    
    
    
    
    
    
    
    