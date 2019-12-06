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
#TODO timeout tentando conectar p dns errado
dnsAddress = '192.168.1.16'
dnsPort = 4241

#TODO timeouts!
#seq = seq esperada / msg = msg completa / retorna msg toda
#manda ack se tiver na sequencia certa
def espera_seq(seq,msg,address,wannabe):
    while msg[0] != seq: #manda seq contraria
        serverSocket.sendto((msg[0]+';').encode(),address)

        msg, wannabeAddress = serverSocket.recvfrom(2048)
        msg = msg.decode()
        # ! chamar check client sempre que receber uma msg
        check_client(wannabeAddress,address) #TODO verificar a continuidade do loop caso nao seja o cliente certo
    serverSocket.sendto((seq+';').encode(),address)
    return msg


#se o endereco for diferente, ele diz q ta ocupado
def check_client(wannabe, address):
    if wannabe != address:
        serverSocket.sendto('busy'.encode(),wannabe)
        return False
    return True

def invert_seq(seq):
    return '1' if seq == '0' else '0'

#! ele automaticamente coloca o numero de sequencia e ;
#TODO desistir apos x tentativas
#retorna so a mensagem
def get_ack(seq, msg):
    while True:
        try:
            serverSocket.settimeout(2.5)
            resp, addr = serverSocket.recvfrom(2048)
            resp = resp.decode()
            if addr[0] != clientAddress[0]:
                pass
            elif resp[0] != seq:
                serverSocket.settimeout(None)
                serverSocket.sendto((seq+';'+msg).encode(),clientAddress)
                serverSocket.settimeout(2.5)
            elif resp == 'busy':
                raise TypeError
            else: 
                serverSocket.settimeout(None)                
                return resp.split(';',maxsplit=1)[1]
        except timeout:
            print('timeout! Sending again...')
            serverSocket.settimeout(None)
            serverSocket.sendto((seq+';'+msg).encode(),clientAddress)
            serverSocket.settimeout(2.5)
        except TypeError:
            r = input('O cliente esta ocupado?\nPressione 1 para continuar ou 2 para sair\n')
            if r == '2':
                exit(0)
        except ConnectionResetError:
            print('o cliente caiu!')
            exit(1)

serverPort = 4242
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("O Servidor esta pronto para receber")

#envia ao server DNS o nome do server
serverName = input('Qual o nome do server?\n')
serverSocket.sendto(('register ' + serverName).encode(),(dnsAddress,dnsPort))
print('enviado!')
clientAddress = 0

while True:

    #espera receber cliente
    #message, clientAddress = serverSocket.recvfrom(2048)  

    #Recebe 0 ou 1, e a solicitacao
    
    # modifiedMessage = message.upper()
    # serverSocket.sendto(modifiedMessage, clientAddress)
    #TODO automatizar por aqui o numero de sequencia
    print('esperando receber mensagem...')
    message, address = serverSocket.recvfrom(2048)
    message = message.decode()
    clientAddress = address

    #seq = seq esperada / mensagem = msg completa / retorna msg toda
    #garante que recebeu na sequencia certa e envia ack
    message = espera_seq('0',message, address ,address)

    #no caso, message é a mensagem só, sem o numero de seq e ;
    if message[2] == '1':
        
        #espera receber nome do arquivo     
        message, wannabeAddress = serverSocket.recvfrom(2048)
        message = message.decode()

        message = espera_seq('1',message, address,wannabeAddress)

        #! Abrir arquivo - EXPERIMENTAL
        #flname = 'C:\\Program Files (x86)\\' + message[3]

        print ('abrindo arquivo')
        try:
            arq=open('files/'+message[2:],'rb')
            seq = '0'

            while True:  
                datagram = arq.read(2048).decode()
                if datagram == '':
                    print('o arquivo está vazio')
                    serverSocket.sendto((seq+';').encode(),address)
                    get_ack(seq,datagram)
                    seq = invert_seq(seq)
                    break
                else:
                    print('enviando todo o arquivo')
                    #TODO ver veracidade do endereço
                    serverSocket.sendto((seq+';'+datagram).encode(),address)
                    get_ack(seq,datagram)
                    seq = invert_seq(seq)
                    
                    #! deprecated, da pra enviar tudo de uma vez
                    # for i in datagram:
                    #     print(i)
                    #     serverSocket.sendto(i.encode(), (address, serverPort))
                    
            print ('fechando arquivo')
            arq.close()
        except FileNotFoundError:
            print('Arquivo não existe!')
            serverSocket.sendto('0;Arquivo inexistente'.encode(),address)
            get_ack('0','Arquivo inexistente')
        

    elif message[2] == '2':
        #TODO receber do cliente certo
        clientIP = address[0]
        #criando arquivo com os nomes dos caminhos que temos disponiveis
        arquivos = os.listdir('./files/')
        print(arquivos)

        #! ABSTRAÇÃO: nome do arquivo nao é maior q 2048 caracteres
        seq = '1'
        for nome in arquivos:
            #envia
            #recebe ack
            #troca sequencia
            serverSocket.sendto((seq+';'+nome).encode(),address)
            get_ack(seq,nome)
            seq = invert_seq(seq)
            
        serverSocket.sendto((seq+';').encode(),address)
        get_ack(seq,'')
        #acabou num precisa dar tchau UDP é assim

        #? ALGORITMO:
        #envia cada entrada da lista
        #quando acabar, envia string vazia
        

    elif message[2] == '3':

        bytesAddressPair = UDPServerSocket.recvfrom(2048)
        message = bytesAddressPair[0].decode()
        address = bytesAddressPair[1]
        serverSocket.sendto('Conexao encerrada'.encode(),(address,serverPort))



    
    
    
    
    
    # Lê usando .read(numero de bytes) enquanto o resultado lido for diferente de vazio ou tiver a qtd de bytes esperada
    # if 
    # f = open('workfile', 'rb+')  
    
    
    '''
    
            print ('abrindo arquivo')
        if os.path.exists(message[3]):

            arq=open(message[3],'rb+')
        
            print ('enviado  arquivo')
            
            if f.read(2048) == '':
                print ('o arquivo esta vazio') 
            elif f.read(2048) != '' and  len(f.read(2048)) <= 2048:
                print('enviando todo arquivo')
                for i in arq:
                #print i
                serverSocket.sendto(i.encode(), (address, serverPort))   
            pass      
            elif f.read(2048) != '' and  len(f.read(2048)) > 2048:
                for j >= 2048 in arq:
                    serverSocket.sendto(i.encond(), (address, serverPort)
            pass
            
            
            
                      
            print ('fechando arquivo')
            arq.close()
        '''