from socket import *
from threading import *

class MiLicorera:
    def __init__(self, ip, puerto):
        self.ip=ip 
        self.puerto=puerto
        self.db={"nombre":['Aguardiente','Ron','Whiskey'],
                "codigo":[1,2,3],
                    "precio":[22000,37000,60000],
                    "cantidad":[5,5,5]}#Base de datos con la informacion de los licores
        self.tcpserver=socket(AF_INET,SOCK_STREAM)#Creacion de un servidor TCP 
    def handle(self,conn,add):#Funcion del manejador de las solicitudes de los clientes
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
    def start(self):#Funcion para iniciar el servidor
        self.tcpserver.bind((self.ip,self.puerto))#Asignacion de la IP y del Puerto
        self.tcpserver.listen(5)#Escucha conexiones
        print "Esperando conexion"
        while True:
            conn,add=self.tcpserver.accept()#Acepta la conexion de un usuario
            print "Conexion desde ",add 
            user_list.append(add)#Agrega el usuario a una lista
            thread=Thread(target=self.handle,args=(conn,add)) #Crea los subprocesos para los multiples clientes
            thread.start()#Inicia el hilo
    def stop(self):#Funcion para detener el servidor
        self.tcpserver.stop()
        print "Servidor Desconectado..."
    def opciones(self,conn):#Muestra al usuario las opciones disponibles para interactuar con el servidor
        conn.send("1)MOSTRAR: para mostrar el catalogo de licores disponibles\n")
        conn.send("2)COMPRAR: para comprar un solo licor\n")
        conn.send("3)USUARIOS: para mostrar los usuarios conectados\n")
        conn.send("4)SALIR: para desconectarse del servidor\n")
    def mostrar(self,conn):#Muestra la informacion de los licores
        for i in range(0,3):
            msg=str(self.db["nombre"][i])+'\t\t'+'cod: '+ str(self.db["codigo"][i])+'\t\t'+str(self.db["precio"][i])+ '\t\t'+str(self.db["cantidad"][i])+' und' +'\n'
            conn.send(msg)
    def comprar(self,conn):#Realiza la compra del licor
        #Envia las opciones de trago disponible
        conn.send("1) Aguardiente\n")
        conn.send("2) Ron\n")
        conn.send("3) Whiskey\n")
        opcion=int(conn.recv(8))#Recibe la opcion seleccionada por el usuario
        if opcion==1:
            ans=self.conectar_banco()#Realizar la conexion con el banco para el pago
            if ans=="ACEPTADO":
                conn.send("Tenga su "+self.db["nombre"][0]+'\n')#Entrega el licor correspondiente
                self.actualizar(0)#Actualiza la cantidad de licores en la base de datos
        elif opcion==2:
            ans=self.conectar_banco()#Realizar la conexion con el banco para el pago
            if ans=="ACEPTADO":
                conn.send("Tenga su "+self.db["nombre"][1]+'\n')#Entrega el licor correspondiente
                self.actualizar(1)#Actualiza la cantidad de licores en la base de datos
        elif opcion==3:
            ans=self.conectar_banco()#Realizar la conexion con el banco para el pago
            if ans=="ACEPTADO":
                conn.send("Tenga su "+self.db["nombre"][2]+'\n')#Entrega el licor correspondiente
                self.actualizar(2)#Actualiza la cantidad de licores en la base de datos
    def actualizar(self,n):
        self.db["cantidad"][n]=self.db["cantidad"][n]-1#Actualiza la cantidad de licores en la base de datos
    def usuarios_conectados(self,conn):#Envia al usuario la lista de los usuarios conectados
        for user in user_list:
            conn.send(str(user)+'\n')
    def conectar_banco(self):
        c=socket(AF_INET,SOCK_DGRAM)#Crea una conexion UDP para realizar el pago con el banco
        c.sendto("PAGAR",("127.0.0.1",5050))
        ans, remoto=c.recvfrom(1024)#Recibe la respuesta del banco
        c.close()#Cierra la conexion con el banco
        return ans 

user_list=[]#Lista con los usuarios conectados
licorera=MiLicorera("127.0.0.1",1234)
licorera.start()