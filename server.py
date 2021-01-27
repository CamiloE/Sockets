from socket import *
from threading import *
import string

class MiLicorera:
    def __init__(self, ip, puerto):
        self.ip=ip 
        self.puerto=puerto
        self.db={"nombre":['Aguardiente','Ron','Whiskey','Vino Tinto','Vodka'],
                "codigo":[1,2,3,4,5],
                    "precio":[40000,80000,125000,95000,65000],
                    "cantidad":[5,5,5,5,5],
                    "procedencia":[".co",".co",".uk",".cl",".ru"]}#Base de datos con la informacion de los licores
        self.tcpserver=socket(AF_INET,SOCK_STREAM)#Creacion de un servidor TCP 
    def handle(self,conn,add):#Funcion del manejador de las solicitudes de los clientes
        bienvenida= "Bienvenido a LiquoStore, para nosotros es un gusto atenderlo\n"
        conn.send(bienvenida)
        ok=conn.recv(50)
        print ok
        conn.send("\t\tLas opciones para interactuar con nosotros son las siguientes\n")
        ok=conn.recv(50)
        print ok
        self.opciones(conn)
        conectado=True
        while conectado:
            datos=conn.recv(1024)
            print datos
            if datos=="SALIR":
                index=dir_user.index(add)
                user_list.pop(index)
                dir_user.remove(add)
                break
            elif datos=="MOSTRAR":
                self.mostrar(conn)
            elif datos=="COMPRAR":
                self.comprar(conn,add)
            elif datos=="USUARIOS":
                self.usuarios_conectados(conn)
            else:
                conn.send("Lo sentimos, la opcion no esta disponible")
        conn.close()
    def start(self):#Funcion para iniciar el servidor
        self.tcpserver.bind((self.ip,self.puerto))#Asignacion de la IP y del Puerto
        self.tcpserver.listen(5)#Escucha conexiones
        print "Esperando conexion"
        while True:
            conn,add=self.tcpserver.accept()#Acepta la conexion de un usuario
            print "Conexion desde ",add
            name = str(conn.recv(1024))
            dir_user.append(add) 
            user_list.append(name)#Agrega el usuario a una lista
            thread=Thread(target=self.handle,args=(conn,add)) #Crea los subprocesos para los multiples clientes
            thread.start()#Inicia el hilo
    def stop(self):#Funcion para detener el servidor
        self.tcpserver.stop()
        print "Servidor Desconectado..."
    def opciones(self,conn):#Muestra al usuario las opciones disponibles para interactuar con el servidor
        menu="1)MOSTRAR: para mostrar el catalogo de licores disponibles\n"+"2)COMPRAR: para comprar un solo licor\n"+"3)USUARIOS: para mostrar los usuarios conectados\n"+"4)SALIR: para desconectarse del servidor\n"
        conn.send(menu)
    def mostrar(self,conn):#Muestra la informacion de los licores
        for i in range(0,5):
            msg=str(self.db["nombre"][i])+'\t\t'+'cod: '+ str(self.db["codigo"][i])+'\t\t'+str(self.db["precio"][i])+ '\t\t'+str(self.db["cantidad"][i])+' und' +"\t\t"+ str(self.db["procedencia"][i])+'\n'
            conn.send(msg)
    def comprar(self,conn,add):#Realiza la compra del licor
        #Envia las opciones de trago disponible
        menu="1) Aguardiente\n"+"2) Ron\n"+"3) Whiskey\n"+"4) Vino Tinto \n"+"5) Vodka\n"
        conn.send(menu)
        opcion=int(conn.recv(8))#Recibe la opcion seleccionada por el usuario
        if opcion==1:
            ans=self.conectar_banco(add,self.db["precio"][0])#Realizar la conexion con el banco para el pago
            if ans=="ACEPTADO":
                conn.send(self.db["nombre"][0]+'\n')#Entrega el licor correspondiente
                self.actualizar(0)#Actualiza la cantidad de licores en la base de datos
            else:
                conn.send("ERROR EN EL PAGO, SALDO INSUFICIENTE")
        elif opcion==2:
            ans=self.conectar_banco(add,self.db["precio"][1])#Realizar la conexion con el banco para el pago
            if ans=="ACEPTADO":
                conn.send(self.db["nombre"][1]+'\n')#Entrega el licor correspondiente
                self.actualizar(1)#Actualiza la cantidad de licores en la base de datos
            else:
                conn.send("ERROR EN EL PAGO, SALDO INSUFICIENTE")
        elif opcion==3:
            ans=self.conectar_banco(add,self.db["precio"][2])#Realizar la conexion con el banco para el pago
            if ans=="ACEPTADO":
                conn.send(self.db["nombre"][2]+'\n')#Entrega el licor correspondiente
                self.actualizar(2)#Actualiza la cantidad de licores en la base de datos
            else:
                conn.send("ERROR EN EL PAGO, SALDO INSUFICIENTE")
        elif opcion==4:
            ans=self.conectar_banco(add,self.db["precio"][3])#Realizar la conexion con el banco para el pago
            if ans=="ACEPTADO":
                conn.send(self.db["nombre"][3]+'\n')#Entrega el licor correspondiente
                self.actualizar(3)#Actualiza la cantidad de licores en la base de datos
            else:
                conn.send("ERROR EN EL PAGO, SALDO INSUFICIENTE")
        elif opcion==5:
            ans=self.conectar_banco(add,self.db["precio"][1])#Realizar la conexion con el banco para el pago
            if ans=="ACEPTADO":
                conn.send(self.db["nombre"][4]+'\n')#Entrega el licor correspondiente
                self.actualizar(4)#Actualiza la cantidad de licores en la base de datos
            else:
                conn.send("ERROR EN EL PAGO, SALDO INSUFICIENTE")
    def actualizar(self,n):
        self.db["cantidad"][n]=self.db["cantidad"][n]-1#Actualiza la cantidad de licores en la base de datos
    def usuarios_conectados(self,conn):#Envia al usuario la lista de los usuarios conectados
        lista=""
        for user in user_list:
            lista=lista+"-> "+user+"\n"
        conn.send(lista)
    def conectar_banco(self,add,n):#Funcion para conectar con el banco para el pago automatico
        c=socket(AF_INET,SOCK_DGRAM)#Crea una conexion UDP para realizar el pago con el banco
        i=dir_user.index(add)
        name=user_list[i]
        vlr=str(n)
        cifrado1=self.cifrado_letras(name,5) #cifra el nombre del usuario
        cifrado2=self.cifrado_numeros(vlr,5) #cifra el precio
        req=cifrado1+":"+cifrado2
        print req
        c.sendto(req,("127.0.0.1",5050)) #envia el cifrado al banco
        ans, remoto=c.recvfrom(1024)#Recibe la respuesta del banco
        c.close()#Cierra la conexion con el banco
        return ans #retorna la respuesta del banco
    def cifrado_letras(self,text,n): #FUncion que cifra las letras con algoritmo cesar
        intab=string.ascii_lowercase
        outrab = intab[ n % 26:] + intab[:n%26]
        trantab = string.maketrans(intab,outrab)
        return text.translate(trantab)
    def cifrado_numeros(self,text,n): #FUncion que cifra los numeros con algoritmo cesar
        intab=string.digits
        outrab = intab[ n % 10:] + intab[:n%10]
        trantab = string.maketrans(intab,outrab)
        return text.translate(trantab)

user_list=[]#Lista con los usuarios conectados
dir_user=[]#lista con las ips y puertos del cliente.
licorera=MiLicorera("127.0.0.1",1234)
licorera.start()