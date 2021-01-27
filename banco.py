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
        "Saldo" : [405000,405000,405000]}#base de datos que contiene la info de los clientes
        self.ban=False#bandera para usarla en el manejador de conexiones

        self.tcpserver=socket(AF_INET,SOCK_STREAM)
        self.udpserver=socket(AF_INET,SOCK_DGRAM)
    def start(self):
        try:
            self.tcpserver.bind((self.ip,self.puerto))
        except:
            print "puerto ocupado o INBOX equivocado"
            self.tcpserver.close()
            os._exit(0)
        print "Esperando conexion..."
        while True:
            self.tcpserver.listen(5)
            conn,add=self.tcpserver.accept()#Acepta la conexion de un usuario
            print "Conexion desde ",add
            thread=Thread(target=self.tcp_handler,args=(conn,add)) #Crea los subprocesos para los multiples clientes por tcp
            thread.start()#inicia los hilos

    def tcp_handler(self,conn,add):#Manejador de conexiones TCP
        bienvenida= "Bienvenido a su Banco, para nosotros es un gusto atenderlo\n"
        conn.send(bienvenida)
        ok=conn.recv(50)
        print ok
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

    def udp_handler(self): #Manejador de conexiones udp
        try:
            self.udpserver.bind((self.ip,5050))#Inicializa los parametros de red
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
            name=self.decifrado_letras(cifrado1,-5)#decifra el nombre de usuario
            vlr=self.decifrado_numeros(cifrado2,-5)#decifra el valor
            ans=self.debitar(name,int(vlr))#realiza el pago automatico, descontando el saldo
            self.udpserver.sendto(ans,remote_host)#envia la respuesta a la licorera

    def autenticacion(self,conn,add):#realiza la autenticacion de los clientes
        conn.send("Ingrese Usuario")
        usuario=str(conn.recv(1024))
        print usuario
        if usuario in self.db["Nombres"]: #revisa que el usuario sea valido
            self.index= self.db["Nombres"].index(usuario)
            dir_user.append(add)
            user_list.append(usuario)
            conn.send("Usuario Valido\n")
            ok=conn.recv(30)
            print ok
            conn.send("Ingrese la contrasena\n")
            contrasena= conn.recv(1024)
            print contrasena
            if contrasena == self.db["Contrasenas"][self.index]:#revisa la contrasena sea valida
                conn.send("Ingreso Exitoso")
                ok=conn.recv(40)
                print ok
                self.ban=True
            else:#cierra la  conexion cuando la autenticacion falla
                conn.send("Contrasena no Valida...cerrando conexion")
                self.ban=False   

        else:#cierra la  conexion cuando la autenticacion falla
            conn.send("Usuario no valido...cerrando conexion")
            self.ban=False


    def opciones(self,conn):#Muestra al usuario las opciones disponibles para interactuar con el Banco
        menu="1)SALDO: para conocer su saldo disponible\n"+"2)RETIRAR: para retirar dinero de su cuenta\n"+"3)CONSIGNAR: para retirar dinero de su cuenta\n"+"4)SALIR: para desconectarse del banco\n"
        conn.send(menu)   
    
    def saldo(self,conn,add):#FUncion para enviar al usuario su saldo
        i=dir_user.index(add)
        e=user_list[i]
        i2=self.db["Nombres"].index(e)
        conn.send("Su saldo es : \n"+ str(self.db["Saldo"][i2]))

    
    def retirar(self,conn,add):#funcion para darle dinero al usuario
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
        
    def consignar(self,conn,add):#FUNCION para consignar dinero en la cuenta
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
    def decifrado_letras(self,text,n): #desencrippta el ususario
        intab=string.ascii_lowercase
        outrab = intab[ n % 26:] + intab[:n%26]
        trantab = string.maketrans(intab,outrab)
        return text.translate(trantab)
    def decifrado_numeros(self,text,n): #desencrippta el valor
        intab=string.digits
        outrab = intab[ n % 10:] + intab[:n%10]
        trantab = string.maketrans(intab,outrab)
        return text.translate(trantab)
    def debitar(self,name,vlr): #Verifica el saldo para hacer el pago
        i=self.db["Nombres"].index(name)
        if self.db["Saldo"][i]>=vlr:
            self.db["Saldo"][i]=self.db["Saldo"][i]-vlr
            return "ACEPTADO"
        else:
            return "ERROR"


user_list=[] #lista de usuarios conectados
dir_user=[] #lista con ip y puerto de los usuarios
banco=Banco("10.20.30.3",6789)
thread1=Thread(target=banco.udp_handler,args=())#crea el hilo para las conexiones udp
thread1.start()#inicia el hilo para las conexiones udp
banco.start()#inicia el banco