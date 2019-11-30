from socket import *
serverPort = 4242

clientSocket = socket(socket.AF_INET, socket.SOCK_DGRAM)

#retorna a mensagem
def get_ack(seq, msg):
    clientSocket.settimeout(2.5)
    timeout_cond = 1
    while timeout_cond:
        try:
            resp, addr = clientSocket.recvfrom(2048)
            if addr[0] != serverIP:
                pass
            elif resp[0] != seq:
                clientSocket.sendto(msg,(serverIP,serverPort))
            else: timeout_cond = 0
        except timeout:
            print('timeout! Sending again...')
            timeout_cond = 1
            clientSocket.sendto(msg,(serverIP,serverPort))

    clientSocket.settimeout(0)
    return resp.split(';',1)[1]

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
#solicita nome do servidor
while True:
    serverName = input('Para qual servidor você quer se conectar?')
    serverName = 'client ' + serverName
    #TODO fix IP?
    clientSocket.sendto(serverName,('127.0.0.1',serverPort))

    serverIP, _ = clientSocket.recvfrom(2048)

    prompt = 'Bem vindo!\n' \
        'Por favor, escolha uma das opções abaixo:\n' \
        '1 - Solicitar Arquivo\n2 - Listar Arquivos\n3 - Sair'
    resposta = input(prompt)
    #começo de protocolo UDP
    if resposta[0] == '1':

        clientSocket.sendto('0;1',(serverIP,serverPort))

        get_ack('0', '0;1')


        resposta = input('Qual o nome do Arquivo?')
        arq = open(resposta,'wb')
        resposta = '1;' + resposta
        clientSocket.sendto(resposta, (serverIP,serverPort))

        recebe_arquivo(resposta,arq)

    elif resposta[0] == '2':
        clientSocket.sendto('0;2',(serverIP,serverPort))

        get_ack('0', '0;2')
        
        lista_files, _ = clientSocket.recvfrom(2048)

        print(lista_files)
    elif resposta[0] == '3':
        print('Até logo!')
        break
    # 0;opçao ou nome

