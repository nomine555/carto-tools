import tkinter as tk

class zoneDialog:
    def __init__(self, parent, titulo, zonas):        
                
        self.cvar1 = tk.BooleanVar()
        self.cvar2 = tk.BooleanVar()
        self.cvar3 = tk.BooleanVar()
        self.cvar4 = tk.BooleanVar()
        self.cvar5 = tk.BooleanVar()
        self.cvar1.set(zonas[0])
        self.cvar2.set(zonas[1])
        self.cvar3.set(zonas[2])
        self.cvar4.set(zonas[3])
        self.cvar5.set(zonas[4])
        
        top = self.top = tk.Toplevel(parent)
        top.title("Secuenciando Visitags...")
        self.myLabel = tk.Label(top, text=titulo)
        self.myLabel.pack(ipadx=30, ipady=6)
                
        self.chkframe = tk.Frame(top)
        self.chkframe.pack( side = tk.TOP )

        self.c1 = tk.Checkbutton(self.chkframe, text='z0',variable=self.cvar1, onvalue=1, offvalue=0, command=lambda:self.toggle(self.cvar1))
        self.c1.pack(side = tk.LEFT, ipadx=10, ipady=6)
        self.c2 = tk.Checkbutton(self.chkframe, text='z1',variable=self.cvar2, onvalue=1, offvalue=0, command=lambda:self.toggle(self.cvar2))
        self.c2.pack(side = tk.LEFT, ipadx=10, ipady=6)
        self.c3 = tk.Checkbutton(self.chkframe, text='z2',variable=self.cvar3, onvalue=1, offvalue=0, command=lambda:self.toggle(self.cvar3))
        self.c3.pack(side = tk.LEFT, ipadx=10, ipady=6)
        self.c4 = tk.Checkbutton(self.chkframe, text='z3',variable=self.cvar4, onvalue=1, offvalue=0, command=lambda:self.toggle(self.cvar4))
        self.c4.pack(side = tk.LEFT, ipadx=10, ipady=6)
        self.c5 = tk.Checkbutton(self.chkframe, text='z4',variable=self.cvar5, onvalue=1, offvalue=0, command=lambda:self.toggle(self.cvar5))
        self.c5.pack(side = tk.LEFT, ipadx=10, ipady=6)

    
        if zonas[0]:
            self.c1.toggle()
        if zonas[1]:            
            self.c2.toggle()
        if zonas[2]:
            self.c3.toggle()
        if zonas[3]:
            self.c4.toggle()
        if zonas[4]:
            self.c5.toggle()

        self.aceptarButton = tk.Button(top, text='Aceptar', command=self.aceptar)
        self.aceptarButton.pack(side = tk.LEFT,padx=20, pady=16)
        
        self.descartarButton = tk.Button(top, text='Reintentar', command=self.descartar)
        self.descartarButton.pack(side = tk.LEFT,padx=20, pady=16)
        
        self.revisionButton = tk.Button(top, text='Marcar para Revisión', command=self.revisar)
        self.revisionButton.pack(side = tk.LEFT,padx=20, pady=16)        

    def aceptar(self):
        self.checkresult = True
        self.top.destroy()
        
    def revisar(self):      
        self.checkresult = None
        self.top.destroy()
        
    def descartar(self):       
        self.checkresult = False
        self.top.destroy()
        
    def toggle(self, var):
        #var.set(not var.get())  
        print(var.get())


'''
root = tk.Tk()
root.withdraw()

zonas = [True, True, True, True, True]

inputDialog = zoneDialog(root, "¿Aceptar Secuencia de tags?",zonas)
root.wait_window(inputDialog.top)
#print(inputDialog.checkresult)
print(inputDialog.cvar1.get())
print(inputDialog.cvar2.get())
print(inputDialog.cvar3.get())
print(inputDialog.cvar4.get())
print(inputDialog.cvar5.get())
'''