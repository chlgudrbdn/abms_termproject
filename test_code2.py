
from multiprocessing.connection import Client

address = ('localhost', 6000)
conn = Client(address, authkey=b'password')
conn.send('call')
conn.send('close')
b = conn.recv()
print("b : ", b)

# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()
