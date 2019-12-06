# coding: UTF-8

from socket import *
serverPort = 4242
dnsPort = 4241

clientSocket = socket(AF_INET, SOCK_DGRAM)

#! ele automaticamente coloca o numero de sequencia e ;
#TODO desistir apos x tentativas
#retorna so a mensagem
def get_ack(seq, msg):
    clientSocket.settimeout(2.5)
    while True:
        try:
            resp, addr = clientSocket.recvfrom(2048)
            resp = resp.decode()
            if addr[0] != serverIP:
                pass
            elif resp[0] != seq:
                clientSocket.sendto((seq+';'+msg).encode(),(serverIP,serverPort))
            elif resp == 'busy':
                raise TypeError
            else: 
                clientSocket.settimeout(0)
                print(resp)
                return resp.split(';',maxsplit=1)[1]
        except timeout:
            print('timeout! Sending again...')
            clientSocket.sendto((seq+';'+msg).encode(),(serverIP,serverPort))
        except TypeError:
            r = input('O servidor esta ocupado!\nPressione 1 para continuar ou 2 para sair\n')
            if r == '2':
                exit(0)
        except ConnectionResetError:
            print('o servidor caiu!')
            exit(1)

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
dnsAddress = '172.22.71.12'
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
        
        lista_files, _ = clientSocket.recvfrom(2048)
        lista_files = lista_files.decode()

        print(lista_files)
    elif resposta[0] == '3':
        print('Ate logo!')
        break
    # 0;opcao ou nome

