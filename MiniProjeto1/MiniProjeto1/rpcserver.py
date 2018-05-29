import socket
import json
import _thread
from socket import timeout

# representa um servidor rpc
class RPCServer:
    def __init__(self):
        self.methods={}
        self.port=8000
        self.host='0.0.0.0'

    #regista uma função na lista de funções
    def register(self,function):
        self.methods[function.__name__ ]=function

    #cria um json para notificação
    def notificate(self,content):
        dicionary={
            "jsonrpc": "2.0",
            "method": content
        }
        return json.dumps(dicionary)

    #cria um dicionario com o id e o resultado
    def createDicionary(str,result, id):
        dicionary = {
            "id": id,
            "jsonrpc": "2.0",
            "result": result
        }
        return dicionary

    def createError(self,code,message,id):
        error={
            "jsonrpc": "2.0",
            "error": {
                "code":code,
                "message":message
            },
            "id":id
        }
        return error

    #verifica se o metodo existe na lista de metodos
    def isValidMethod(self,method):
        if method in self.methods:
            return True
        return False

    #verifica se o metodo é de "saida"
    def isExit(self,method):
        if method == "Exit":
            return True
        return  False

    #retorna o dicionario com a resposta ao pedido pretendido
    def getInformation(self,dicionary):
        method = dicionary["method"]
        if self.isValidMethod(method):
            if isLetter(dicionary) == True:
                return self.createError(-32600,"Parametros Inválidos", dicionary["id"])
            x, y = isLetter(dicionary)
            return self.createDicionary(self.methods[method](x, y), dicionary["id"])
        else:
            return self.createError(-32600,"Metodo desconhecido",dicionary["id"])

    #Descodifica a informação recebida por parametro
    def decode(self,information):
        decoded=json.loads(information)
        if isinstance(decoded, (list,)):
            jsonInformation = []
            for item in decoded:
                jsonInformation.append(self.getInformation(item))
            return json.dumps(jsonInformation)
        else:
            if self.isExit(decoded["method"]):
                return "Exit"
            return json.dumps(self.getInformation(decoded))

    # cria um socket de servidor
    def createServerSocket(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        server_socket.settimeout(10)
        return server_socket

    # inicia a escuta de clientes
    def start(self):
        # Create socket
        server_socket=self.createServerSocket()
        print('Listening on port %s ...' % self.port)

        try:
            while True:
                # Wait for client connections
                client_connection, client_address = server_socket.accept()
                client_connection.settimeout(10)
                _thread.start_new_thread(self.listenClient, (client_connection,))
        except timeout:
            # Close socket
            server_socket.close()
            print('Servidor encerrado!')

    #inicia a escuta de mensagens de um cliente
    def listenClient(self,client_connection):
        while True:
            # Print message from client
            msg = client_connection.recv(1024).decode()
            print('Received:', msg)
            try:
                result = self.decode(msg)
                if result != "Exit":
                    client_connection.send(result.encode())
                else:
                    break
            except:
                client_connection.send(self.notificate("Erro!").encode())
        client_connection.close()

#verifica se os parametros do dicionario sao letras
def isLetter(decoded):
    x = decoded["params"]["x"]
    y = decoded["params"]["y"]

    try:
        value = int(x)
        value2=int(y)
        return value,value2
    except ValueError:
        return True