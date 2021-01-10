from socket import *
from threading import *

server=socket(AF_INET,SOCK_DGRAM)
server.bind(("127.0.0.1",5050))
print "Esperando conexion..."
while True:
    datos, host_remoto=server.recvfrom(1024)
    print datos
    if datos=="bye\n":
        server.close()
        break
    elif datos=="PAGAR":
        server.sendto("ACEPTADO",host_remoto)
    else:
        server.sendto("Hola desde el banco\n",host_remoto)