import customtkinter as ct
import tkinter as tk
import os
import pagamentos as PAG
import recebimentos as REC
import organizacao as ORG
from Utils import formatacao
from infra.repository.usuarios_repository import UsuariosRepository
from tkinter import messagebox
from PIL import Image

class App(ct.CTk):
    def __init__(self):
        super().__init__()
        self.format = formatacao.Util()   
        
        self.protocol("WM_DELETE_WINDOW", self.confirmar_fechar_janela)

        self.title("Sistema de contas a pagar e receber")
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()
        self.geometry(f"{largura_tela}x{altura_tela}+0+0")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # carrega imagens
        self.image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.logo_image = ct.CTkImage(Image.open(os.path.join(self.image_path, "logo.png")), size=(26, 26))
        self.logo_pagar = ct.CTkImage(Image.open(os.path.join(self.image_path, "pagar.png")), size=(20, 20))
        self.logo_receber = ct.CTkImage(Image.open(os.path.join(self.image_path, "receber.png")), size=(20, 20))

        # cria frame de navegação
        self.navigation_frame = ct.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)
        
        self.navigation_frame_label = ct.CTkLabel(self.navigation_frame, text="  Controle Financeiro", image=self.logo_image, compound="left", font=ct.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=5) 

        ct.set_appearance_mode("Dark")
        
        self.email = ""
        self.login()
        
    def login(self):
        
        self.ctk_entry_var_email = tk.StringVar()
        self.ctk_entry_var_senha = tk.StringVar()
        self.ctk_entry_var_senha.set('123456')
        self.ctk_entry_var_email.set('admin@admin.com')
        # frame login
        frame_login = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        frame_login.grid_columnconfigure(1, weight=1)
        frame_login.grid(row=0, column=1, sticky="nsew")

        titulo_login = ct.CTkLabel(frame_login, text="Faça login para continuar", compound="left", font=ct.CTkFont(size=25, weight="bold"))
        titulo_login.grid(row=0, column=1, padx=5, pady=50, sticky="n")
        
        lblEmail = ct.CTkLabel(frame_login, text="Email", compound="left", font=ct.CTkFont(size=14, weight="bold"))
        lblEmail.grid(row=1, column=1, padx=5, pady=1, sticky="n")          
        
        inpEmail = ct.CTkEntry(frame_login, textvariable=self.ctk_entry_var_email, height=30, width=400, placeholder_text="Entre com email")
        inpEmail.grid(row=2, column=1, padx=5, pady=1, sticky="n") 
        inpEmail.tabindex = 2
        inpEmail.bind("<Tab>", self.format.mover_foco)
        #inpEmail.bind("<Return>", self.verificar_login)
        
        lblSenha = ct.CTkLabel(frame_login, text="Senha", compound="left", font=ct.CTkFont(size=14, weight="bold"))
        lblSenha.grid(row=3, column=1, padx=5, pady=1, sticky="n")          
        
        inpSenha = ct.CTkEntry(frame_login, textvariable=self.ctk_entry_var_senha, height=30, width=400, placeholder_text="Entre com a senha", show="*")
        inpSenha.grid(row=4, column=1, padx=5, pady=1, sticky="n") 
        inpSenha.tabindex = 3
        inpSenha.bind("<Tab>", self.format.mover_foco)
        #inpSenha.bind("<Return>", self.verificar_login)
        
        btnLogar = ct.CTkButton(frame_login, text="Login", command=self.verificar_login, compound="right",  text_color=("gray10", "#DCE4EE"))
        btnLogar.grid(row=5, column=1, padx=5, pady=5, sticky="n")
        
        
    def verificar_login(self):
        
        self.email    = str(self.ctk_entry_var_email.get())
        senha    = str(self.ctk_entry_var_senha.get())       
        
        if self.email == "":
            messagebox.showwarning("Informação", "O campo Email é de preenchimento obrigatório")
            return False        
        if senha == "":
            messagebox.showwarning("Informação", "O campo Senha é de preenchimento obrigatório")
            return False
        
        repo = UsuariosRepository()
        
        sucesso, exception = repo.login(self.email, senha, True)
        if (sucesso):
            self.tela_principal()
        else:
            messagebox.showwarning("LOGIN", exception)
    
    def tela_principal(self):
        
        self.recebimentos = REC.Recebimentos()
        self.pagamentos  = PAG.Pagamentos()
        self.organizacao  = ORG.Organizacao()          
        
        self.frame_login_email = ct.CTkLabel(self.navigation_frame, text=self.email, compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_login_email.grid(row=1, column=0, padx=5, pady=5, sticky="w")           
                        
        # botão navegação do pagamento
        self.button_pagamento = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Pagamentos",fg_color="transparent", 
                                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),image=self.logo_pagar, anchor="w", command=self.button_pagagamento_event)
        self.button_pagamento.grid(row=2, column=0, sticky="ew")   
        
         # botão navegação do recebimento
        self.button_recebimentos = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Recebimentos",fg_color="transparent", text_color=("gray10", "gray90"), 
                                                           hover_color=("gray70", "gray30"),image=self.logo_receber, anchor="w", command=self.button_recebimento_event)
        self.button_recebimentos.grid(row=3, column=0, sticky="ew")
        
         # botão navegação organização
        self.button_organizacao = ct.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Organizações",fg_color="transparent", text_color=("gray10", "gray90"), 
                                                           hover_color=("gray70", "gray30"),image=self.logo_receber, anchor="w", command=self.button_organizacao_event)
        self.button_organizacao.grid(row=4, column=0, sticky="ew")        
        
        # frame pagamento
        self.frame_pagamento = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_pagamento.grid_columnconfigure(2, weight=1)
        
       # frame recebimento
        self.frame_recebimento = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_recebimento.grid_columnconfigure(2, weight=1)   
        
       # frame organização
        self.frame_organizacao = ct.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_organizacao.grid_columnconfigure(2, weight=1)          
           
        # default frame
        self.select_frame_by_name("pagar")
        
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        #self.menu_file = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Logout", command=self.logout)
        self.menu_bar.add_cascade(label="Sair", command=self.confirmar_fechar_janela)
        #menu_file.add_command(label="Save")   
            
    def logout(self):
        self.login()
        self.menu_bar.delete(1,2)
        self.button_pagamento.grid_forget()
        self.button_recebimentos.grid_forget()
        self.button_organizacao.grid_forget()
        self.frame_login_email.configure(text="")    
        
    def confirmar_fechar_janela(self):
        resposta = messagebox.askokcancel("Confirmação", "Deseja realmente sair?")
        if resposta:
            self.quit()  # Fecha a janela se o usuário confirmar             
        
    def button_pagagamento_event(self):
        self.select_frame_by_name("pagar")    
        
    def button_recebimento_event(self):
        self.select_frame_by_name("receber") 
        
    def button_organizacao_event(self):
        self.select_frame_by_name("organizacao")          
        
    def select_frame_by_name(self, name):
        self.button_pagamento.configure(fg_color=("gray75", "gray25") if name == "pagar" else "transparent")
        self.button_recebimentos.configure(fg_color=("gray75", "gray25") if name == "receber" else "transparent")
        self.button_organizacao.configure(fg_color=("gray75", "gray25") if name == "organizacao" else "transparent")
        
        self.frame_organizacao.grid_forget()
        self.frame_pagamento.grid_forget()
        self.frame_recebimento.grid_forget() 
        
        if name == "organizacao":
            self.frame_organizacao.grid(row=0, column=1, sticky="nsew")
            self.organizacao.organizacao(self.frame_organizacao)
        if name == "pagar":
            self.frame_pagamento.grid(row=0, column=1, sticky="nsew")
            self.pagamentos.pagar(self.frame_pagamento)
        if name == "receber":
            self.frame_recebimento.grid(row=0, column=1, sticky="nsew")
            self.recebimentos.receber(self.frame_recebimento)     
        
        
if __name__ == "__main__":
    app = App()
    app.mainloop()        
    