from multiprocessing.connection import Client
from turtle import clear, title
import paho.mqtt.client as mqtt
from tkinter import *
from tkinter import messagebox

from paramiko import HostKeys

class Relays:

    def __init__(self):
        self.is_onR1 = False
        self.is_onR2 = False
        self.is_onR3 = False
        self.is_onR4 = False
        self.is_onAll = False

        self.host = "10.244.132.223"
        self.puerto = 1883
        self.timeC = 60

        self.relayWindow = Tk()
        self.relayWindow.title("Relay controller")
        self.relayWindow.geometry("400x300")

        self.lblR1 = Label(self.relayWindow, text="Rele 1:")
        self.lblR1.grid(row=0, column=0, columnspan=1)
        self.botonR1 = Button(self.relayWindow, text="OFF", command=self.botonR1, width=20)
        self.botonR1.grid(row=0, column=1, columnspan=1)

        self.lblR2 = Label(self.relayWindow, text="Relay 2:")
        self.lblR2.grid(row=1, column=0, columnspan=1)
        self.botonR2 = Button(self.relayWindow, text="OFF", command=self.botonR2, width=20)
        self.botonR2.grid(row=1, column=1, columnspan=1)

        self.lblR3 = Label(self.relayWindow, text="Relay 3:")
        self.lblR3.grid(row=2, column=0, columnspan=1)
        self.botonR3 = Button(self.relayWindow, text="OFF", command=self.botonR3, width=20)
        self.botonR3.grid(row=2, column=1, columnspan=1)

        self.lblR4 = Label(self.relayWindow, text="Relay 4:")
        self.lblR4.grid(row=3, column=0, columnspan=1)
        self.botonR4 = Button(self.relayWindow, text="OFF", command=self.botonR4, width=20)
        self.botonR4.grid(row=3, column=1, columnspan=1)

        self.lblAll = Label(self.relayWindow, text="Todos los Relés:")
        self.lblAll.grid(row=4, column=0, columnspan=1)
        self.botonAll = Button(self.relayWindow, text="OFF", command=self.botonAll, width=30)
        self.botonAll.grid(row=5, column=1, columnspan=1)

        self.relayWindow.mainloop()

    def botonR1(self):

        if self.is_onR1 == False:
            self.botonR1.config(text="ON")
            self.is_onR1 = True
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay/one", "ON")
            client_p.disconnect()

        elif self.is_onR1:
            self.botonR1.config(text="OFF")
            self.is_onR1 = False
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay/one", "OFF")
            client_p.disconnect()

    def botonR2(self):

        if self.is_onR2 == False:
            self.botonR2.config(text="ON")
            self.is_onR2 = True
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay/two", "ON")
            client_p.disconnect()

        elif self.is_onR2:
            self.botonR2.config(text="OFF")
            self.is_onR2 = False
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay/two", "OFF")
            client_p.disconnect()
    
    def botonR3(self):

        if self.is_onR3 == False:
            self.botonR3.config(text="ON")
            self.is_onR3 = True
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay/three", "ON")
            client_p.disconnect()

        elif self.is_onR3:
            self.botonR3.config(text="OFF")
            self.is_onR3 = False
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay/three", "OFF")
            client_p.disconnect()
    
    def botonR4(self):

        if self.is_onR4 == False:
            self.botonR4.config(text="ON")
            self.is_onR4 = True
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay/four", "ON")
            client_p.disconnect()

        elif self.is_onR4:
            self.botonR4.config(text="OFF")
            self.is_onR4 = False
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay/four", "OFF")
            client_p.disconnect()
    
    def botonAll(self):

        if self.is_onAll == False:
            self.botonAll.config(text="ON")
            self.is_onAll = True
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay", "ON")
            client_p.disconnect()

        elif self.is_onAll:
            self.botonAll.config(text="OFF")
            self.is_onAll = False
            client_p = mqtt.Client()
            client_p.connect(self.host, self.puerto, self.timeC)
            client_p.publish("test/relay", "OFF")
            client_p.disconnect()
    
    
