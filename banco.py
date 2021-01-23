from socket import *
from threading import *

class Banco:
    def __init__(self, ip,puerto):
        self.ip=ip
        self.puerto=puerto
        self.db={"Nombres":["Camilo","Alexandra"],
        "NoCuenta":["1111","2222"],
        "Contrasenas":["pass1","pass2"], "Saldo" : [500000,500000]}
        self.tcpserver=socket(AF_INET,SOCK_STREAM)
        self.udpserver=socket(AF_INET,SOCK_DGRAM)
    def start(self):
        self.tcpserver.bind((self.ip,self.puerto))
        self.udpserver.bind((self.ip,5050))
        #
        print "Esperando conexion..."
        thread=Thread(target=self.tcp_handler)
        thread.start()
        thread2=Thread(target=self.udp_handler)
        thread2.start()
    def tcp_handler(self):
        print "entra al tcp"
        while True:
            self.tcpserver.listen(5)
            conn, add=self.tcpserver.accept()
            print "Conexion desde ",add
            conn.send("Bienvenido a su banco, a continuacion se mostrara las opciones\n para que ingrese el numero correspondiente")
            self.opciones(conn)
        #while True:
    def udp_handler(self):
        print "Entra al udp"
        while True:
            data,remote_host = self.udpserver.recvfrom(1024)
            print data
            print remote_host
    def opciones(self,conn):
        menu="1) Consultar saldo\n"+"2) Retirar\n"+"3) Consignar\n"+"4) Salir\n"
        conn.send(menu)


banco=Banco("127.0.0.1",6789)
banco.start()