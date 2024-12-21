import tkinter as tk
import random
from tkinter import messagebox
from tkinter import PhotoImage
from time import sleep
windows = tk.Tk()
windows.title("Campo Minato")
bandiera = "🚩"
bomba = "💣"
errore = "❌"
icon = PhotoImage(file="bomba.png")
windows.iconphoto(True, icon)
inizializzato = False


#Funzioni
def crea_griglia(righe:int, colonne:int):
    matrice = [] #Se è scoperta, che numero c'è dentro e button
    for r in range(righe):
        matrice.append([])
        for c in range(colonne):
            bottone = tk.Button(gioco,width=2,height=1, borderwidth=0)
            if (r+c)%2==0:
                bottone.config(bg="#CCEB75")
            else:
                bottone.config(bg="#A2D149")
            bottone.grid(row=r,column=c)
            bottone.bind("<Button-1>",scopri_ascoltatore) #Click SX
            bottone.bind("<Button-2>",completamento) #Click Centrale del mouse
            bottone.bind("<Button-3>",bandieratore) #Click DX
            dictionary = {
                "bottone": bottone,
                "etichetta": 0,
                "scoperta": False
            }

            matrice[r].append(dictionary)
    return matrice
    
def crea_bombe(n_bombe:int, x:int, y:int):
    global celle_da_scoprire, griglia
    righe=len(griglia)
    colonne=len(griglia[0])
    celle_da_scoprire = righe*colonne - n_bombe
    posizionate = 0
    while n_bombe != posizionate:
        r = random.randrange(righe)
        c = random.randrange(colonne)
        if griglia[r][c]["etichetta"] != -1 and (r!=x or c!=y):
            griglia[r][c]["etichetta"] = -1
           #matrice[r][c]["bottone"].config(text="B")
            posizionate+=1
    numerazione(griglia)

def scopri_ascoltatore(event):
    x = event.widget.grid_info()['row']
    y = event.widget.grid_info()['column']
    global inizializzato
    if not inizializzato:
        crea_bombe(BOMBE, x, y)
        inizializzato = True
        #timer()

    scopri(x,y)
    #print(x,y)
"""
async def timer():
    global tempo
    timer = 0
    while True:
        sleep(1)
        timer+=1
        tempo["text"] = f"⏲️: {timer}"
        tempo.update()
"""

def scopri(x:int, y:int):
    global griglia, celle_da_scoprire
    if griglia[x][y]["scoperta"]==False: #Evito di iterare una cella già scoperta
        righe=len(griglia)
        colonne=len(griglia[0])
        if griglia[x][y]["etichetta"]>=0:
            griglia[x][y]["bottone"].config(text=griglia[x][y]["etichetta"])
            griglia[x][y]["scoperta"] = True
            celle_da_scoprire-=1
        else:
            #Sconfitta
            griglia[x][y]["bottone"].config(text=bomba, bg=COLORI[random.randrange(len(COLORI))])
            sconfitta(griglia, righe, colonne)
            messagebox.showerror("Sconfitta","Hai perso!")
            exit(0)
            
        if celle_da_scoprire==0:
            vittoria(griglia,righe,colonne)
            messagebox.showinfo("Vittoria","Hai vinto!")
            exit(0)
        if griglia[x][y]["etichetta"]==0:
            griglia[x][y]["bottone"].config(text="", bg="#455c42")
            for k in range(-1,2,1):
                for l in range(-1,2,1):
                    if x+k<0 or y+l<0 or x+k>righe-1 or y+l> colonne-1: continue #Evito di andare out of index
                    else: scopri(x+k,y+l)


    

#Animazione sconfitta
def sconfitta(matrice:list, righe:int, colonne:int):
    for r in range(righe):
        for c in range(colonne):
            if matrice[r][c]["etichetta"]==-1 and matrice[r][c]["bottone"]["text"]=="":
                matrice[r][c]["bottone"].config(text=bomba, bg=COLORI[random.randrange(len(COLORI))])
                matrice[r][c]["bottone"].update()
                sleep((random.random()/2))
            elif matrice[r][c]["etichetta"]!=-1 and matrice[r][c]["bottone"]["text"]==bandiera:
                matrice[r][c]["bottone"].config(text=errore)
                matrice[r][c]["bottone"].update()
                sleep((random.random()/2))

#Animazione vittoria
def vittoria(matrice:list, righe:int, colonne:int):
    fiori = ["🌸","🌻"]
    #Tutte le caselle blu
    for r in range(righe):
        for c in range(colonne):
            if matrice[r][c]["etichetta"] >= 0:
                if (r+c)%2==0:
                    matrice[r][c]["bottone"].config(bg="#83c4f7", text="")
                else:
                    matrice[r][c]["bottone"].config(bg="#8ec9f9", text="")
                matrice[r][c]["bottone"].update()
            else:
                matrice[r][c]["bottone"].config(text="")
        sleep(0.2)
    for r in range(righe):
        for c in range(colonne):
            if matrice[r][c]["etichetta"] == -1:
                matrice[r][c]["bottone"].config(text=fiori[random.randrange(len(fiori))])
                matrice[r][c]["bottone"].update()
        sleep(0.2)
                
#Mette i numeri delle bombe adiacenti per ogni bottone
def numerazione(matrice:list):
    righe=len(matrice)
    colonne=len(matrice[0])
    for i in range(righe):
            for j in range(colonne):
                if matrice[i][j]["etichetta"]==0: #Se una bomba non è presente
                    #Contatore celle bomba
                    contatore = 0
                    for k in range(-1,2,1):
                        for l in range(-1,2,1):
                            if i+k<0 or j+l<0 or i+k>righe-1 or j+l> colonne-1: continue #Evito di andare out of index
                            elif matrice[i+k][j+l]["etichetta"] == -1: contatore+=1
                    matrice[i][j]["etichetta"] = contatore

#Scopre le celle adiacenti se e solo se ci sono tante bandierine quante il numero di bombe vicine
def completamento(event):
    global griglia
    x = event.widget.grid_info()['row']
    y = event.widget.grid_info()['column']
    if griglia[x][y]["scoperta"]: #Cella già scoperta
        bombe = griglia[x][y]["etichetta"]
        if bombe == 0: return #Inutile andare avanti se sappiamo che la cella è già stata scoperta ed è = 0
        else:
            righe=len(griglia)
            colonne=len(griglia[0])
            #Conto se ci sono abbastanza bandiere inserite
            for k in range(-1,2,1):
                for l in range(-1,2,1):
                    if x+k<0 or y+l<0 or x+k>righe-1 or y+l> colonne-1: continue #Evito di andare out of index
                    elif griglia[x+k][y+l]["bottone"]["text"] == bandiera:
                        bombe-=1
            if bombe == 0:
                for k in range(-1,2,1):
                    for l in range(-1,2,1):
                        if x+k<0 or y+l<0 or x+k>righe-1 or y+l> colonne-1: continue #Evito di andare out of index
                        else:
                            scopri(x+k,y+l) #Scopre la cella solo se tutto è a posto

#Posiziona una bandierina
def bandieratore(event):
    global bandierine, contatore_bandiere, griglia
    if griglia[event.widget.grid_info()['row']][event.widget.grid_info()['column']]["scoperta"]==False or event.widget["text"]==bandiera:
        if event.widget["text"] != bandiera:
            event.widget.config(text=bandiera)
            griglia[event.widget.grid_info()['row']][event.widget.grid_info()['column']]["scoperta"]=True
            bandierine-=1
        else:
            event.widget.config(text="")
            griglia[event.widget.grid_info()['row']][event.widget.grid_info()['column']]["scoperta"]=False
            bandierine+=1
        contatore_bandiere["text"] = f"🚩: {bandierine}"
        

#COSTANTI
RIGHE=14
COLONNE=18
BOMBE=30


COLORI = ["red", "orange", "yellow", "blue", "violet", "brown", "gray", "purple", "pink", "snow", "gold","azure", "dark green", "salmon"] #Colori per l'animazione di sconfitta

#Frame
informazioni = tk.Frame(windows)
gioco = tk.Frame(windows)
#Creazione griglia
griglia = crea_griglia(RIGHE, COLONNE)

#Contatore bandiere
bandierine = BOMBE
contatore_bandiere = tk.Label(informazioni, text=f"🚩: {bandierine}",background="green4",width=int(2.8*COLONNE))
#tempo = tk.Label(informazioni)
contatore_bandiere.pack()
#tempo.pack()
informazioni.pack()
gioco.pack()
#print(griglia)

windows.mainloop()