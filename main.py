from customtkinter import *
from notifypy import Notify
import os
import pygame 
from PIL import Image, ImageTk
import ctypes

# Caminho global do PNG para evitar repetição
caminho_png = os.path.join(os.path.dirname(__file__), "Icone.png")

#------------
#Notificação
#------------
descanso = 0

foco = 0

#Notificação de  descanso
noti_descanso = Notify()
noti_descanso.title = "Hora do descanso"
if os.path.exists(caminho_png):
    noti_descanso.icon = caminho_png

#Notificação de foco
noti_foco = Notify()
noti_foco.title = "Hora do foco!"
if os.path.exists(caminho_png):
    noti_descanso.icon = caminho_png

#-----------------------------------
#Audio do negócio lá, tô com sono...
#-----------------------------------

#inicia o tocador do audio
pygame.mixer.init()

Camiho_audio = os.path.join(os.path.dirname(__file__), "[Efeito Sonoro] Sinos - Brilhante.mp3")

#Variáveis de controle

timer_rodando = False
modo_foco = True
tempo_restante = 1500
id_timer = None

#----------------------
#Funções para os botões
#----------------------

#Troca os botões stop e start
def alternar_timer():
    global timer_rodando, id_timer

    if not timer_rodando:
        timer_rodando = True
        botão1.configure(
            text="Pause ⏸",
            fg_color="#FF9F1C",
            hover_color="#E68A1F"
        )
        atualizar_relogio()
    else:
        timer_rodando = False

        botão1.configure(
            text="Start ▶",
            fg_color="#1E2530",
            hover_color="#0099CC"
        )
        if id_timer: 
            app.after_cancel(id_timer)

#Faz o Relógio funcionar
def atualizar_relogio():
    global timer_rodando, tempo_restante, id_timer
    
    if timer_rodando and tempo_restante >0:
        tempo_restante = tempo_restante - 1

        minutos = tempo_restante // 60
        segundos = tempo_restante % 60
        timer.configure(text = f"{minutos:02d}:{segundos:02d}")

        id_timer = app.after(1000, atualizar_relogio)
    elif tempo_restante == 0:
        proxima_fase()

#Ativa o modo de descanso
def proxima_fase():
    global modo_foco, tempo_restante, timer_rodando, foco, descanso

    if os.path.exists(Camiho_audio):
        pygame.mixer.music.load(Camiho_audio)
        pygame.mixer.music.play()

    modo_foco = not modo_foco

    if modo_foco:
        tempo_restante = 1500
        ttl.configure(text = "FOCO TOTAL!")
        camadacnt.configure(border_color ="#00BFFF")
        timer.configure(text = "25:00")

        descanso = descanso + 1

        #notificação foco
        noti_foco.message = f"Foco Total! \n ciclos de descanso {descanso}."
        noti_foco.send()

    else:
        tempo_restante = 300
        ttl.configure(text = "HORA DA PAUSA")
        camadacnt.configure(border_color ="#10B981")
        timer.configure(text = "5:00")

        foco = foco + 1

        #Notificação descanso
        noti_descanso.message = f"aperte o play para contabilizar o seu descanso \n ciclos de foco: {foco}"
        noti_descanso.send()

    timer_rodando = False
    botão1.configure(
        text="Start ▶",
        fg_color="#1E2530",
        hover_color="#0099CC"
    )

#Limpa o token e reseta o timer completamente
def resetar_timer():
    global timer_rodando, modo_foco, tempo_restante, id_timer
    
    timer_rodando = False
    
    if id_timer:
        app.after_cancel(id_timer)
    
    pygame.mixer.music.stop()
    
    modo_foco = True
    tempo_restante = 1500
    
    #reinicia os ciclos
    foco -= foco

    descanso -= descanso

    ttl.configure(text="Time Flow")
    camadacnt.configure(border_color="#00BFFF")
    timer.configure(text="25:00")
    botão1.configure(
        text="Start ▶",
        fg_color="#1E2530",
        hover_color="#0099CC"
    )

#----------------
#INTERFACE VISUAL
#----------------
#Configs do app
app = CTk()
app.title("Time Flow")
app.geometry("390x844")

# ---- CONFIGURAÇÃO DE ÍCONE MULTIPLATAFORMA ----
caminho_ico = os.path.join(os.path.dirname(__file__), "Icone.ico")
caminho_png = os.path.join(os.path.dirname(__file__), "Icone.png") #PNG original de alta qualidade

# 1. Se for Windows, aplica a nitidez DPI e o arquivo .ico
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    if os.path.exists(caminho_ico):
        app.iconbitmap(caminho_ico)
except:
    # 2. Se falhar ou estiver no Linux/Mac, o método para PNG com boa qualidade
    if os.path.exists(caminho_png):
        img_original = Image.open(caminho_png)
        # Cria uma versão nítida para a barra do Linux
        img_barra = img_original.resize((32, 32), Image.Resampling.LANCZOS)
        
        ico_alta = ImageTk.PhotoImage(img_original)
        ico_baixa = ImageTk.PhotoImage(img_barra)
        
        app.wm_iconphoto(True, ico_alta, ico_baixa)

app._set_appearance_mode("system")
app.resizable(False,False)
app.configure(fg_color="#1E2530")

#Camada de título
camada_ttl = CTkFrame(
    app,
    fg_color="transparent",
    height=40,
)
camada_ttl.pack(fill="x", pady=(10, 20))

#Camadas de trabalho
camadacnt = CTkFrame(
    app,
    fg_color="transparent", 
    width= 325, 
    height= 325, 
    border_color="#00BFFF",
    border_width=8,
    corner_radius=200
    )
camadacnt.pack(padx = 0, pady=(40,40))
camadacnt.pack_propagate(False)

camada_botoes = CTkFrame(
    app,
    fg_color="#1E2530",
    border_color="#2D3748",
    border_width=3,
    width= 350, 
    height= 200,
)
camada_botoes.pack_propagate(False)
camada_botoes.pack()

#Raio dos botões 


botão1 = CTkButton(
    camada_botoes,
    text="Start ▶",
    font=("arial",25,"bold"),
    text_color="#F9FAFB",
    fg_color="#1E2530",
    border_color="#2D3748",
    border_width=3,
    width=325,
    height=85,
    hover_color="#0099CC",
    corner_radius= 15,
    command= alternar_timer
)
botão1.pack(pady=(10,0))

botão2 = CTkButton(
    camada_botoes,
    text="Reset ↻",
    font=("arial",25,"bold"),
    text_color="#F9FAFB",
    fg_color="#10B981",
    border_color="#2D3748",
    border_width=3,
    width=325,
    height=85,
    hover_color="#0C936A",
    corner_radius= 15,
    command=resetar_timer
)
botão2.pack(pady=(10,10))

#label de Título
ttl = CTkLabel(
    camada_ttl,
    text="MODO FOCO",
    font=("arial", 30,"bold"),
    text_color="#F9FAFB"
)
ttl.pack()

timer = CTkLabel(
    camadacnt,
    text="25:00",
    font=("arial", 60,"bold"),
    text_color="#F9FAFB",
)
timer.place(relx=0.5, rely=0.5, anchor="center")

app.mainloop()