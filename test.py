try:
    arq = open('files/file1.txt','rb')
except err:
    print('erro porra')
    exit(self,0)

# print(arq.read().decode())
# fora = arq.read(5)
# while fora != '':
#     print(fora)
#     fora = arq.read(5)
print(arq.read(5))
print(arq.read(5))
print(arq.read(5))
print(arq.read(5))
print(arq.read(5))
print(arq.read(5))
print(arq.read(5))
print(arq.read(5))


# Lê usando .read(numero de bytes) enquanto o resultado lido for diferente de vazio ou tiver a qtd de bytes esperada