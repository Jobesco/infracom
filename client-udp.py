# coding: UTF-8

from socket import *
serverPort = 4242
dnsPort = 4241

clientSocket = socket(AF_INET, SOCK_DGRAM)
# clientSocket.bind(('',serverPort))

#! ele automaticamente coloca o numero de sequencia e ;
#TODO desistir apos x tentativas
#retorna so a mensagem
def get_ack(seq, msg):
    while True:
        try:
            clientSocket.settimeout(2.5)
            resp, addr = clientSocket.recvfrom(2048)
            resp = resp.decode()
            print('get ack',resp)
            if addr[0] != serverIP:
                pass
            elif resp[0] != seq:
                print('seq errada',resp)
                clientSocket.settimeout(None)
                print('enviando',(seq+';'+msg))
                clientSocket.sendto((seq+';'+msg).encode(),(serverIP,serverPort))
                clientSocket.settimeout(2.5)
            elif resp == 'busy':
                raise TypeError
            else: 
                clientSocket.settimeout(None)
                print('certo',resp)                
                return resp.split(';',maxsplit=1)[1]
        except timeout:
            print('timeout! Sending again...')
            clientSocket.settimeout(None)
            clientSocket.sendto((seq+';'+msg).encode(),(serverIP,serverPort))
            clientSocket.settimeout(2.5)
        except TypeError:
            r = input('O servidor esta ocupado!\nPressione 1 para continuar ou 2 para sair\n')
            if r == '2':
                exit(0)
        except ConnectionResetError:
            print('o servidor caiu!')
            exit(1)

#TODO timeouts!
#seq = seq esperada / msg = msg completa / retorna msg toda
#manda ack se tiver na sequencia certa
def espera_seq(seq,msg,address,wannabe):
    while msg[0] != seq: #manda seq contraria
        print('espera seq recebeu msg errada',msg)
        clientSocket.sendto((msg[0]+';').encode(),(address,serverPort))

        msg, wannabeAddress = clientSocket.recvfrom(2048)
        msg = msg.decode()
        # ! chamar check client sempre que receber uma msg
        check_client(wannabeAddress,address) #TODO verificar a continuidade do loop caso nao seja o cliente certo
    clientSocket.sendto((seq+';').encode(),(address,serverPort))
    return msg


#se o endereco for diferente, ele diz q ta ocupado
def check_server(wannabe, address):
    if wannabe != address:
        return False
    return True

def recebe_arquivo(msg,arq):
    seq = '1'
    full = False
    fraction = ''
    while not full: #TODO check if full
        fraction += get_ack(seq,msg)
        seq = invert_seq(seq)
    arq.write(fraction)
    arq.close()

def invert_seq(seq):
    return '1' if seq == '0' else '0'

serverIP = 0
dnsAddress = '192.168.1.16'
#solicita nome do servidor
while True:
    serverName = input('Para qual servidor voce quer se conectar?\n')
    serverName = 'client ' + serverName
    
    clientSocket.sendto(serverName.encode(),(dnsAddress,dnsPort))

    serverIP, _ = clientSocket.recvfrom(2048)
    serverIP = serverIP.decode()

    while serverIP == 'no-ip':
        serverName = input('O nome não existe no servidor DNS!\n' \
            'Por favor, insira um nome válido!\n')
        serverName = 'client ' + serverName

        clientSocket.sendto(serverName.encode(),(dnsAddress,dnsPort))
        serverIP, _ = clientSocket.recvfrom(2048)
        serverIP = serverIP.decode()

    prompt = 'Bem vindo!\n' \
        'Por favor, escolha uma das opcoes abaixo:\n' \
        '1 - Solicitar Arquivo\n2 - Listar Arquivos\n3 - Sair\n'
    resposta = input(prompt)
    #comeco de protocolo UDP
    if resposta[0] == '1':
        print('test')
        clientSocket.sendto('0;1'.encode(),(serverIP,serverPort))

        #get_ack recebe a msg tb
        get_ack('0', '1')


        resposta = input('Qual o nome do Arquivo?')
        arq = open(resposta,'wb')
        resposta = '1;' + resposta
        clientSocket.sendto(resposta.encode(), (serverIP,serverPort))

        get_ack('1', resposta.encode())

        recebe_arquivo(resposta,arq)

    elif resposta[0] == '2':
        clientSocket.sendto('0;2'.encode(),(serverIP,serverPort))

        get_ack('0', '2')
        # print(clientSocket.getblocking())
        #informa que está pronto pra passar a receber
        # clientSocket.sendto('invert'.encode(),(serverIP,serverPort))
        
        seq = '1'
        print('Segue a lista de arquivos existentes:')
        #nesse momento o cliente se torna receptor
        message, wannabeAddress = clientSocket.recvfrom(2048)
        message = message.decode()

        message = espera_seq(seq,message, serverIP,wannabeAddress)
        message = message.split(';',maxsplit=1)[1]
        seq = invert_seq(seq)
        print(message)
        while message != '':
            message, wannabeAddress = clientSocket.recvfrom(2048)
            message = message.decode()

            message = espera_seq(seq,message, serverIP,wannabeAddress)
            message = message.split(';',maxsplit=1)[1]
            seq = invert_seq(seq)
            print(message)

    elif resposta[0] == '3':
        print('Ate logo!')
        break
    # 0;opcao ou nome

