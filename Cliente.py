import socket
from tkinter import Tk, Label, Text, Scrollbar, Entry, mainloop, Button, Menu
from tkinter.constants import DISABLED, VERTICAL, END, NORMAL, NS
import threading

class cliente():
        def __init__(self):
                self.sock = socket.socket()
                self.host = "81.184.244.85"
                self.port = 9999
                self.sock.connect((self.host, self.port))
                self.grafic()

        def grafic(self):
                self.ventana = Tk()
                self.ventana.protocol("WM_DELETE_WINDOW", "onexit") # Elimina la opción de salir para evitar errores
                self.titulo = Label(self.ventana, text = "Chat Python v1.0", font = "verdana 15 bold")
                self.textArea = Text(self.ventana, height = 30, width = 60)
                self.scroll = Scrollbar(command = self.textArea.yview, orient = VERTICAL)
                self.cajaTexto = Entry(self.ventana)

                self.menuArchivo = Menu(self.ventana)
                self.ventana.config(menu = self.menuArchivo)
                self.menuArchivo_1 = Menu(self.menuArchivo, tearoff=0)
                
                self.menuNick = Menu(self.menuArchivo, tearoff=0)
                self.menuNick_1 = Menu(self.menuNick, tearoff=0)
                
                self.ejecutar()

        def graficNickname(self):
                self.ventanaNick = Tk()
                self.tituloNick = Label(self.ventanaNick, text = "Cambiar NickName", font = "verdana 15 bold")
                self.cajaNick = Entry(self.ventanaNick)
                self.ejecutarGraficNick()

        def sendEvent(self, event):
                try:
                        data = ""
                        data = self.nick + ": " + self.cajaTexto.get().strip() + "\r\n"
                        self.insertText(data)
                        if self.cajaTexto.get() == ":quit":
                                self.insertText("Te has desconectado...\r\n")
                                self.cajaTexto.delete(0,END)
                                self.nick = ""
                                self.sock.close()
                        self.sock.send(data.encode(encoding = 'utf_8', errors = 'strict'))
                        self.cajaTexto.delete(0, END)
                except:
                        self.insertText("ERROR al enviar un mensaje desde cliente\r\n")
                        self.cajaTexto.delete(0,END)
                        self.insertText("Necesitas un nick para escribir\r\n")
                        self.cajaTexto.delete(0,END)


        def insertText(self, text):
                self.textArea.config(state = NORMAL)
                self.textArea.insert(END, text)
                self.textArea.config(state = DISABLED)

        def insertNick(self, nickname):
                self.nick = nickname
                self.insertText("Nick cambiado correctamente\r\n")
                self.cajaTexto.delete(0,END)


        def receiveData(self):
                try:
                        while(True):
                                self.insertText(self.sock.recv(1024).decode('utf_8'))
                except:
                        self.insertText("ERROR, servidor desconectado, inténtelo más tarde\r\n")
                        self.cajaTexto.delete(0, END)
                        

        def ejecutar(self):
                self.titulo.grid(row = 0, column = 0)
                self.textArea.config(state = DISABLED)
                self.textArea.grid(row = 1, column = 0)
                
                self.scroll.grid(row = 1, column = 1, sticky = NS)
                self.cajaTexto.bind('<Return>', self.sendEvent)
                self.cajaTexto.grid(row = 2, column = 0)
                
                b1=Button(self.ventana,text="Send", command = lambda:self.sendEvent(""))
                b1.grid(row = 3, column = 0)

                self.menuArchivo.add_cascade(label = "Archivo", menu = self.menuArchivo_1)
                self.menuArchivo_1.add_command(label = "Salir", command = lambda: self.ventana.withdraw() or self.sock.close())
                self.menuArchivo.add_cascade(label = "Nick", menu = self.menuNick_1)
                self.menuNick_1.add_command(label = "Establecer un nick",command = lambda: self.graficNickname())

                threading.Thread(target = self.receiveData).start()
                mainloop()

        def ejecutarGraficNick(self):
                self.tituloNick.grid(row = 0, column = 0)
                self.cajaNick.grid(row = 1, column = 0)
                
                btn_nick = Button(self.ventanaNick, text = "Establecer NickName", command = lambda: self.insertNick(self.cajaNick.get().strip()) or self.ventanaNick.withdraw())
                btn_nick.grid(row = 2, column = 0)
                mainloop()

cliente()
