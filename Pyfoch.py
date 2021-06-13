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
	filetypes=(("Pyfoch", "*.pfcf"),("Text file", "*.txt"),),title="Open a new file")

	if ruta != "":
		fichero = open(ruta, 'r')
		contenido = fichero.read()
		texto.delete(1.0,'end')
		texto.insert('insert', contenido)
		fichero.close()
		root.title(ruta + " - Pyfoch")

def guardar_como():
  global ruta
  mensaje.set("Save file as")

  fichero = FileDialog.asksaveasfile(title="Save file",mode="w", defaultextension=".pfcf")

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
    #uwu

# Configuracion de la raiz
root=Tk()
root.configure(bg='white')
root.title("Pyfoch")

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
def getLines(adress: str):
  h=open(adress,"r")
  lines=h.readlines()
  h.close()
  return lines

class Parser():
  def __init__(self,name: str ="Parser"):
    self.sep=[',']
    self.sec=['|']
    self.ski=["\""]
    self.vip=["\\"]
    self.den=["~"]
    self.name=name
  def compare(self,x: str,arr):
    k = False
    for i in arr:
      k =( k or x==i)
    return k
  def separator(self,x: str ):
    return self.compare(x,self.sep)
  def section(self,x: str):
    return self.compare(x,self.sec)
  def skip(self,x: str):
    return self.compare(x,self.ski)
  def isVip(self,x: str):
    return self.compare(x,self.vip)
  def isDeny(self,x: str):
    return self.compare(x,self.den)

def pfcfread(name: str,printYesOrNo: int =1,returnText: int =0):
  lines=getLines(name+".pfcf")
  T=""
  t=""
  code=""
  codel="" #code language
  m=0
  codem=0
  p=Parser()
  lineCount=0
  for k in lines:
    count=0
    for i in range(0,len(k)):
      j=k[i]
      if  p.isDeny(j):
        if m==2:
          m=0
        else:
          m=2
      elif  p.isVip(j):
        m=1
      elif m==2: #Comment mode on
        pass
      elif m==1: #Vip mode on
        t+=j
        m=0
      elif j=="<" or j==">":
        codem+=1
      elif codem==4:
        try:
          codef(codel,code)
          codem==0
          codel=""
          code=""
        except:
          print("Sintax error")
      elif codem==3:
        pass
      elif codem==2:
        code+=j
      elif codem==1: #Code mode on
        codel+=j
      elif p.separator(j):
        T+=t+"\n"
        t=""
      elif p.section(j):
        T+="\n"
      elif  p.skip(j):
        pass
      elif j!="\n":
        t+=j
      count+=1
    lineCount+=1
  if printYesOrNo:
    print(T)
  if returnText:
    a={T,k}
    return a
  return T

def export():
  global ruta
  mensaje.set("Export file as")
  if ".pfcf" in ruta: 
    ruta2=ruta[:-5]
		#.rstrip('f')
  T=pfcfread(ruta2,0)

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