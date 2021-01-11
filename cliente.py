from socket import *

class Cliente:
    def __init__(self, nombre):
        self.nombre=nombre
        self.c=socket(AF_INET,SOCK_STREAM)
    def conectar_licorera(self):
        self.c.connect(("127.0.0.1",1234))
        bienvenida=self.c.recv(1024)
        print bienvenida
        segundo=self.c.recv(1024)
        print segundo
        opciones=self.c.recv(1024)
        print opciones
        while True:
            #data= self.c.recv(1024)
            #print data
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
        self.c.close()
    def consultar_licores(self,opcion):
        self.c.send(opcion)
        data=self.c.recv(1024)
        print data
    def comprar_licor(self,opcion):
        self.c.send(opcion)
        data=self.c.recv(1024)
        print data
        opcion=input("Seleccione una opcion: ")
        self.c.send(opcion)
        ans=self.c.recv(1024)
        print ans

camilo=Cliente("Camilo")
camilo.conectar_licorera()