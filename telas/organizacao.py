import customtkinter as ct
import tkinter as tk
from Utils import formatacao
from Utils import paginacao as page
from tkinter import ttk, filedialog
from tkinter import messagebox
from CTkToolTip import *
from dotenv import load_dotenv
import os
from infra.repository.organizacoes_repository import OrganizacoesRepository
from telas import pdfview
from telas import relatorios
class Organizacao():
    
    def __init__(self):
        load_dotenv()
        self.paginar_tree_view = int(os.getenv('PAGINACAO'))
        self.tamanho_pagina    = int(os.getenv('TAMANHO_PAGINA'))
        super().__init__()
        
    def listar(self, tupla):
        self.repo_org = OrganizacoesRepository()
        sucesso, self.lista_organizacoes = self.repo_org.listar(tupla)
        if sucesso == False:
            messagebox.showerror("Erro", self.lista_organizacoes)
            self.lista_organizacoes = []
        return sucesso       
     
        
    def organizacao(self, frame_organizacao):

        self.listar(True)
        self.rels_pdf = relatorios.Relatorios(title_text="Cadastro de organizações")
        self.format = formatacao.Util()  
        self.frame_organizacao = frame_organizacao
        self.nome_coluna_ordenar = "nome" #ordenação default
        self.colunas_data   = [] # Nome das colunas do tipo data
        self.colunas_numericas = ["id"] # nome das colunas do tipo numérico
        self.colunas_tree_view  = ["id", "nome"] # colunas do tree view
        self.ordenacao_colunas = {"id": "crescente", "nome": "crescente"}
        self.colunas_relatorio = ["Código", "Nome"]
        
        self.tree_view_organizacao = ttk.Treeview(self.frame_organizacao)      
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10, "bold"))
        self.tree_view_organizacao['columns'] = tuple(self.colunas_tree_view)
        self.tree_view_organizacao.column("#0", width=0, stretch=False)
        self.tree_view_organizacao.column("id",  width=60)
        self.tree_view_organizacao.column("nome",  width=850)
        self.tree_view_organizacao.heading("id", text="ID", command=lambda: self.ordenar_por_coluna_click_cabecalho("id"))
        self.tree_view_organizacao.heading("nome", text="Nome", command=lambda: self.ordenar_por_coluna_click_cabecalho("descricao"))
        self.tree_view_organizacao.bind("<Button-1>", lambda event: self.on_item_double_click_bind(event)) 
        self.tree_view_organizacao.bind("<KeyPress>", lambda event: self.on_item_double_click_bind(event)) 
        self.tree_view_organizacao.tag_configure('orow', background='#EEEEEE')             
        
        self.idx_coluna_id = 0
        self.tree_view_organizacao_id_selecionado = 0
        self.paginacao = page.PaginatedTreeView(self.tamanho_pagina, 
                                                0, 
                                                self.paginar_tree_view, 
                                                self.nome_coluna_ordenar, 
                                                self.colunas_data, 
                                                self.colunas_numericas, 
                                                self.colunas_tree_view, 
                                                self.ordenacao_colunas,
                                                self.tree_view_organizacao,
                                                self.lista_organizacoes,
                                                self.idx_coluna_id,
                                                self.tree_view_organizacao_id_selecionado
                                                )
        
        self.label = ct.CTkLabel(self.frame_organizacao, text="Organizações", font=ct.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=10)        

        self.frame_organizacao_label_nome = ct.CTkLabel(self.frame_organizacao, text="Nome:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_organizacao_label_nome.grid(row=2, column=0, padx=10, pady=5, sticky="w")             
                
        #INPUTS
        self.ctk_entry_var_nome = tk.StringVar()
        self.ctk_entry_var_id = tk.StringVar()
        self.ctk_entry_var_filtro = tk.StringVar()       

        self.frame_organizacao_entry_nome = ct.CTkEntry(self.frame_organizacao, textvariable=self.ctk_entry_var_nome, height=30, width=905)
        self.frame_organizacao_entry_nome.grid(row=2, column=1, padx=10, pady=5, sticky="w") 
        self.frame_organizacao_entry_nome.tabindex = 1
        self.frame_organizacao_entry_nome.bind("<Tab>", self.format.mover_foco)
        
        self.frame_organizacao_button_novo = ct.CTkButton(self.frame_organizacao, text="Novo", command=self.novo,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_novo.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        CTkToolTip(self.frame_organizacao_button_novo, delay=0.5, message="Nova organização", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        self.frame_organizacao_button_altera = ct.CTkButton(self.frame_organizacao, text="Alterar", command=self.alterar,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_altera.grid(row=5, column=1, padx=155, pady=5, sticky="w")
        CTkToolTip(self.frame_organizacao_button_altera, delay=0.5, message="Alterar organização", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")        
        
        self.frame_organizacao_button_cancelar = ct.CTkButton(self.frame_organizacao, text="Cancelar", command=self.cancelar,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_cancelar.grid(row=5, column=1, padx=300, pady=5, sticky="w")
        CTkToolTip(self.frame_organizacao_button_cancelar, delay=0.5, message="Cancelar organização!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")        
        
        self.frame_organizacao_button_salvar = ct.CTkButton(self.frame_organizacao, text="Salvar", command=self.salvar, compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_salvar.grid(row=5, column=1, padx=445, pady=5, sticky="w")   
        CTkToolTip(self.frame_organizacao_button_salvar, delay=0.5, message="Salvar organização", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
               
        self.frame_organizacao_button_excluir = ct.CTkButton(self.frame_organizacao, text="Excluir", command=self.remover, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_excluir.grid(row=5, column=1, padx=590, pady=5, sticky="w")     
        CTkToolTip(self.frame_organizacao_button_excluir, delay=0.5, message="Exclui organização selecionado!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        #INPUT FILTRAR
        self.frame_label_filtro = ct.CTkLabel(self.frame_organizacao, text="Filtro:",  compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_label_filtro.grid(row=6, column=1, padx=630, pady=5 ,sticky="w")         
        self.frame_entry_filtro = ct.CTkEntry(self.frame_organizacao, height=30, width=250, textvariable=self.ctk_entry_var_filtro)
        self.frame_entry_filtro.grid(row=6, column=1, padx=675, pady=1, sticky="w")       
        self.frame_entry_filtro.bind("<KeyRelease>", self.filtrar_bind)
        
        self.tree_view_organizacao.grid(row=7, column=1, columnspan=4, rowspan=5, padx=10, pady=1, sticky="w")
          
        _row = 12
        if self.paginar_tree_view == 1:
            self.first_button  = ct.CTkButton(self.frame_organizacao, text="Primeiro", command=self.primeira_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            self.next_button  = ct.CTkButton(self.frame_organizacao, text="Próximo", command=self.proxima_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            self.prev_button = ct.CTkButton(self.frame_organizacao, text="Anterior", command=self.pagina_anterior, compound="right",  text_color=("gray10", "#DCE4EE"))
            self.last_button  = ct.CTkButton(self.frame_organizacao, text="Último", command=self.ultima_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            self.first_button.grid(row=12, column=1, padx=10, pady=1, sticky="w")
            self.next_button.grid(row=12, column=1, padx=155, pady=1, sticky="w")
            self.prev_button.grid(row=12, column=1, padx=300, pady=1, sticky="w")
            self.last_button.grid(row=12, column=1, padx=445, pady=1, sticky="w") 
            _row = 13
            
        self.frame_organizacao_button_imprimir = ct.CTkButton(self.frame_organizacao, text="Imprimir", command=self.imprimir, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_imprimir.grid(row=_row, column=1, padx=800, pady=5, sticky="w")     
        CTkToolTip(self.frame_organizacao_button_imprimir, delay=0.5, message="Visualizar Organizações", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")        
        

        self.acao = 6 #1=novo, #2=altera, 3=salvar, 4=deletar, 5=cancelar, 6=listar, 7=limpar
        self.update_tree_view()
        self.habilita_desabilita_entry(tk.DISABLED)
        
    def imprimir(self):
       
       s, lista = self.repo_org.listar(None)
       data = [self.colunas_relatorio]
       for p in lista:
           data.append([f"{p.id}", f"{p.nome}"])      
           
       self.rels_pdf.add_table(data=data)
       self.rels_pdf.build()
         
       #self.frame_organizacao.grid_forget()
       
       # frame dos relatorios em pdf
 
       
       view = pdfview.PDFView(self.rels_pdf.path)
         

    def alterar(self):
        self.acao = 2
        self.controla_botoes()
        
    def novo(self):
        self.ctk_entry_var_filtro.set("")  
        self.filtrar() 
        self.limpar()
        self.acao = 1
        self.controla_botoes()
        
    def limpar(self):
        self.ctk_entry_var_id.set("")
        self.ctk_entry_var_nome.set("")
        self.acao = 7
    
    def cancelar(self):
        self.acao = 5
        self.controla_botoes()
        
        
    def remover(self):
        desc = str(self.ctk_entry_var_nome.get())
        resposta = messagebox.askyesno("Confirmação", f"Deseja excluir a organização {desc}?")
        if (resposta):      
            id = str(self.ctk_entry_var_id.get())
            if (self.repo_org.delete(id)):
                self.acao = 4
                self.listar(True) 
                self.update_tree_view()         
            
    def salvar(self):
        id          = str(self.ctk_entry_var_id.get())
        desc        = str(self.ctk_entry_var_nome.get())
      
        if desc == "":
            messagebox.showinfo("Informação", "O campo nome é de preenchimento obrigatório")
            self.frame_organizacao_entry_nome.focus()
            return False
        
        sucesso, objects = self.repo_org.insert_update(id, desc)
        if (sucesso):  
            resposta = messagebox.askyesno("Confirmação", f"Confirma {' inclusão' if not id else 'alteração'} dessa organização?")
            if resposta:    
                self.listar(True) 
                if id == "":
                    messagebox.showinfo("Sucesso", f"Organização inserida com sucesso")
                    self.ctk_entry_var_filtro.set("")
                    if (objects != None):
                        self.tree_view_organizacao_id_selecionado = objects
                    else:
                        self.tree_view_organizacao_id_selecionado = self.lista_organizacoes[len(self.lista_organizacoes)-1]['id']
                else:
                    messagebox.showinfo("Sucesso", f"Organização alterada com sucesso")
                
                self.paginacao.verificar_pagina_item = True
                self.acao = 3
                self.update_tree_view() 
                self.paginacao.verificar_pagina_item = False
                
        else:
            messagebox.showerror("Erro", objects)    
        
    def update_tree_view(self):
 
        for data in self.tree_view_organizacao.get_children():
            self.tree_view_organizacao.delete(data) 
            
        self.data_filtro_original = []
        for result in self.lista_organizacoes:
                                
            result = list(result.values())
            #Para auxiliar no buscar
            self.data_filtro_original.append(result)  
        
        if self.acao == 4:
            self.tree_view_id_selecionado = 0
            self.paginacao.tree_view_id_selecionado = self.tree_view_organizacao_id_selecionado
            self.paginacao.verificar_pagina_item = False
        
        self.monta_paginacao(False)     
        self.selecionar_linha_tree_view_por_id()
        _acao = self.acao
        self.acao = -1 #para não executa o self.controla_botoes()
        self.on_item_double_click()
        self.acao = _acao
        self.controla_botoes()
        self.acao = 6
        
    def on_item_double_click_bind(self,event):
        if (self.ctk_entry_var_id.get() != ""):
            item = self.tree_view_organizacao.identify('item', event.x, event.y)
            if item:
                self.tree_view_organizacao.selection_set(item)
                self.tree_view_organizacao.focus(item)                
                self.on_item_double_click()
            else:
                if event.keysym in ('Up', 'Down'):
                    if event.keysym == 'Up':
                        item = self.tree_view_organizacao.prev(self.tree_view_organizacao.focus())
                    elif event.keysym == 'Down':
                        item = self.tree_view_organizacao.next(self.tree_view_organizacao.focus())

                    if item:
                        self.tree_view_organizacao.selection_set(item)
                        self.tree_view_organizacao.focus(item)                        
                        self.on_item_double_click()
        
    def on_item_double_click(self):
        self.buscar()
        self.controla_botoes()
        
    def buscar(self):    
        if len(self.tree_view_organizacao.selection()) > 0:
            item = self.tree_view_organizacao.selection()[0]
            values = self.tree_view_organizacao.item(item, 'values')
            self.tree_view_organizacao_id_selecionado = values[0]
            self.paginacao.tree_view_id_selecionado = self.tree_view_organizacao_id_selecionado
            sucesso, res = self.repo_org.buscar(self.tree_view_organizacao_id_selecionado, True)
            if sucesso:
                self.ctk_entry_var_id.set(res['id'])
                self.ctk_entry_var_nome.set(res['nome'])
            else:
                messagebox.showinfo("Atenção", f"{res}. O ID {id} não está presente na tabela")
                        
    def filtrar_bind(self, event):
        self.filtrar()

    def filtrar(self):
        filtro = self.frame_entry_filtro.get().lower()
        if filtro:
            items = []
            for item in self.data_filtro_original:
                if any(str(value).lower().find(filtro) != -1 for value in item):
                    items.append(item)
                    self.tree_view_organizacao_id_selecionado = items[0][0]
                    self.paginacao.tree_view_id_selecionado = self.tree_view_organizacao_id_selecionado
            self.atualizar_treeview(items)
                          
        else:
            #self.atualizar_treeview(self.data_filtro_original)
            self.monta_paginacao(False)
            self.tree_view_organizacao_id_selecionado = 0
            self.paginacao.tree_view_id_selecionado = self.tree_view_organizacao_id_selecionado            
            self.selecionar_linha_tree_view_por_id()   
            self.on_item_double_click()       
            
    def atualizar_treeview(self, items):
        self.tree_view_organizacao.delete(*self.tree_view_organizacao.get_children())
        for item in items:
            self.tree_view_organizacao.insert("", "end", values=item)  
            
        self.paginacao.idx_coluna_id            = self.idx_coluna_id
        self.paginacao.tree_view_paginada = self.tree_view_organizacao
        self.selecionar_linha_tree_view_por_id()
        self.tree_view_organizacao = self.paginacao.tree_view_paginada
        self.on_item_double_click()
        self.acao = 6
        self.controla_botoes()

    def ordenar_por_coluna_click_cabecalho(self, coluna):
        self.nome_coluna_ordenar = coluna
        self.paginacao.nome_coluna_ordenar      = self.nome_coluna_ordenar
        self.paginacao.ordencao(True)
        self.on_item_double_click()
        self.paginacao.tree_view_id_selecionado = self.tree_view_organizacao_id_selecionado
        self.paginacao.idx_coluna_id            = self.idx_coluna_id        
        self.selecionar_linha_tree_view_por_id()
        
    def selecionar_linha_tree_view_por_id(self):
        self.paginacao.selecionar_linha_tree_view_por_id()
        self.tree_view_organizacao = self.paginacao.tree_view_paginada
        
    def monta_paginacao(self, alternar_ascendencia):
        self.paginacao.tree_view_paginada       = self.tree_view_organizacao
        self.paginacao.dados_all                = self.lista_organizacoes
        self.paginacao.tree_view_id_selecionado = self.tree_view_organizacao_id_selecionado
        self.paginacao.idx_coluna_id            = self.idx_coluna_id
        self.paginacao.monta_paginacao(alternar_ascendencia)
        
    def primeira_pagina(self):
        self.paginacao.primeira_pagina()
        self.navegacao()   
        
    def ultima_pagina(self):
        self.paginacao.ultima_pagina()  
        self.navegacao()
        if len(self.tree_view_pagamento.get_children()) == 0:
            self.pagina_anterior()
            self.last_button.configure(state=tk.DISABLED)
            self.last_button_state_origem =tk.DISABLED
            self.next_button.configure(state=tk.DISABLED)
            self.next_button_state_origem =tk.DISABLED
        
    def proxima_pagina(self):
        self.paginacao.proxima_pagina()
        self.navegacao()   
        
    def pagina_anterior(self):
        self.paginacao.pagina_anterior()  
        self.navegacao()
        
    def navegacao(self):   
        self.paginacao.idx_coluna_id            = self.idx_coluna_id   
        self.monta_paginacao(False)  
        self.paginacao.tree_view_id_selecionado = 0    
        self.selecionar_linha_tree_view_por_id()
        self.on_item_double_click() 
        self.atualizar_estado_botoes_paginacao()   
                
   
        
    def atualizar_estado_botoes_paginacao(self):
        n, p, f, l = self.paginacao.atualizar_estado_botoes_paginacao()   
        self.next_button.configure(state=n) 
        self.prev_button.configure(state=p)
        self.first_button.configure(state=f) 
        self.last_button.configure(state=l)
        self.next_button_state_origem =  n 
        self.prev_button_state_origem =  p
        self.first_button_state_origem =  f
        self.last_button_state_origem =  l   
        
        
    def habilita_desabilita_entry(self, state):
        self.frame_organizacao_entry_nome.configure(state=state)

    def controla_botoes(self):
        verifica = False
        
        if self.paginar_tree_view == 1:
            if len(self.tree_view_organizacao.get_children()) <= int(self.tamanho_pagina ):
                self.next_button.configure(state=tk.DISABLED)
                self.prev_button.configure(state=tk.DISABLED)
                self.first_button.configure(state=tk.DISABLED)
                self.last_button.configure(state=tk.DISABLED)

        if self.acao == 1:#novo
            self.frame_organizacao_button_novo.configure(state=tk.DISABLED)
            self.frame_organizacao_button_altera.configure(state=tk.DISABLED)
            self.frame_organizacao_button_excluir.configure(state=tk.DISABLED) 
            self.frame_organizacao_button_cancelar.configure(state=tk.NORMAL)
            self.frame_organizacao_button_salvar.configure(state=tk.NORMAL)
            self.next_button.configure(state=tk.DISABLED)
            self.prev_button.configure(state=tk.DISABLED)
            self.first_button.configure(state=tk.DISABLED)
            self.last_button.configure(state=tk.DISABLED)       
            self.tree_view_organizacao.configure(selectmode="none")
            self.frame_entry_filtro.configure(state=tk.DISABLED)
            self.habilita_desabilita_entry(tk.NORMAL)
            
        if self.acao == 2:#altera
            self.frame_organizacao_button_novo.configure(state=tk.DISABLED)
            self.frame_organizacao_button_altera.configure(state=tk.DISABLED)
            self.frame_organizacao_button_excluir.configure(state=tk.DISABLED) 
            self.frame_organizacao_button_cancelar.configure(state=tk.NORMAL)
            self.frame_organizacao_button_salvar.configure(state=tk.NORMAL)
            self.next_button.configure(state=tk.DISABLED)
            self.prev_button.configure(state=tk.DISABLED)
            self.first_button.configure(state=tk.DISABLED)
            self.last_button.configure(state=tk.DISABLED)             
            self.tree_view_organizacao.configure(selectmode="none")
            self.frame_entry_filtro.configure(state=tk.DISABLED)            
            self.habilita_desabilita_entry(tk.NORMAL)
            
        if self.acao == 3:#Salvar
            self.frame_organizacao_button_novo.configure(state=tk.NORMAL)
            self.frame_organizacao_button_altera.configure(state=tk.NORMAL)
            self.frame_organizacao_button_excluir.configure(state=tk.NORMAL) 
            self.frame_organizacao_button_cancelar.configure(state=tk.DISABLED)
            self.frame_organizacao_button_salvar.configure(state=tk.DISABLED)            
            self.tree_view_organizacao.configure(selectmode="browse")
            self.frame_entry_filtro.configure(state=tk.NORMAL)            
            self.habilita_desabilita_entry(tk.DISABLED)
            self.atualizar_estado_botoes_paginacao()    
            
        if self.acao == 4:#deletar
            self.frame_organizacao_button_novo.configure(state=tk.NORMAL)
            self.frame_organizacao_button_cancelar.configure(state=tk.DISABLED)
            self.frame_organizacao_button_salvar.configure(state=tk.DISABLED)        
            if len(self.tree_view_organizacao.get_children()) == 0:
                self.limpar()              
            verifica = True                 
            
        if self.acao == 5:#cancelar
            self.limpar()
            self.frame_organizacao_button_novo.configure(state=tk.NORMAL)
            self.frame_organizacao_button_cancelar.configure(state=tk.DISABLED)
            self.frame_organizacao_button_salvar.configure(state=tk.DISABLED)
            self.tree_view_organizacao.configure(selectmode="browse")
            self.frame_entry_filtro.configure(state=tk.NORMAL)            
            self.habilita_desabilita_entry(tk.DISABLED)
            self.selecionar_linha_tree_view_por_id()
            self.buscar()          
            verifica = True
            
        if self.acao == 6 or verifica:
            verifica = False
            self.frame_organizacao_button_salvar.configure(state=tk.DISABLED)
            self.frame_organizacao_button_cancelar.configure(state=tk.DISABLED)
            
            if len(self.tree_view_organizacao.get_children()) == 0:
                self.frame_organizacao_button_excluir.configure(state=tk.DISABLED) 
                self.frame_organizacao_button_altera.configure(state=tk.DISABLED)           
            else:        
                item = self.tree_view_organizacao.focus()
                if item:
                    self.frame_organizacao_button_excluir.configure(state=tk.NORMAL)
                    self.frame_organizacao_button_altera.configure(state=tk.NORMAL)  
                else:
                    self.frame_organizacao_button_excluir.configure(state=tk.DISABLED)
                    self.frame_organizacao_button_altera.configure(state=tk.DISABLED)  
            self.atualizar_estado_botoes_paginacao()        