'''
O servidor inicia registrando se no DNS, fornecendo o seu nome junto com o seu IP e porta atraves de mensagens usando o protocolo UDP.
Apos o registro, o servidor foca a espera de um cliente a se conectar. O servidor tem suporte a 3 comandos:
'lista': que responde com a lista de arquivos .txt que possui
'envia': que envia o arquivo requirido
'encerra': que encerra a conexao com o cliente
qualquer outro comando ele responde como comando nao suportado.

'''


import os
import socket
SERVER_IP = ''
SERVER_PORT = 1323
BUFFER_SIZE = 1024


def Registra_Servidor():
    
    DNS_PORT = 4241
    #cria socket UPD
    sock_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
    print("Socket UDP criado!\n\n")

    print("Digite o nome do seu servidor:")
    ServerName = input()

    print("Considerando que o IP é",socket.gethostbyname(socket.gethostname()))
    DNS_IP = socket.gethostbyname(socket.gethostname())

    #envia para o DNS o comando para registrar se junto com o seu nome
    print("\nRegistrando este servidor no DNS...")
    sock_UDP.sendto(("register " + ServerName).encode(),(DNS_IP, DNS_PORT))

    sock_UDP.close()


def lista_arquivos(): #Retorna uma lista contendo os arquivos .txt no diretório do codigo. 

    # files = []
    # for r, d, f in os.walk('files/'): 
    #     for file in f:
    #         if '.txt' in file:
    #             files.append(os.path.join(r, file))
    
    files = os.listdir('./files/')

    print(files)
    return files

'''
Tenta abrir o arquivo com o nome fornecido. Caso nao exista, retorna a string 'Arquivo nao existente'
Caso exista, abre o arquivo e armazena seu conteudo em uma variavel e retorna essa variavel
'''
def envia_arquivo(filename): #precisa de ajustes se o tamanho tamanho do arquivo foi muuuito grande
    try:
        print("Abrindo o arquivo...")
        file = open(filename,'rb')
    except:
        print("Arquivo nao existente.")
        return 'Arquivo nao existente'
    l = file.read()

    file.close()
    return l


print("Iniciando o servidor...")

#Registra o servidor no DNS
print("Preparando para registrar o servidor no DNS...")
Registra_Servidor()

#Cria o socket TCP e espera por uma conexao
sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_TCP.bind((SERVER_IP, SERVER_PORT))
sock_TCP.listen(1)
print("Socket TCP criado!")


while 1:
    conn, addr = sock_TCP.accept()
    print(f"Conexao com {addr} realizada")
    data = conn.recv(BUFFER_SIZE).decode().split()
    print(data)

    if data[0] == 'lista': #Caso receba o comando lista, responde com a lista de arquivos .txt existentes
        conn.send(str(lista_arquivos()).encode()) 
    elif data[0] == 'envia': #Caso receba o comando envia, responde enciando o arquivo requisitado para o cliente
        conn.send(str(envia_arquivo(data[1])).encode())
    elif data[0] == 'encerra': #Caso receba o comando encerra, responde dizendo que ira encerrar a conexao e a encerra
        conn.send(('Encerrando conexao...').encode())
        conn.close()
    else: #Caso receba um comando nao reconhecido, responde comando nao ceconhecido
        conn.send(('Comando nao reconhecido').encode())






