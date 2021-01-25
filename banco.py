from socket import *
from threading import *
import os
import string

class Banco:
    def __init__(self, ip,puerto):
        self.ip=ip
        self.puerto=puerto
        self.db={"Nombres":["camilo","alexandra","andres"],
        "NoCuenta":["1111","2222", "3333"],
        "Contrasenas":["pass1","pass2","pass3"], 
        "Saldo" : [10000,500000,500000]}
        self.ban=False

        self.tcpserver=socket(AF_INET,SOCK_STREAM)
        self.udpserver=socket(AF_INET,SOCK_DGRAM)
    def start(self):
        try:
            self.tcpserver.bind((self.ip,self.puerto))
            #self.tcpserver.listen(5)
        except:
            print "puerto ocupado o INBOX equivocado"
            self.tcpserver.close()
            os._exit(0)       #
        print "Esperando conexion..."
        while True:
            self.tcpserver.listen(5)
            conn,add=self.tcpserver.accept()#Acepta la conexion de un usuario
            print "Conexion desde ",add
            thread=Thread(target=self.tcp_handler,args=(conn,add)) #Crea los subprocesos para los multiples clientes
            thread.start()

    def tcp_handler(self,conn,add):
        bienvenida= "Bienvenido a su Banco, para nosotros es un gusto atenderlo\n"
        conn.send(bienvenida)
        self.autenticacion (conn,add)
        if self.ban==True:
            conn.send("\t\tLas opciones para interactuar con nosotros son las siguientes\n")
            ok=conn.recv(50)
            print ok
            self.opciones(conn)
        while self.ban:
            datos=conn.recv(1024)
            print datos
            if datos=="SALIR":
                break
            elif datos=="SALDO":
                self.saldo(conn,add)
            elif datos=="RETIRAR":
                self.retirar(conn,add)
            elif datos=="CONSIGNAR":
                self.consignar(conn,add)
            else:
                conn.send("Lo sentimos, la opcion no esta disponible")
        print "Cerrando conexion"
        conn.close()

    def udp_handler(self):
        print "Entra al udp"
        try:
            self.udpserver.bind((self.ip,5050))
        except:
            print "puerto ocupado o INBOX equivocado"
            self.udpserver.close()
            os._exit(0)
        #print "Entra al udp"
        while True:
            data,remote_host = self.udpserver.recvfrom(1024)
            print data
            cifrado1=data.split(":")[0]
            cifrado2=data.split(":")[1]
            name=self.decifrado_letras(cifrado1,-5)
            vlr=self.decifrado_numeros(cifrado2,-5)
            #print name+":"+vlr
            ans=self.debitar(name,int(vlr))
            self.udpserver.sendto(ans,remote_host)

    def autenticacion(self,conn,add):
        conn.send("Ingrese Usuario")
        usuario=str(conn.recv(1024))
        print usuario
        if usuario in self.db["Nombres"]:
            print "entro al if"
            self.index= self.db["Nombres"].index(usuario)
            dir_user.append(add)
            user_list.append(usuario)
            conn.send("Usuario Valido\n")
            ok=conn.recv(30)
            print ok
            conn.send("Ingrese la contrasena\n")
            contrasena= conn.recv(1024)
            print contrasena
            if contrasena == self.db["Contrasenas"][self.index]:
                conn.send("Ingreso Exitoso")
                ok=conn.recv(40)
                print ok
                self.ban=True
            else:
                conn.send("Contrasena no Valida...cerrando conexion")
                #conn.close()
                self.ban=False   

        else:
            conn.send("Usuario no valido...cerrando conexion")
            #conn.close()
            self.ban=False


    def opciones(self,conn):#Muestra al usuario las opciones disponibles para interactuar con el Banco
        menu="1)SALDO: para conocer su saldo disponible\n"+"2)RETIRAR: para retirar dinero de su cuenta\n"+"3)CONSIGNAR: para retirar dinero de su cuenta\n"+"4)SALIR: para desconectarse del banco\n"
        conn.send(menu)   
    
    def saldo(self,conn,add):
        i=dir_user.index(add)
        e=user_list[i]
        i2=self.db["Nombres"].index(e)
        conn.send("Su saldo es : \n"+ str(self.db["Saldo"][i2]))

    
    def retirar(self,conn,add):
        i=dir_user.index(add)
        e=user_list[i]
        i2=self.db["Nombres"].index(e)
        conn.send("ingrese valor que desea retirar")
        valor= int(conn.recv(1024))  
        if valor > self.db["Saldo"][i2]:
            conn.send("El valor supera su saldo")  
        else:
            self.db["Saldo"][i2] =  self.db["Saldo"][i2] - valor
            conn.send("Dinero retirado")
        
    def consignar(self,conn,add):
        i=dir_user.index(add)
        e=user_list[i]
        i2=self.db["Nombres"].index(e)
        conn.send("Ingrese Valor que desea consignar... maximo puede consignar 1 millon")
        consig= int(conn.recv(1024))
        if consig > 1000000:
            conn.send("Valor no valido")
        else:
            self.db["Saldo"][i2] =  self.db["Saldo"][i2] + consig
            conn.send("Dinero consignado")
    def decifrado_letras(self,text,n):
        intab=string.ascii_lowercase
        outrab = intab[ n % 26:] + intab[:n%26]
        trantab = string.maketrans(intab,outrab)
        return text.translate(trantab)
    def decifrado_numeros(self,text,n):
        intab=string.digits
        outrab = intab[ n % 10:] + intab[:n%10]
        trantab = string.maketrans(intab,outrab)
        return text.translate(trantab)
    def debitar(self,name,vlr):
        i=self.db["Nombres"].index(name)
        if self.db["Saldo"][i]>=vlr:
            self.db["Saldo"][i]=self.db["Saldo"][i]-vlr
            return "ACEPTADO"
        else:
            return "ERROR"


user_list=[]
dir_user=[]
banco=Banco("127.0.0.1",6789)
thread1=Thread(target=banco.udp_handler,args=())
thread1.start()
banco.start()