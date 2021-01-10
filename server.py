from socket import *
from threading import *

class MiBanco:
    def __init__(self, ip, puerto):
        self.ip=ip 
        self.puerto=puerto
        self.db={"nombre":['Aguardiente','Ron','Whiskey'],
                "codigo":[1,2,3],
                    "precio":[22000,37000,60000],
                    "cantidad":[5,5,5]}
        self.tcpserver=socket(AF_INET,SOCK_STREAM)
    def handle(self,conn,add):
        bienvenida= "Bienvenido a LiquoStore, para nosotros es un gusto atenderlo\n"
        conn.send(bienvenida)
        conn.send("\t\tLas opciones para interactuar con nosotros son las siguientes\n")
        conn.send("\n")
        self.opciones(conn)
        conectado=True
        while conectado:
            datos=conn.recv(1024)
            if datos=="SALIR\r\n":
                user_list.remove(add)
                conn.close()
                break
            elif datos=="MOSTRAR\r\n":
                self.mostrar(conn)
            elif datos=="COMPRAR\r\n":
                self.comprar(conn)
            elif datos=="USUARIOS\r\n":
                self.usuarios_conectados(conn)
            else:
                conn.send("Lo sentimos, la opcion no esta disponible")
    def start(self):
        self.tcpserver.bind((self.ip,self.puerto))
        self.tcpserver.listen(5)
        print "Esperando conexion"
        while True:
            conn,add=self.tcpserver.accept()
            print "Conexion desde ",add
            user_list.append(add)
            thread=Thread(target=self.handle,args=(conn,add))
            thread.start()
    def stop(self):
        self.tcpserver.stop()
        print "Servidor Desconectado..."
    def opciones(self,conn):
        conn.send("1)MOSTRAR: para mostrar el catalogo de licores disponibles\n")
        conn.send("2)COMPRAR: para comprar un solo licor\n")
        conn.send("3)USUARIOS: para mostrar los usuarios conectados\n")
        conn.send("4)SALIR: para desconectarse del servidor\n")
    def mostrar(self,conn):
        for i in range(0,3):
            msg=str(self.db["nombre"][i])+'\t\t'+'cod: '+ str(self.db["codigo"][i])+'\t\t'+str(self.db["precio"][i])+ '\t\t'+str(self.db["cantidad"][i])+' und' +'\n'
            conn.send(msg)
    def comprar(self,conn):
        conn.send("1) Aguardiente\n")
        conn.send("2) Ron\n")
        conn.send("3) Whiskey\n")
        opcion=int(conn.recv(8))
        if opcion==1:
            conn.send("Tenga su "+self.db["nombre"][0]+'\n')
            self.actualizar(0)
        elif opcion==2:
            conn.send("Tenga su "+self.db["nombre"][1]+'\n')
            self.actualizar(1)
        elif opcion==3:
            conn.send("Tenga su "+self.db["nombre"][2]+'\n')
            self.actualizar(2)
    def actualizar(self,n):
        self.db["cantidad"][n]=self.db["cantidad"][n]-1
    def usuarios_conectados(self,conn):
        for user in user_list:
            conn.send(str(user)+'\n') 

user_list=[]
banco=MiBanco("127.0.0.1",1234)
banco.start()