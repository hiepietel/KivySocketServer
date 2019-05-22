#kivy library
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.pagelayout import PageLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.graphics import *

#others library
from threading import Thread, Timer
import socket
import time

clock = str("00:00:00")

class MyPageLayout(BoxLayout):
    ip = "192.168.0.196"
    #ip = 'localhost'
    port = 6666
    clock = StringProperty
    alarmHour = -1
    alarmMinute = -1
    alarmed = False

    def __init__(self, **kwargs):
        super(MyPageLayout, self).__init__(**kwargs)
        self.alarmed = False
        self.rect = Rectangle(size=self.size, pos=self.pos)
        self.serv = self.server()
        self.orientation = "vertical"
        self.color = (1, 0, 1, 1)
        #self.sock = MySocket()
       #Thread(target=self.get_data).start()

        self.timelbl = Label(
                text=clock,
                bold=True,
                color=(1, 0, 1, 1),
                font_size="90sp",
                size_hint=(1, .5),
                id="clockLbl"
            )

        self.datelbl = Label(
                text=clock,
                bold=True,
                color=(1, 0, 1, 1),
                font_size="40sp",
                size_hint=(1, .1),
                id="clockLbll"
            )

        self.allarmlbl = Label(
                text = "Alarm not set up",
                bold = False,
                font_size="20sp",
                color=(0, 0, 0, 0),
                size_hint=(1, .3)

            )

        #self.(self.bgRect)
        self.add_widget(self.timelbl)
        self.add_widget(self.datelbl)
        self.add_widget(self.allarmlbl)
        Thread(target=self.serverStart).start()
        #Thread(1,target=self.time).start()
        Thread(target=self.time).start()

    def serverStart(self):
            #self.serverRun()
            #pass
            while True:
                self.serverRun()
    def time(self):
        while True:
            #print("clock")
            myTime = time.gmtime()
            myTime = time.localtime()
            myTimeStr = ""
            if myTime.tm_hour+2 < 10:
                myTimeStr += "0"+str(myTime.tm_hour)+":"
            else:
                myTimeStr += str(myTime.tm_hour)+":"
            if myTime.tm_min < 10:
                myTimeStr += "0"+str(myTime.tm_min)+":"
            else:
                myTimeStr += str(myTime.tm_min)+":"
            if myTime.tm_sec < 10:
                myTimeStr += "0"+str(myTime.tm_sec)
            else:
                myTimeStr += str(myTime.tm_sec)

            myDateStr = ""
            if myTime.tm_mday < 10:
                myDateStr += "0" + str(myTime.tm_mday) + "-"
            else:
                myDateStr += str(myTime.tm_mday) + "-"
            if myTime.tm_mon < 10:
                myDateStr += "0" + str(myTime.tm_mon) + "-"
            else:
                myDateStr += str(myTime.tm_mon) + "-"
            myDateStr += str(myTime.tm_year)
            #check alarm
            if self.alarmHour == myTime.tm_hour and self.alarmMinute == myTime.tm_min:
                print("alarm")
            self.timelbl.text = myTimeStr
            self.datelbl.text = myDateStr
            ##print(myTimeStr)
            time.sleep(1)

    def timee(self):
        myTime = time.gmtime()
        self.clock = str(myTime.tm_sec)

    def server(self):
        proto = socket.getprotobyname('tcp')  # [1]
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)

        self.serv.bind((self.ip, self.port))  # [2]
        self.serv.listen(1)  # [3]
        print("server initialized")
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
                #self.lbl.text = str(message)
                conn.send(b'i received: ' + message)
                if message == b'exit':
                    print("exit")
                    conn.close()
                    run = False
                    break
                if message[0] == 115 and message[1] == 97:
                    self.alarmHour = int(message[2]-48)*10 + int(message[3]-48)
                    self.alarmMinute = int(message[5]-48)*10 + int(message[6]-48)
                    print("alarm set to: "+str(self.alarmHour)+" : "+str(self.alarmMinute))
                    self.allarmlbl.text = "Alarm: "+str(int(message[2]-48)) + str(int(message[3]-48)) + " : " + str(int(message[5]-48)) + str(int(message[6]-48))
                if message == b'alarmOn':
                    self.allarmlbl.color = self.timelbl.color
                    print("alarm on")
                    self.alarmed = True
                if message == b'alarmOff':
                    self.allarmlbl.color = (0, 0, 0, 0)
                    print("alarm off")
                    self.alarmed = False
                if message == b'purple':
                    print("font color is purple")
                    self.timelbl.color = (1, 0, 1, 1)
                    self.datelbl.color = (1, 0, 1, 1)
                    if self.alarmed:
                        self.allarmlbl.color = (1, 0, 1, 1)
                if message == b'green':
                    print("font color is green")
                    self.timelbl.color = (0, 1, 0, 1)
                    self.datelbl.color = (0, 1, 0, 1)
                    if self.alarmed:
                        self.allarmlbl.color = (0, 1, 0, 1)
                if message == b'cyan':
                    print("font color is cyan")
                    self.timelbl.color = (0, 1, 1, 1)
                    self.datelbl.color = (0, 1, 1, 1)
                    if self.alarmed:
                        self.allarmlbl.color = (0, 1, 1, 1)
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
    windowWidth = 480
    windowHeight = 320
    def build(self):
        #pass
        Config.set("graphics", "borderless", 1)
        Config.set('graphics', 'width', self.windowWidth)
        Config.set('graphics', 'height', self.windowHeight)
        Config.write()
        myTime = time.gmtime()
        return MyPageLayout()


#if __name__ == '__main__':
BoxApp().run()