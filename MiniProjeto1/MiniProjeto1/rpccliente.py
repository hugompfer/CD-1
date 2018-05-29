import socket
import json

# representa um cliente rpc
class RPCClient:
    idCounter = 0
    def __init__(self,host,port):
        self.client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port=port
        self.host=host
        self.online=False

    #conecta ao servidor
    def start(self):
        # Connect to server
        try:
            self.client_socket.connect((self.host, self.port))
            self.online=True
        except:
            print("Servidor offline!")
    #envia ao servidor uma notificação sobre um determinado conteudo
    def notificate(self,content):
        dicionary={
            "jsonrpc": "2.0",
            "method": content
        }
        self.client_socket.send(json.dumps(dicionary).encode())

    #codifica uma determinada informação passada por parametro
    def encode(self,information):
        if isinstance(information,(list,)):
            jsonInformation=[]
            for item in information:
                method,x,y=splitStr(item)
                extra=createDicionary(method,x,y)
                jsonInformation.append(extra)
        else:
            method, x, y= information.split(",")
            jsonInformation=createDicionary(method,x,y)
        return json.dumps(jsonInformation)

    #descodifica uma determinada informação dada por parametro
    def decode(self,information):
        decoded = json.loads(information)
        if isinstance(decoded, (list,)):
            newList = []
            for item in decoded:
                newList.append(self.singleDecode(item))
            return newList
        else:
            return self.singleDecode(decoded)

    #retorna a informação do metodo do dicionario passado
    def singleDecode(self,information):
        if "id" in information:
            if "result" in information:
                return 'Id: %s - Result: %s' % (information["id"], information["result"])
            else:
                return 'Id: %s - Erro: %s' % (information["id"], information["error"])
        return information["method"]

    #envia para o servidor a informaçao e recebe o resultado
    def sendReceive(self,information):
        self.client_socket.send(information.encode())
        received = self.client_socket.recv(1024).decode()
        return self.decode(received)

    #"apanha" os metodos desconhecidos com os seus parametros para de seguida ser enviado para o servidor os mesmos
    def __getattr__(self, item):
        def calc(*args):
            if self.online == True:
                if len(args) == 1 and isinstance(args[0], (list,)):
                    info = self.encode(args[0])
                elif len(args) == 1:
                    info = self.encode("%s,%s,%s" % (item, args[0],0))
                else:
                    info = self.encode("%s,%s,%s" % (item, args[0], args[1]))
                return self.sendReceive(info)
            else:
               return "Servidor offline!"
        return calc

    #fecha ligação ao servidor
    def close(self):
        if self.online == True:
            self.notificate("Exit")
            self.client_socket.close()
            self.online = False

#divide a informação de uma função(nome,x,y)
def splitStr(information):
    name,second=information.split("(")
    splitComma=second.split(")")
    x,y=splitComma[0].split(",")
    return name,x,y

#cria um dicionario com o metodo e parametros
def createDicionary(method,x,y):
    RPCClient.idCounter += 1
    dicionary = {
        "id": RPCClient.idCounter,
        "jsonrpc": "2.0",
        "method": method,
        "params": {
            "x": x,
            "y": y}
    }
    return dicionary





