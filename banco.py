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
        #thread2=Thread(target=self.udp_handler)
        #thread2.start()
        while True:
            thread2=Thread(target=self.udp_handler)
            thread2.start()
            self.tcpserver.listen(5)
            conn,add=self.tcpserver.accept()#Acepta la conexion de un usuario
            print "Conexion desde ",add
            thread=Thread(target=self.tcp_handler,args=(conn,add)) #Crea los subprocesos para los multiples clientes
            thread.start()
    def tcp_handler(self,conn,add):
        conn.send("Bienvenido")
    def udp_handler(self):
        print "Entra al udp"
        while True:
            data,remote_host = self.udpserver.recvfrom(1024)
            print data
            print remote_host
            add,p=remote_host
            self.udpserver.sendto("respuesta udp a"+str(p),remote_host)
    def opciones(self,conn):
        menu="1) Consultar saldo\n"+"2) Retirar\n"+"3) Consignar\n"+"4) Salir\n"
        conn.send(menu)


banco=Banco("127.0.0.1",6789)
banco.start()
