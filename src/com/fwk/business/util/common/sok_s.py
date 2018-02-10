import socket

port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
s.bind((host, port))

s.listen(5)
print ("listen ok")

while True:
    c, addr= s.accept()
    print ('connection', addr)
    c.send('Connection success')
    c.close()