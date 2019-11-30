'''
Nesta parte, dever ́a ser implementado um servidor que, ao ser inicializado, envie ao servidor
DNS local seu nome e endere ̧co IP. Em seguida, este servidor deve esperar por solicitac ̧ ̃oes de
clientes na rede e ao receber, enviar o arquivo solicitado, ou informar a inexistˆencia do
mesmo. O cliente tamb ́em poder ́a requisitar os arquivos dispon ́ıveis no reposit ́orio ou encerrar
a conex ̃ao.
'''
from socket import *
 serverPort = 4242
 serverSocket = socket(AF_INET,SOCK_STREAM)
 serverSocket.bind((’’,serverPort))
 serverSocket.listen(1)
 print ‘The server is ready to receive’
 while 1:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024)
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence)
        connectionSocket.close()

        try:
            