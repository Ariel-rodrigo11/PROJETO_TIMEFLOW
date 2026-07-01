from customtkinter import *
import os
import pygame 

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
    global modo_foco, tempo_restante, timer_rodando

    if os.path.exists(Camiho_audio):
        pygame.mixer.music.load(Camiho_audio)
        pygame.mixer.music.play()

    modo_foco = not modo_foco

    if modo_foco:
        tempo_restante = 1500
        ttl.configure(text = "FOCO TOTAL!")
        camadacnt.configure(border_color ="#00BFFF")
        timer.configure(text = "25:00")
    else:
        tempo_restante = 300
        ttl.configure(text = "HORA DA PAUSA")
        camadacnt.configure(border_color ="#10B981")
        timer.configure(text = "5:00")

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

    ttl.configure(text="STUDY FLASH")
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
    text="TIME FLOW",
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