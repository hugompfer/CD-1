
import rpccliente

client=rpccliente.RPCClient('127.0.0.1',8000)
client.start()

client2=rpccliente.RPCClient('127.0.0.1',8000)
client2.start()


x=client.xc(2,3)
print(x)

list= ['mul(1, a)', 'sub(2,4)', 'ads(10,2)', 'mul(4,2)']
x=client2.sdf(list)
print(x)

x=client2.add(1,2)
print(x)

x=client.sub(2,4)
print(x)

x=client2.div(10,2)
print(x)

x=client.mul(4,2)
print(x)

x=client2.mul('a', 2)
print(x)

client2.close()
client.close()

