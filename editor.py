'''
This code is based on the code from 
https://docs.hektorprofe.net/python/interfaces-graficas-con-tkinter/editor-de-texto/
'''

from tkinter import *
from tkinter import filedialog as FileDialog
from io import open

ruta = "" # La utilizaremos para almacenar la ruta del fichero

def nuevo():
    global ruta
    mensaje.set("New file")
    ruta = ""
    texto.delete(1.0, "end")
    root.title("Pyfoch")

def abrir():
    global ruta
    mensaje.set("Open file")
    ruta = FileDialog.askopenfilename(
        initialdir='.', 
        filetypes=(("Pyfoch", "*.pfcf"),("Text file", "*.txt"),),
        title="Open a new file")

    if ruta != "":
        fichero = open(ruta, 'r')
        contenido = fichero.read()
        texto.delete(1.0,'end')
        texto.insert('insert', contenido)
        fichero.close()
        root.title(ruta + " - Pyfoch")

def guardar():
    mensaje.set("Save file")
    if ruta != "":
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("File saved succesfully")
    else:
        guardar_como()

def guardar_como():
    global ruta
    mensaje.set("Save file as")

    fichero = FileDialog.asksaveasfile(title="Save file", mode="w", defaultextension=".pfcf")

    if fichero is not None:
        ruta=fichero.name
        contenido=texto.get(1.0,'end-1c')
        fichero=open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("File saved succesfully")
    else:
        mensaje.set("Save canceled")
        ruta = ""


# Configuracion de la raiz
root=Tk()
root.configure(bg='white')
root.title("Pyfoch")
root.iconbitmap('/icon.ico')

# File Menu
menubar=Menu(root)
filemenu=Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=nuevo)
filemenu.add_command(label="Open", command=abrir)
filemenu.add_command(label="Save", command=guardar)
filemenu.add_command(label="Save as", command=guardar_como)
filemenu.add_separator()


'''
This code is mine:
'''
import pyforchange.pfcf.read as pfcf

def export():
  global ruta
  mensaje.set("Export file as")

  if ".pfcf" in ruta: 
    ruta2=ruta[:-5]
    #.rstrip('f')
  T=pfcf.read(ruta2,0)

  fichero = FileDialog.asksaveasfile(title="Save file", mode="w", defaultextension=".txt")

  if fichero is not None:
        ruta=fichero.name
        contenido=T
        fichero=open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("File saved succesfully")
    else:
        mensaje.set("Save canceled")
        ruta = ""

#Tools Menu
filemenu.add_command(label="Export", command=export)
'''
This code is based on the code from 
https://docs.hektorprofe.net/python/interfaces-graficas-con-tkinter/editor-de-texto
'''

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(menu=filemenu, label="File")

# Caja de texto central
texto=Text(root)
texto.pack(fill="both", expand=1)
texto.config(bd=0, padx=6, pady=4, font=("Consolas",12))

# Monitor inferior
mensaje = StringVar()
mensaje.set("Welcome to Pyfoch")
monitor = Label(root, textvar=mensaje, justify='left')
monitor.pack(side="left")

root.config(menu=menubar)
# Finalmente bucle de la aplicacion
root.mainloop()

'''
This code is mine:
'''