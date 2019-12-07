# coding: UTF-8
import os
from socket import *

#! ele automaticamente coloca o numero de sequencia e ;
#retorna so a mensagem
def get_ack(seq, msg):
    tentativas = 0
    while True:
        try:
            clientSocket.settimeout(2.5)
            resp, addr = clientSocket.recvfrom(2048)
            resp = resp.decode()
            if addr != (serverIP,serverPort):
                pass
            elif resp[0] != seq:
                # clientSocket.settimeout(None)
                clientSocket.sendto((seq+';'+msg).encode(),(serverIP,serverPort))
                # clientSocket.settimeout(2.5)
            elif resp == 'busy':
                raise TypeError
            else: 
                clientSocket.settimeout(None)             
                return resp.split(';',maxsplit=1)[1]
        except timeout:
            print('timeout! Sending again...')
            tentativas += 1
            # clientSocket.settimeout(None)
            clientSocket.sendto((seq+';'+msg).encode(),(serverIP,serverPort))
            if tentativas == 10:
                r = input('O servidor parece não estar respondendo, pressione 1 para sair, ou qualquer outra tecla para continuar.\n')
                if r == '1': exit(0)
                tentativas = 0
            # clientSocket.settimeout(2.5)
        except TypeError:
            r = input('O servidor esta ocupado!\nPressione 1 para sair, ou qualquer outra tecla para continuar.\n')
            if r == '1':
                exit(0)
        except ConnectionResetError:
            print('o servidor caiu!')
            exit(1)

#TODO checar check_server e timeouts
#seq = seq esperada / msg = msg completa / retorna msg toda
#manda ack se tiver na sequencia certa
#address sempre é serverIP
def espera_seq(seq,msg,address,wannabe):
    if not (msg[0] != seq or not check_server(address,wannabe)):
        clientSocket.sendto((seq+';').encode(),address)
        return msg
    while msg[0] != seq or not check_server(address,wannabe): #manda seq contraria

        #so envia se o endereço ta certo
        if check_server(wannabe,address):
            clientSocket.sendto((msg[0]+';').encode(),(address,serverPort))

        try:
            clientSocket.settimeout(10)
            wannabeMsg = 0
            wannabeMsg , wannabeAddress = clientSocket.recvfrom(2048)
            wannabeMsg = msg.decode()
            clientSocket.settimeout(None)
        except timeout:
            print('Parece que o servidor caiu, tente novamente!')
            exit(0)

        # ! chamar check client sempre que receber uma msg
        if check_server(wannabeAddress,address) and wannabeMsg[0] == seq:
            msg = wannabeMsg
            clientSocket.sendto((seq+';').encode(),(address,serverPort))

    return msg


#se o endereco for diferente, ele ignora
def check_server(wannabe, address):
    if wannabe != address:
        return False
    return True

def invert_seq(seq):
    return '1' if seq == '0' else '0'


serverPort = 4242
dnsPort = 4241
clientSocket = socket(AF_INET, SOCK_DGRAM)
serverIP = 0
dnsAddress = '192.168.15.6'

#solicita nome do servidor
while True:
    serverName = input('Lembre-se de verificar o endereço do DNS!' \
        '\nPara qual servidor voce quer se conectar?\n')
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
        
        clientSocket.sendto('0;1'.encode(),(serverIP,serverPort))

        #numero de sequencia esperado, mensagem a reenviar caso não receba o ack a tempo
        get_ack('0', '1')


        resposta = input('Qual o nome do Arquivo?')
        arq = open('./'+resposta,'wb')
        resposta = '1;' + resposta
        clientSocket.sendto(resposta.encode(), (serverIP,serverPort))

        get_ack('1', resposta[2:].encode())
        seq = '0'

        #cliente se torna receptor no protocolo rdt
        while True:
            message, wannabeAddress = clientSocket.recvfrom(2048)
            message = message.decode()

            #verifica sequencia e manda ack
            message = espera_seq(seq,message, (serverIP,serverPort), wannabeAddress)
            message = message.split(';',maxsplit=1)[1]
            # print('message',message)
            seq = invert_seq(seq)

            if message == 'Arquivo inexistente':
                print('Arquivo não existe!')
                arq.close()
                os.remove('./'+resposta[2:])
                break
            elif message != '':
                arq.write(message.encode())
            else:
                print('recebido!')
                break
        arq.close()


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

        message = espera_seq(seq,message, (serverIP,serverPort),wannabeAddress)
        message = message.split(';',maxsplit=1)[1]
        seq = invert_seq(seq)
        print(message)
        while message != '':
            message, wannabeAddress = clientSocket.recvfrom(2048)
            message = message.decode()

            message = espera_seq(seq,message, (serverIP,serverPort),wannabeAddress)
            message = message.split(';',maxsplit=1)[1]
            seq = invert_seq(seq)
            print(message)

    elif resposta[0] == '3':
        print('Ate logo!')
        break
    # 0;opcao ou nome

