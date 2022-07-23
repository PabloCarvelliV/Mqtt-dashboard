from ast import Lambda
from tkinter.ttk import Treeview

from mysqlx import Column
from setuptools import Command
from crud import *
from tkinter import *

class GestorBrokers:

    def __init__(self):

        self.gestorWindow = Tk()
        self.gestorWindow.title("Gestor de Brokers.")

        contenedor = LabelFrame(self.gestorWindow, text="Registrar broker")
        contenedor.grid(row=0, column=0, columnspan=3, pady=20)

        # Entrada del nombre del host
        Label(contenedor, text="Nombre: ").grid(row=1, column=0)
        self.hostName = Entry(contenedor)
        self.hostName.focus()
        self.hostName.grid(row=1, column=1)

        # Entrada ip
        Label(contenedor, text="IP: ").grid(row=2, column=0)
        self.ip = Entry(contenedor)
        self.ip.grid(row=2, column=1)

        # Entrada puerto
        Label(contenedor, text="Puerto:").grid(row=3, column=0)
        self.ePort = Entry(contenedor)
        self.ePort.grid(row=3, column=1)

        # Boton de agregar broker
        self.btAdd = Button(contenedor, text="Guardar", command=self.addBroker)
        self.btAdd.grid(row=4, columnspan=2, sticky= W + E)

        # Mensaje salida
        self.mensaje = Label(self.gestorWindow, text = '', fg = "red")
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky = W + E)

        # Tabla visualizacion
        self.table = Treeview(self.gestorWindow, height=10, columns=('#1', '#2'))
        self.table.grid(row=5, column=0, columnspan=2)
        self.table.heading('#0', text="Host name", anchor=CENTER)
        self.table.heading('#1', text="IP", anchor=CENTER)
        self.table.heading('#2', text="Puerto", anchor=CENTER)
        # Botones
        self.btBorrar = Button(self.gestorWindow, text="Borrar", command=self.deleteBroker)
        self.btBorrar.grid(row=6, column=0, sticky= W + E)

        self.btEditar = Button(self.gestorWindow, text="Editar", command=self.editBroker)
        self.btEditar.grid(row=6, column=1, sticky= W + E)

        self.getBroker()
    
    def validation(self):
        return len(self.hostName.get()) != 0 and len(self.ip.get()) != 0 and len(self.ePort.get()) != 0
    
    def addBroker(self):

        cr = Crud()
        if self.validation():
            cr.add_broker(self.hostName.get(), self.ip.get(), self.ePort.get())
            del cr
        else:
            self.mensaje["text"] = "Error, El nombre, la IP son requeridos."
        
        self.getBroker()
    
    def editBroker(self):

        cr = Crud()
        self.mensaje["text"] = ''

        try:
            self.table.item(self.table.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Seleccione un broker!"
            return
        
        oldHostName = self.table.item(self.table.selection())["text"]
        oldIp = self.table.item(self.table.selection())["values"][0]
        oldPort = self.table.item(self.table.selection())["values"][1]
        self.editWindow = Toplevel()
        self.editWindow.title = "Editar broker."

        Label(self.editWindow, text= "Nombre anterior:").grid(row=0, column=1)
        Entry(self.editWindow, textvariable=StringVar(self.editWindow, value=oldHostName), state="readonly").grid(row=0, column=2)

        Label(self.editWindow, text="Nuevo nombre:").grid(row=1, column=1)
        self.newHostName = Entry(self.editWindow)
        self.newHostName.grid(row=1, column=2)
        self.newHostName.focus()

        Label(self.editWindow, text="Ip anterior:").grid(row=2, column=1)
        Entry(self.editWindow, textvariable=StringVar(self.editWindow, value= oldIp), state="readonly").grid(row=2, column=2)

        Label(self.editWindow, text="Nueva IP:").grid(row=3, column=1)
        self.newIp = Entry(self.editWindow)
        self.newIp.grid(row=3, column=2)

        Label(self.editWindow, text="Puerto anterior:").grid(row=4, column=1)
        Entry(self.editWindow, textvariable=StringVar(self.editWindow, value=oldPort), state="readonly").grid(row=4, column=2)

        Label(self.editWindow, text="Nuevo Puerto:").grid(row=5, column=1)
        self.newPort = Entry(self.editWindow)
        self.newPort.grid(row=5, column=2)

        Button(self.editWindow, text="Actualizar", command=lambda: self.editRecord(self.newHostName.get(), oldHostName, self.newIp.get(), oldIp, self.newPort.get(), oldPort)).grid(row=6, column=2, sticky= W + E)
        
    def deleteBroker(self):

        cr = Crud()
        self.mensaje["text"] = ''

        try:
            self.table.item(self.table.selection())["text"][0]
        except IndexError as e:
            self.mensaje["text"] = "Seleccione un broker!"
            return
        
        self.mensaje["text"] = ''
        hostName = self.table.item(self.table.selection())["text"]
        query = "DELETE FROM brokers WHERE hostName = ?"
        cr.run_query(query, (hostName, ))
        self.mensaje["text"] = "El broker {} ha sido eliminado.".format(hostName)
        self.getBroker()
    
    def getBroker(self):

        cr = Crud()
        records = self.table.get_children()

        for element in records:
            self.table.delete(element)
        
        query = "SELECT * FROM brokers ORDER BY hostName DESC"
        db_rows = cr.run_query(query)

        for row in db_rows:

            self.table.insert('', 0, text=row[0], values=(row[1], row[2]))
    
    def editRecord(self, newName, name, newIp, ip, newPort, port):
        if len(self.newHostName.get()) != 0 and len(self.newIp.get()) != 0 and len(self.newPort.get()) != 0:
            cr = Crud()
            cr.edit_records(newName, name, newIp, ip, newPort, port)
            self.editWindow.destroy()
            self.mensaje["text"] = "Broker {} actualizado.".format(name)
            self.getBroker()
        else:
            self.mensaje["text"] = "Cambios no guardados, todos los datos son requerido!"
            self.editWindow.destroy()
