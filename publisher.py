from tkinter.ttk import Treeview
from turtle import clear, title
import paho.mqtt.client as mqtt
from tkinter import *
from tkinter import messagebox
from crud import *

class Publisher:

    def __init__(self):

        self.client = mqtt.Client()
        self.is_conn_bt = False

        self.pubWindow = Tk()
        self.pubWindow.title("Herramienta de publicación.")
        self.pubWindow.geometry("620x500")

        self.etiquetaHost = Label(self.pubWindow, text="Host:", width=10)
        self.etiquetaHost.grid(row=0, column=0)
        self.entradaHost = Entry(self.pubWindow, width=30, borderwidth=5)
        self.entradaHost.grid(row=0, column=1, columnspan=4)

        self.etiquetaPort = Label(self.pubWindow, text="Puerto: ", width=10)
        self.etiquetaPort.grid(row = 1, column=0)
        self.entradaPort = Entry(self.pubWindow, width=30, borderwidth=5)
        self.entradaPort.grid(row=1, column=1, columnspan=4)

        self.etiquetaTopic = Label(self.pubWindow, text="Topic:", width=10)
        self.etiquetaTopic.grid(row=2, column=0)
        self.entradaTopic = Entry(self.pubWindow, width=30, borderwidth=5)
        self.entradaTopic.grid(row=2, column=1, columnspan=4)

        self.btConectar = Button(self.pubWindow, text="Conectar", command=self.conectar, width=30)
        self.btConectar.grid(row=3,column=1, columnspan=4)


        self.etiquetaMsg = Label(self.pubWindow, text="Msg: ", width=10)
        self.etiquetaMsg.grid(row=4, column=0)
        self.entradaMsg = Entry(self.pubWindow, width=30, borderwidth=5)
        self.entradaMsg.grid(row=4, column=1, columnspan=4)

        self.boton = Button(self.pubWindow, text="Enviar", command=self.sendMsg, width=30)
        self.boton.grid(row=5, column=1, columnspan=4)

        # Visualizacion de brokers

        self.contenedorTabla = LabelFrame(self.pubWindow, text="Tabla de conexiones.", width=30)
        self.contenedorTabla.grid(row=6, column=0, columnspan=2, pady=0)

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

        self.pubWindow.mainloop()
    
    def validation(self):
        return len(self.entradaHost.get()) != 0 and len(self.entradaPort.get()) != 0 and len(self.entradaTopic.get()) != 0
    
    def conectar(self):
        if self.is_conn_bt == False:
            if self.validation():
                self.is_conn_bt = True
                self.client.connect(str(self.entradaHost.get()), int(self.entradaPort.get()), 60)
                self.btConectar.config(text="Desconectar")
            else:
                messagebox.showinfo(title="Error!", message="Introduzca todos los datos necesarios para conexion.")
        
        else:
            self.is_conn_bt = False
            self.btConectar.config(text="Conectar")
            self.client.disconnect()
    
    def sendMsg(self):
        
        self.client.publish(str(self.entradaTopic.get()), str(self.entradaMsg.get()))
    
    def selectBroker(self):
        try:
            self.table.item(self.table.selection())["text"][0]
        except IndexError as e:
            self.infoSB()
            return
        ip = self.table.item(self.table.selection())["values"][0]
        self.entradaHost.delete(0, END)
        self.entradaHost.insert(END, ip)
        port = self.table.item(self.table.selection())["values"][1]
        self.entradaPort.delete(0, END)
        self.entradaPort.insert(END, port)
    
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

    def infoSB(self):
        messagebox.showinfo(title="Error!", message="Seleccione un broker!")
