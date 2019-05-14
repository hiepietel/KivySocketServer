from kivy.app import App
from kivy.uix.label import Label
from server import *
from threading import Thread


class MyLabel(Label):

    def __init__(self, **kwargs):
        super(MyLabel,self).__init__(**kwargs)
        self.serv = self.server()
        print("server initialized")
        #self.sock = MySocket()
       #Thread(target=self.get_data).start()
        Thread(target=self.serverStart).start()

    def serverStart(self):
            #self.serverRun()
            #pass
            while True:
                self.serverRun()

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
        while True:
            message = conn.recv(64)
            # print(str(message))                                      # [5]
            if message:
                print("message " + str(message))
                self.text = str(message)
                conn.send(b'i received: ' + message)
                if message == b'exit':
                    print("exit")
                    conn.close()
                    run = False
                    break;
                if message == b'yes':
                    print("yes")
                    conn.send(b'say yes')
                if message == b'say update':
                    print("update")
                    conn.send(b'update')
                    # conn.close()
            else:
                break
            run = False
        conn.close()
        run = False


class BoxApp(App):

    def build(self):
        return MyLabel()


if __name__ == '__main__':
    BoxApp().run()