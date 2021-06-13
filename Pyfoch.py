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

def codef(codel: str,text: str): #code function
  if codel=="qiskit":
    t=qiskit(text)
  elif codel=="wolfram":
    t=wolfram(text)
  elif codel=="python":
    t=python(text)
  return t

def qiskit(text: str):
  T=""
  T+="from qiskit import QuantumCircuit, execute, Aer\n"
  T+="from qiskit.visualization import plot_histogram,display\n"
  s=0
  command=""
  param=""
  Q=0
  gate=""
  gatecount=0
  qdef=0
  for i in text:
    if i==",":
      pass
    elif s==1: #settings mode on
      if i!=" ":
        command+=i
      else:
        s=2
    elif s==2:
      if i!=" " and i!="\n":
        param+=i
      else:
        T+=qsettings(command,param)
        command=""
        param=""
        s=0
    elif i=="$":
      s=1
    elif qdef==1:
      if i=="q":
        Q+=1
      elif i=="\n":
        qdef=2
        T+="circuit=QuantumCircuit("+str(Q)+","+str(Q)+")\n"
    elif qdef==2:
      if i!="\n" and i!=" ":
        gate+=i
      elif i==" ":
        gatecount+=0.5
        T+=quantum(gate,gatecount)
        gate=""
      else:
        T+=quantum(gate,gatecount)
        gate=""
        gatecount=0
    elif i=="q":
      qdef=1
      Q+=1
  return T

def wolfram(text: str):
  T=""
  T+="from wolframclient.evaluation import WolframLanguageSession\n"
  T+="from wolframclient.language import wl, wlexpr\n"
  T+="session = WolframLanguageSession()\n"
  s=0
  command=""
  param=""
  t=""
  for i in text:
    if i==",":
      pass
    elif s==1: #settings mode on
      if i!=" ":
        command+=i
      else:
        s=2
    elif s==2:
      if i!=" " and i!="\n":
        param+=i
      else:
        T+=wsettings(command,param)
        command=""
        param=""
        s=0
    elif i=="$":
      s=1
    elif i=="\n" and t!="":
      T+="session.evaluate(wlexpr(\'"+t+"\'))\n"
      t=""
    elif i!="\n":
      t+=i
  return T

def python(text: str):
  T=""
  T+="from pyforchange.pfcf.utils import *\n"
  T+="from pyforchange.pfcf.read import *\n"
  s=0
  command=""
  param=""
  for i in text:
    if i==",":
      pass
    elif s==1: #settings mode on
      if i!=" ":
        command+=i
      else:
        s=2
    elif s==2:
      if i!=" " and i!="\n":
        param+=i
      else:
        T+=psettings(command,param)
        command=""
        param=""
        s=0
    elif i=="$":
      s=1
    else:
      T+=i
  return T

def psettings(command: str,param):
  t=""
  if command=="pfcf":
    t="executepfcf(\""+param+"\")"
  elif command=="python":
    t="execute(\""+param+"\")"
  return t

def wsettings(command: str,param):
  t=""
  if command=="inject":
    t=param+"\n"
  return t

def qsettings(command: str,param):
  t=""
  if command=="host":
    t0="s=1024\nbackend=Aer.get_backend('"+param+"')\n"
    t1="job=execute(circuit, backend, shots=s)\n"
    t2="result=job.result()\n"
    t3="counts=result.get_counts(circuit)\n"
    t=t0+t1+t2+t3
  elif command=="shots":
    t="s="+param
  elif command=="hist":
    t1="graph=plot_histogram(counts)\n"
    t2="display(graph)\n"
    t=t1+t2
  elif command=="draw":
    t="circuit.draw('mpl')\n"
  elif command=="inject":
    t=param+"\n"
  return t

def quantum(gate: str,n):
  t=""
  N=floor(n)
  n=str(N)
  T="circuit."
  if len(gate)==1:
    t=T+gate.lower()+"("+n+")\n"
  elif gate==".---X":
    t=T+"cx("+n+","+str(N+1)+")\n"
  elif gate=="X---.":
    t=T+"cx("+str(N+1)+","+n+")\n"
  else:
    number=""
    b=0
    for i in gate:
      if i!="c":
        number+=i
      else:
        b=1
    if b==1:
      t=T+"measure("+n+","+number+")\n"
  return t

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
          T+=codef(codel,code)
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