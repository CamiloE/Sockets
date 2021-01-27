from socket import *
from art import *

class Cliente:
    '''Inicializa el cliente con el nombre y el socket para hacer las conexiones'''
    def __init__(self, nombre):
        self.nombre=nombre
        #self.c=socket(AF_INET,SOCK_STREAM)
    '''Metodo para conectarse a la licorera, recibir los mensajes de ella y
    y recibir del teclado las opciones del usuario'''
    def conectar_licorera(self):#funcion para conectarse a la licorera
        self.c=socket(AF_INET,SOCK_STREAM)
        self.c.connect(("127.0.0.1",1234))
        self.c.send(self.nombre)
        bienvenida=self.c.recv(1024)
        print bienvenida
        self.c.send("OK")
        segundo=self.c.recv(1024)
        print segundo
        self.c.send("OK")
        opciones=self.c.recv(1024)
        print opciones
        while True:
            opcion=str(input("Escriba una opcion: "))
            if opcion=="MOSTRAR":
                self.consultar_licores(opcion)
                print opciones
            elif opcion=="SALIR":
                self.c.send(opcion)#cierra conexion con la licorera
                break
            elif opcion=="COMPRAR":
                self.comprar_licor(opcion)
                print opciones
            elif opcion=="USUARIOS":
                self.consultar_usuarios(opcion)
                print opciones
        self.c.close()
    '''Metodo para pedirle a la licorera que muestre el catalogo con los licores'''
    def consultar_licores(self,opcion):#FUncion para consultar el catalogo de licores
        self.c.send(opcion)
        data=self.c.recv(1024)
        print data
    '''Metodo para realizar la compra de un solo licor'''
    def comprar_licor(self,opcion):#Funcion para relizar la compra
        self.c.send(opcion)
        data=self.c.recv(1024)
        print data
        opcion=input("Seleccione una opcion: ")
        self.c.send(opcion)
        ans=self.c.recv(1024)
        if ans=="ERROR EN EL PAGO, SALDO INSUFICIENTE":
            print ans
        else:
            tprint(ans)
    '''Metodo para realizar la consulta a la licorera de los usuarios conectados'''
    def consultar_usuarios(self,opcion):#FUncion para consultar los usuarios
        self.c.send(opcion)
        data=self.c.recv(1024)
        print data
    def conectar_banco(self):#FUncion para conectarce al  banco
        self.c=socket(AF_INET,SOCK_STREAM)
        self.c.connect(("127.0.0.1",6789))
        bienvenida=self.c.recv(1024)
        print bienvenida
        self.c.send("OK")
        segundo=self.c.recv(1024)
        print segundo
        user=input()
        self.c.send(str(user))
        res1=self.c.recv(1024)
        self.c.send("OK")
        print res1
        if res1=="Usuario Valido\n":#Confirma la validacion del usuario
            tercero=self.c.recv(1024)
            print tercero
            pasw=input("Contrasena: ")
            self.c.send(str(pasw))
            conf=self.c.recv(52)
            if conf=="Ingreso Exitoso":#Confirma la contraseña
                self.c.send("OK")
                print conf
                conectado=True
                print conectado
                opciones=self.c.recv(1024)
                print opciones
                self.c.send("OK")
                menu=self.c.recv(1024)
                print menu
            else:#Si la autenticacion falla cierra la conexion con el banco
                print conf
                conectado=False
        else:#Si la autenticacion falla cierra la conexion con el banco 
            ans=self.c.recv(1024)
            print ans
            conectado=False 
        while conectado: #Interactua con el banco mientras este conectado
            opcion=str(input("Escriba una opcion: "))
            if opcion=="SALDO":
                self.consultar_saldo(opcion)
                print menu
            elif opcion=="SALIR":
                self.c.send(opcion)
                break
            elif opcion=="CONSIGNAR":
                self.consignar(opcion)
                print menu
            elif opcion=="RETIRAR":
                self.retirar(opcion)
                print menu
        print "Saliendo"
        self.c.close()#Cierra la conexion
    def consultar_saldo(self,opcion):#FUncion para consultar el saldo en el banco
        self.c.send(opcion)
        ans=self.c.recv(1024)
        print ans
    def consignar(self,opcion):#FUncion para depositar dinero en la cuenta
        self.c.send(opcion)
        ans=self.c.recv(1024)
        print ans
        vlr=input("Valor: ")
        self.c.send(vlr)
        ans2=self.c.recv(1024)
        print ans2
    def retirar(self,opcion):#FUncion para retirar dinero
        self.c.send(opcion)
        ans=self.c.recv(1024)
        print ans
        vlr=input("Monto: ")
        self.c.send(vlr)
        ans2=self.c.recv(1024)
        print ans2

'''Inicializacion del codigo'''
camilo=Cliente("camilo")
print "Hola, las opciones son las siguientes: "
while True:#ciclo para que el usuario se mantenga en el programa y escoja entre el banco y la licorera
    print "1) Conectar con la licorera"
    print "2) Conectar con el banco"
    opcion=int(input("Ingrese el numero de la opcion deseada: "))
    if opcion==1:
        camilo.conectar_licorera()
    elif opcion==2:
        camilo.conectar_banco()