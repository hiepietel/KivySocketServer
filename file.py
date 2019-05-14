import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
#from server import *
from threading import Thread
from kivy.properties import StringProperty
import socket

class MyPageLayout(BoxLayout):
    ip = "192.168.0.196"
    # ip = 'localhost'
    port = 6666
    clock = "as"

    def __init__(self, **kwargs):
        super(MyPageLayout,self).__init__(**kwargs)
        self.serv = self.server()
        print("server initialized")
        #self.sock = MySocket()
       #Thread(target=self.get_data).start()
        Thread(target=self.serverStart).start()
        self.lbl=Label(
                text=self.clock,
                size_hint=(.5, .5),
                id = "clock"
            )
        self.add_widget(self.lbl)


    def serverStart(self):
            #self.serverRun()
            #pass
            while True:
                self.serverRun()

    def server(self):
        proto = socket.getprotobyname('tcp')  # [1]
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)

        self.serv.bind((self.ip, self.port))  # [2]
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
                self.lbl.text = str(message)
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
        #pass
        return MyPageLayout()


#if __name__ == '__main__':
BoxApp().run()