import customtkinter as ct
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import DB.conn as bd
import pagamentos as PAG
import recebimentos as REC
from PIL import Image
   

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        
        conn = bd.Conexao()
        if (conn.conexao() != None):
            conn.criar_tabelas()
        

        self.protocol("WM_DELETE_WINDOW", self.confirmar_fechar_janela)

        self.title("Sistema de contas a pagar e receber")
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        self.geometry(f"{largura_tela}x{altura_tela}+0+0")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # carrega imagens
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.logo_image = ct.CTkImage(Image.open(os.path.join(image_path, "logo.png")), size=(26, 26))
        self.logo_pagar = ct.CTkImage(Image.open(os.path.join(image_path, "pagar.png")), size=(20, 20))
        self.logo_receber = ct.CTkImage(Image.open(os.path.join(image_path, "receber.png")), size=(20, 20))

        # cria frame de navegação
        self.navigation_frame = ct.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)
        self.navigation_frame_label = ct.CTkLabel(self.navigation_frame, text="  Controle Financeiro", image=self.logo_image, compound="left", font=ct.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        
        # botão navegação do pagamento
        self.button_pagamento = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Pagamentos",fg_color="transparent", 
                                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=self.logo_pagar, anchor="w", command=self.button_pagagamento_event)
        self.button_pagamento.grid(row=1, column=0, sticky="ew")   
        
         # botão navegação do recebimento
        self.button_recebimentos = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Recebimentos",fg_color="transparent", text_color=("gray10", "gray90"), 
                                                           hover_color=("gray70", "gray30"),image=self.logo_receber, anchor="w", command=self.button_recebimento_event)
        self.button_recebimentos.grid(row=2, column=0, sticky="ew")    

        self.rct = REC.Recebimentos()
        self.pg = PAG.Pagamentos()
        
        # frame pagamento
        self.frame_pagamento = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_pagamento.grid_columnconfigure(2, weight=1)
        
       # frame recebimento
        self.frame_recebimento = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_recebimento.grid_columnconfigure(2, weight=1)   
           
        # default frame
        self.select_frame_by_name("pagar")
        ct.set_appearance_mode("Dark")   
        
    def confirmar_fechar_janela(self):
        resposta = messagebox.askokcancel("Confirmação", "Deseja realmente sair?")
        if resposta:
            self.destroy()  # Fecha a janela se o usuário confirmar             
        
    def button_pagagamento_event(self):
        self.select_frame_by_name("pagar")    
        
    def button_recebimento_event(self):
        self.select_frame_by_name("receber")             
        
    def select_frame_by_name(self, name):
        self.button_pagamento.configure(fg_color=("gray75", "gray25") if name == "pagar" else "transparent")
        self.button_recebimentos.configure(fg_color=("gray75", "gray25") if name == "receber" else "transparent")

        if name == "pagar":
            self.pg.pagar(self.frame_pagamento)
            self.frame_pagamento.grid(row=0, column=1, sticky="nsew")
        else:
            self.frame_pagamento.grid_forget()
        if name == "receber":
            self.rct.receber(self.frame_recebimento)  
            self.frame_recebimento.grid(row=0, column=1, sticky="nsew")
        else:
            self.frame_recebimento.grid_forget()     
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()        
    