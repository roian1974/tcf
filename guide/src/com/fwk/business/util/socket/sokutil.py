import sys
import socket
import select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096 * 10
PORT = 9009

def TP_server():
    tp_srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tp_srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tp_srv_socket.bind((HOST, PORT))
    tp_srv_socket.listen(10)

    SOCKET_LIST.append(tp_srv_socket)

    print ("Chat server started on port " + str(PORT))

    while 1:

        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
            # a new connection request recieved
            if sock == tp_srv_socket:
                sockfd, addr = tp_srv_socket.accept()

                SOCKET_LIST.append(sockfd)
                print ("Client (%s, %s) connected" % addr)

            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # ---------------------------------------------------------------------------------------------
                        # TCF_SP_commo
                        # ---------------------------------------------------------------------------------------------
                        sock.send(data)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        # exception
                except:
                    continue

    tp_srv_socket.close()


def SOKsendrecv(ip,port,message):
    host = socket.gethostname()
    port = port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(message)
    data = s.recv(1024*30)
    s.close()
    return data

print(SOKsendrecv('localhost',9009,b'aaaaaaaaaaaaaaa'))


