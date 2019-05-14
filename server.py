import socket

ip = "192.168.0.196"
#ip = 'localhost'
port = 6666

class MySocket:

    def __init__(self,host="localhost", port=54545):
        self.serv = self.server()
        print("server initialized")
        #self.sock = socket.socket()
        #self.sock.connect((host, port))

    def server(self):
        proto = socket.getprotobyname('tcp')  # [1]
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)

        self.serv.bind((ip, port))  # [2]
        self.serv.listen(1)  # [3]
        return self.serv

    def serverRun(self):
        conn, addr = self.serv.accept()
        print("connected")
        # conn.send(b'hello') # [4]
        run = True;
        while run:
            message = conn.recv(64)
            # print(str(message))                                      # [5]
            if message:
                print("message " + str(message))
                conn.send(b'i received: ' + message)
                if message == b'exit':
                    print("exit")
                    conn.close()
                    run = False
                    break;
                if message == b'yes':
                    print("yes")
                    conn.send(b'i got yes')
                    # conn.close()
            else:
                break
            run = False
        conn.close()
        run=False

    def get_data(self):
        return self.sock.recv(1024)