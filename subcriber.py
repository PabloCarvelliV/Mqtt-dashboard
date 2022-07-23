from cgitb import text
from tkinter.ttk import Treeview
from mysqlx import Column
import paho.mqtt.client as mqtt
from tkinter import *
import threading
import time
from crud import *
from tkinter import messagebox

class Subcriber:

    def __init__(self):

        self.is_conn_bt = False
        self.mensaje = StringVar()

        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_massage

        self.subWindow = Tk()
        self.subWindow.title("Herramienta de suscripción")

        self.contenedor_s = LabelFrame(self.subWindow, text="Suscriptor.")
        self.contenedor_s.grid(row=0, column=0, columnspan=3, pady=20)

        self.texto = Text(self.contenedor_s, height=12)
        self.texto.grid(row=0, column=0, columnspan=3)
        self.texto.insert(END, "")

        self.btsBorrarConsola = Button(self.contenedor_s, text="Clear", width=25, command=self.borrarConsola)
        self.btsBorrarConsola.grid(row=1, column=0, columnspan=1)

        self.contForm = LabelFrame(self.contenedor_s, text="Conexión:")
        self.contForm.grid(row=1, column=2)

        self.lbsHost = Label(self.contForm, text="Nombre del Host:")
        self.lbsHost.grid(row=0, column=0)
        self.esHost = Entry(self.contForm, width=30, borderwidth=5)
        self.esHost.grid(row=0, column=1)

        self.lbsPort = Label(self.contForm, text="Numero del puerto:")
        self.lbsPort.grid(row=1, column=0)
        self.esPort = Entry(self.contForm, width=30, borderwidth=5)
        self.esPort.grid(row=1, column=1)

        self.lbsTopic = Label(self.contForm, text="Tema:")
        self.lbsTopic.grid(row=2, column=0)
        self.esTopic = Entry(self.contForm, width=30, borderwidth=5)
        self.esTopic.grid(row=2, column=1)

        self.btsConectar = Button(self.contForm, text="Conectar", width=25, command=self.conectar)
        self.btsConectar.grid(row=3, column=1)

        # Visualizacion de brokers

        self.contenedorTabla = LabelFrame(self.subWindow, text="Tabla de conexiones.", width=30)
        self.contenedorTabla.grid(row=4, column=0, columnspan=2, pady=0)

        # Tabla

        self.table = Treeview(self.contenedorTabla, height=10, columns=('#1','#2'))
        self.table.grid(row=0, column=0, columnspan=2)
        self.table.heading('#0', text="Host name", anchor=CENTER)
        self.table.heading('#1', text="Ip", anchor=CENTER)
        self.table.heading('#2', text="Puerto", anchor=CENTER)

        self.btSeleccionar = Button(self.contenedorTabla, text="Utilizar broker", command=self.selectBroker)
        self.btSeleccionar.grid(row=1, column=0, columnspan=1)

        self.btActualizarTabla = Button(self.contenedorTabla, text="Actualizar", command=self.actualizaTabla)
        self.btActualizarTabla.grid(row=1, column=1,columnspan=1)

        self.getBroker()

        self.subWindow.mainloop()
    
    def validation(self):
        return len(self.esHost.get()) != 0 and len(self.esPort.get()) != 0 and len(self.esTopic.get()) != 0

    def conectar(self):

        if self.is_conn_bt == False:
            if self.validation():
                self.is_conn_bt = True
                self.btsConectar.config(text="Desconectar")
                self.client.connect(str(self.esHost.get()), int(self.esPort.get()), 60)
                self.client.subscribe(self.esTopic.get())
                self.client.loop_start()
            else:
                messagebox.showinfo(title="Error!", message="Introduzca todos los datos necesarios para conexion.")

        else:
            self.is_conn_bt = False
            self.btsConectar.config(text="Conectar")
            self.client.loop_stop()
            self.client.disconnect()
    
    def borrarConsola(self):
        self.texto.delete('1.0', END)

    def selectBroker(self):
        try:
            self.table.item(self.table.selection())["text"][0]
        except IndexError as e:
            self.infoSB()
            return
        ip = self.table.item(self.table.selection())["values"][0]
        self.esHost.delete(0, END)
        self.esHost.insert(END, ip)
        port = self.table.item(self.table.selection())["values"][1]
        self.esPort.delete(0, END)
        self.esPort.insert(END, port)
    
    def getBroker(self):

        cr = Crud()
        records = self.table.get_children()

        for element in records:
            self.table.delete(element)
        
        query = "SELECT * FROM brokers ORDER BY hostName DESC"
        db_rows = cr.run_query(query)

        for row in db_rows:

            self.table.insert('', 0, text=row[0], values=(row[1], row[2]))
    
    def actualizaTabla(self):
        self.getBroker()
        

    def on_connect(self, client, userdata, flags, rc):
        topic = str(self.esTopic.get())
        self.client.subscribe(topic)

    def on_massage(self, client, userdata, msg): 
        self.mensaje.set(str(msg.payload))
        self.texto.insert(END, self.mensaje.get())













