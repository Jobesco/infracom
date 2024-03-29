#coding: UTF-8
'''
O cliente inincia mandando uma mensagem para o servidor DNS, consultando o servidor que deseja conectar-se. Se o DNS possuir o IP para aquele nome, o cliente
o recebe como resposta e, entao realiza uma conexao TCP com o servidor.

O servidor possui 3 comandos reconheciveis:

'lista': que manda como resposta uma lista de arquivos .txt que possui
'envia '<nome.txt>: que envia o arquivo requisitado. Este arquivo eh entao salvo pelo cliente em uma pasta separada chamada 'Client_files'
'encerra': que encerra a conexao com o servidor
'''

import os
import socket

BUBBER_SIZE = 1024
SERVER_PORT = 1323


def request_dns():
    DNS_PORT = 4241

    #cria um socket UDP
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Socket UDP criado!")

    print("Considerando que o IP DNS é",socket.gethostbyname(socket.gethostname()))
    DNS_IP = socket.gethostbyname(socket.gethostname())

    print("Digite o nome do servidor desejado:")
    req = input()

    #Envia a mensagem para o DNS contendo o comando 'client ' e o nome do servidor requisitado 
    print("Enviando mensagem para o DNS...")
    s_udp.sendto(('client ' + req).encode(), (DNS_IP, DNS_PORT))

    #Recebe a resposta do DNS e o retorna
    data, addr = s_udp.recvfrom(2048)
    data = data.decode()

    return data


#Cria um socket TCP para comunicar se com o cliente
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

SERVER_IP = request_dns()
    
s.connect((SERVER_IP, SERVER_PORT))

while 1:
    
    print("Envie a sua mensagem:")
    mensagem = input()

    s.send(mensagem.encode())
    print("\nMensagem enviada\n")
    
    #Separa a mensagem enviada para saber o que ira receber como resposta
    mensagem = mensagem.split()

    #Se enviou um comando de envia...
    if mensagem[0] == 'envia':
        data = s.recv(BUBBER_SIZE).decode()
        
        #Se a resposta nao for a seguinte, abre ou cria se um arquivo no diretorio escrito abaixo e escreve o que foi recebido 
        if data != 'Arquivo nao existente':
            arq = open('client_files/' + mensagem[1], 'wb')
            arq.write(data.encode())
            arq.close()
        #Se recebeu como resposta 'Arquivo nao existente' printa a resposta abaixo
        else:
            print(data)
    #Se nao, printa a resposta recebida
    else:
        data = s.recv(BUBBER_SIZE)
        print(data.decode())
