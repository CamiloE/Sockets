from SocketServer import TCPServer, BaseRequestHandler

class handler(BaseRequestHandler):
    def mostrar(self):
        for i in range(0,3):
            msg=str(self.db["nombre"][i])+'\t\t'+'cod: '+ str(self.db["codigo"][i])+'\t\t'+str(self.db["precio"][i])+ '\t\t'+str(self.db["cantidad"][i])+' und' +'\n'
            self.request.send(msg)
    def handle(self):
        self.db={"nombre":['Aguardiente','Ron','Whiskey'],
                "codigo":[1,2,3],
                    "precio":[22000,37000,60000],
                    "cantidad":[5,5,5]}
        print "Connection from ",(self.client_address)
        bienvenida= "Bienvenido a LiquoStore, para nosotros es un gusto atenderlo\n"
        self.request.send(bienvenida)
        self.request.send("\t\tLas opciones para interactuar con nosotros son las siguientes\n")
        self.request.send("\n")
        self.opciones()
        while True:
            datos= self.request.recv(1024)
            if datos == "SALIR\r\n":
                break
            elif datos=='MOSTRAR\r\n':
                self.mostrar()
            elif datos=="COMPRAR\r\n":
                self.comprar()
            else:
                self.request.send("Lo sentimos, la opcion es invalida\n")
        self.request.close()
    def opciones(self):
        self.request.send("1)MOSTRAR: para mostrar el catalogo de licores disponibles\n")
        self.request.send("2)COMPRAR: para comprar un solo licor\n")
        self.request.send("3)SALIR: para desconectarse del servidor\n")
    def comprar(self):
        self.request.send("1) Aguardiente\n")
        self.request.send("2) Ron\n")
        self.request.send("3) Whiskey\n")
        opcion=int(self.request.recv(8))
        if opcion==1:
            self.request.send("Tenga su "+self.db["nombre"][0]+'\n')
            self.actualizar(0)
        elif opcion==2:
            self.request.send("Tenga su "+self.db["nombre"][1]+'\n')
            self.actualizar(1)
        elif opcion==3:
            self.request.send("Tenga su "+self.db["nombre"][2]+'\n')
            self.actualizar(2)
    def actualizar(self,n):
        self.db["cantidad"][n]=self.db["cantidad"][n]-1


class MyEchoServer(): 
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.server=TCPServer((self.ip,self.port),handler)
    def start(self):
        print "Waiting connection..."
        self.server.serve_forever()

servidor=MyEchoServer("127.0.0.1",1234)
servidor.start()