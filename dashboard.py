from turtle import clear, title
from urllib.error import ContentTooShortError
import paho.mqtt.client as mqtt
from tkinter import *
from tkinter import messagebox
from relays import *
from publisher import *
from subcriber import *
from gestorBrokers import *
from crud import *
from timbre import *

class Dashboard:

    def __init__(self):
        self.is_conn_bt_p = False
        self.is_conn_bt_s = False
        self.client_p = mqtt.Client()
        self.client_s = mqtt.Client()
        self.dashWindow = Tk()
        self.dashWindow.title("Mqtt-Dashboard.")
        self.dashWindow.geometry("1010x740")
        self.mensaje = StringVar()

        self.client_p.on_connect = self.on_connect_p
        self.client_s.on_connect = self.on_connect_s
        self.client_s.on_message = self.on_massage

        self.infoMsg = "Aplicacion hecha por Pablo Carvelli Vargas estudiante de segundo año de Desarrollo de Aplicaciones Multiplataforma (DAM2) Escuela Jesuites el Clot. como proyecto final de grado. 05/2022."

        # Barra de herramientas

        self.toolBar = Menu(self.dashWindow)

        self.mHerramientas = Menu(self.toolBar)

        self.mHerramientas.add_command(label="Publicador", command=self.initPublisher)
        self.mHerramientas.add_command(label="Suscriptor", command=self.initSubcriber)
        self.mHerramientas.add_separator()
        self.mHerramientas.add_command(label="Relays controller", command=self.initRelaysController)
        self.mHerramientas.add_command(label="Timbre", command=self.initDoorBell)
        self.mHerramientas.add_command(label="Acerca de...", command=self.info)
        self.mHerramientas.add_separator()
        self.mHerramientas.add_command(label="Salir", command= self.salir)

        self.toolBar.add_cascade(label="Herramientas", menu=self.mHerramientas)

        self.mConfiguracion = Menu(self.toolBar)

        self.mConfiguracion.add_command(label="Conexiones", command=self.initGestorBrokers)
        self.mConfiguracion.add_command(label="Opciones")

        self.toolBar.add_cascade(label="Configuracion", menu=self.mConfiguracion)
        self.toolBar.config(background="white")

        self.dashWindow.config(menu=self.toolBar)

        # Dashboard

        # Seccion publicador

        self.contenedor_p = LabelFrame(self.dashWindow, text="Publicador mqtt.")
        self.contenedor_p.grid(row=0, column=0, columnspan=1, pady=20)

        self.lbHost = Label(self.contenedor_p, text="Host:", width=10)
        self.lbHost.grid(row=0, column=0)
        self.eHost = Entry(self.contenedor_p, width=30, borderwidth=5)
        self.eHost.grid(row=0, column=1, columnspan=4)

        self.lbPort = Label(self.contenedor_p, text="Puerto:", width=10)
        self.lbPort.grid(row=1, column=0)
        self.ePort = Entry(self.contenedor_p, width=30, borderwidth=5)
        self.ePort.grid(row=1, column=1, columnspan=4)

        self.lbTopic = Label(self.contenedor_p, text="Topic:", width=10)
        self.lbTopic.grid(row=2, column=0)
        self.eTopic = Entry(self.contenedor_p, width=30, borderwidth=5)
        self.eTopic.grid(row=2, column=1, columnspan=4)

        self.btConectar_p = Button(self.contenedor_p, text="Conectar",width=30, command=self.conectar_p)
        self.btConectar_p.grid(row=3, column=1,columnspan=4)

        self.lbMsg = Label(self.contenedor_p, text="Mensaje")
        self.lbMsg.grid(row=4, column=0)
        self.eMsg = Entry(self.contenedor_p, width=30, borderwidth=5)
        self.eMsg.grid(row=4, column=1, columnspan=4)

        self.btSend = Button(self.contenedor_p, text="Publicar", width=30, command=self.sendMsg)
        self.btSend.grid(row=5, column=1, columnspan=4)

        self.btpUsarBrker = Button(self.contenedor_p, text="Select Broker", width=30, command=self.selectBroker)
        self.btpUsarBrker.grid(row=6, column=1, columnspan=4)

        # Suscriptor

        self.contenedor_s = LabelFrame(self.dashWindow, text="Suscriptor.")
        self.contenedor_s.grid(row=0, column=1, columnspan=1, pady=20)

        self.texto = Text(self.contenedor_s, height=12)
        self.texto.grid(row=0, column=0, columnspan=3)
        self.texto.insert(END, "")

        self.btsBorrarConsola = Button(self.contenedor_s, text="Clear", width=25, command=self.borrarConsola)
        self.btsBorrarConsola.grid(row=1, column=0, columnspan=1)

        self.btsUsarBroker = Button(self.contenedor_s, text="Broker seleccionado", width=25, command=self.selectBrokerS)
        self.btsUsarBroker.grid(row=2, column=0, columnspan=1)

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

        self.btsConectar_s = Button(self.contForm, text="Conectar", width=25, command=self.conectar_s)
        self.btsConectar_s.grid(row=3, column=1)

        # Visualizacion de brokers

        self.contenedorTabla = LabelFrame(self.dashWindow, text="Brokers añadidos.", width=30)
        self.contenedorTabla.grid(row=1, column=0, columnspan=2, pady=0)

        self.table = Treeview(self.contenedorTabla, height=10, columns=('#1','#2'))
        self.table.grid(row=0, column=0, columnspan=2)
        self.table.heading('#0', text="Host name", anchor=CENTER)
        self.table.heading('#1', text="Ip", anchor=CENTER)
        self.table.heading('#2', text="Puerto", anchor=CENTER)

        self.btActualizarTabla = Button(self.contenedorTabla, text="Actualizar", command=self.actualizaTabla)
        self.btActualizarTabla.grid(row=1, column=1,columnspan=1)

        # Loop de la ventana

        self.getBroker()

        self.dashWindow.mainloop()
    
    # Metodos

    def validation_p(self):
        return len(self.eHost.get()) != 0 and len(self.ePort.get()) != 0 and len(self.eTopic.get()) != 0

    def validation_s(self):
        return len(self.esHost.get()) != 0 and len(self.esPort.get()) != 0 and len(self.esTopic.get()) != 0

    def borrarConsola(self):
        self.texto.delete('1.0', END)

    def actualizaTabla(self):
        self.getBroker()
    
    def conectar_p(self):
        
        if self.is_conn_bt_p == False:
            if self.validation_p():
                self.is_conn_bt_p = True
                self.btConectar_p.config(text="Desconectar")
                self.client_p.connect(str(self.eHost.get()), int(self.ePort.get()), 60)
            else:
                messagebox.showinfo(title="Error!", message="Introduzca todos los datos necesarios correspondientes a la conexion del publicador.")
        else:
            self.is_conn_bt_p = False
            self.btConectar_p.config(text="Conectar")
            self.client_p.disconnect()
        
    def conectar_s(self):

        if self.is_conn_bt_s == False:
            if self.validation_s():
                self.is_conn_bt_s = True
                self.btsConectar_s.config(text="Desconectar")
                self.client_s.connect(str(self.esHost.get()), int(self.esPort.get()), 60)
                self.client_s.subscribe(self.esTopic.get())
                self.client_s.loop_start()
            else:
                messagebox.showinfo(title="Error!", message="Introduzca todos los datos necesarios correspondientes a la conexion del suscriptor.")
        else:
            self.is_conn_bt_s = False
            self.btsConectar_s.config(text="Conectar")
            self.client_s.loop_stop()
            self.client_s.disconnect()
        
    def selectBroker(self):
        try:
            self.table.item(self.table.selection())["text"][0]
        except IndexError as e:
            self.infoSB()
            return
        ip = self.table.item(self.table.selection())["values"][0]
        self.eHost.delete(0, END)
        self.eHost.insert(END, ip)
        port = self.table.item(self.table.selection())["values"][1]
        self.ePort.delete(0, END)
        self.ePort.insert(END, port)

    def selectBrokerS(self):
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

    def sendMsg(self):
        self.client_p.publish(str(self.eTopic.get()), str(self.eMsg.get()))

    def initRelaysController(self):
        relayC = Relays()
    
    def infoSB(self):
        messagebox.showinfo(title="Error!", message="Seleccione un broker!")

    def info(self):
        messagebox.showinfo(title="Acerca de...", message=self.infoMsg)
    
    def initPublisher(self):
        pub = Publisher()

    def initSubcriber(self):
        sub = Subcriber()
    
    def initGestorBrokers(self):
        gB = GestorBrokers()
    
    def initDoorBell(self):
        dbell = Timbre()
    
    def getBroker(self):

        cr = Crud()
        records = self.table.get_children()

        for element in records:
            self.table.delete(element)
        
        query = "SELECT * FROM brokers ORDER BY hostName DESC"
        db_rows = cr.run_query(query)

        for row in db_rows:

            self.table.insert('', 0, text=row[0], values=(row[1], row[2]))
    
    def salir(self):
        try:
            self.client_p.disconnect()
            self.client_s.loop_stop()
            self.client_s.disconnect()
        except IndexError as e:
            self.dashWindow.destroy()

        self.dashWindow.destroy()
    
    def on_connect_p(self, client, userdata, flags, rc):
        self.client_p.subscribe(str(self.eTopic.get()))
    
    def on_connect_s(self, client, userdata, flags, rc):
        self.client_s.subscribe(str(self.esTopic.get()))

    def on_massage(self, client, userdata, msg):
        self.mensaje.set(str(msg.payload))
        self.texto.insert(END, self.mensaje.get())
    
    