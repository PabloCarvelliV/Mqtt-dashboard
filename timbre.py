from turtle import clear, title
import paho.mqtt.client as mqtt
from tkinter import *

class Timbre():

    def __init__(self):
        self.doorbellWindow = Tk()
        self.doorbellWindow.title("Timbre.")
        self.doorbellWindow.geometry("200x200")

        self.btTimbre = Button(self.doorbellWindow, text= "PLAY", command=self.playBell)
        self.btTimbre.place(x = 70, y = 70)
    
    def playBell(self):
        client = mqtt.Client()
        client.connect("10.244.132.223", 1883, 60)
        client.publish("test/timbre/use", "4")