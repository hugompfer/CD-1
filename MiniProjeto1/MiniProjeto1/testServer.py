import rpcserver
import myLib


rpcserver=rpcserver.RPCServer()
rpcserver.register(myLib.add)
rpcserver.register(myLib.div)
rpcserver.register(myLib.mul)
rpcserver.register(myLib.sub)
rpcserver.start()

