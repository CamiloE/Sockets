from socket import *
from threading import *

class Banco:
    def __init__(self, ip,puerto):
        self.ip=ip
        self.puerto=puerto
        self.db={"Nombres":["Camilo","Alexandra"],
        "NoCuenta":["1111","2222"],
        "Contrasenas":["pass1","pass2"]}
        self.tcpserver=socket(AF_INET,SOCK_STREAM)
        self.udpserver=socket(AF_INET,SOCK_DGRAM)
    def start(self):
        self.tcpserver.bind((self.ip,self.puerto))
        self.udpserver.bind((self.ip,5050))
        self.tcpserver.listen(5)
        print "Esperando conexion..."
        while True:
            conn, add=self.tcpserver.accept()
            print "Conexion desde ",add
            thread=Thread(self.tcp_handler, args=(conn,add))
            thread.start()
    def tcp_handler(self,conn,add):
        conn.send("Bienvenido a su banco, a continuacion se mostrara las opciones\n para que ingrese el numero correspondiente")
        self.opciones(conn)
    def opciones(self,conn):
        menu="1) Consultar saldo\n"+"2) Retirar\n"+"3) Consignar\n"+"4) Salir\n"
        conn.send(menu)


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