import os
import socket

DNS_IP = "127.0.0.1"
DNS_PORT = 666


print("Iniciando servidor DNS...")
print("Criando socket...")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((DNS_IP, DNS_PORT))

print("Servidor DNS pronto! Aguardando mensagens...")
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print (f"Mensagem recebida de {addr} :")
    print(data) 