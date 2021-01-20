from socket import *

class Cliente:
    '''Inicializa el cliente con el nombre y el socket para hacer las conexiones'''
    def __init__(self, nombre):
        self.nombre=nombre
        self.c=socket(AF_INET,SOCK_STREAM)
    '''Metodo para conectarse a la licorera, recibir los mensajes de ella y
    y recibir del teclado las opciones del usuario'''
    def conectar_licorera(self):
        self.c.connect(("127.0.0.1",1234))
        self.c.send(self.nombre)
        bienvenida=self.c.recv(1024)
        print bienvenida
        segundo=self.c.recv(1024)
        print segundo
        opciones=self.c.recv(1024)
        print opciones
        while True:
            opcion=str(input("Escriba una opcion: "))
            if opcion=="MOSTRAR":
                self.consultar_licores(opcion)
                print opciones
            elif opcion=="SALIR":
                self.c.send(opcion)
                break
            elif opcion=="COMPRAR":
                self.comprar_licor(opcion)
                print opciones
            elif opcion=="USUARIOS":
                self.consultar_usuarios(opcion)
                print opciones
        self.c.close()
    '''Metodo para pedirle a la licorera que muestre el catalogo con los licores'''
    def consultar_licores(self,opcion):
        self.c.send(opcion)
        data=self.c.recv(1024)
        print data
    '''Metodo para realizar la compra de un solo licor'''
    def comprar_licor(self,opcion):
        self.c.send(opcion)
        data=self.c.recv(1024)
        print data
        opcion=input("Seleccione una opcion: ")
        self.c.send(opcion)
        ans=self.c.recv(1024)
        print ans
    '''Metodo para realizar la consulta a la licorera de los usuarios conectados'''
    def consultar_usuarios(self,opcion):
        self.c.send(opcion)
        data=self.c.recv(1024)
        print data

'''Inicializacion del codigo'''
camilo=Cliente("Camilo")
camilo.conectar_licorera()