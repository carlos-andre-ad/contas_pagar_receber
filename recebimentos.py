import customtkinter as ct
import tkinter as tk
from DB.entidades import contas_receber as cr
from DB.entidades import pessoa
from Utils import formatacao
from Utils import paginacao as page
from tkinter import ttk
from tkinter import messagebox
from CTkToolTip import *
from dotenv import load_dotenv
import os

class Recebimentos():
    def __init__(self):
        load_dotenv()
        self.paginar_tree_view = int(os.getenv('PAGINACAO'))
        self.tamanho_pagina    = int(os.getenv('TAMANHO_PAGINA'))
        super().__init__()
        
    def receber(self,frame_recebimento):
        
        self.contasReceber = cr.ContasReceber()
        self.format = formatacao.Util()        
        
        self.nome_coluna_ordenar = "descricao" #ordenação default
        self.colunas_data   = ["data_recebimento"] # Nome das colunas do tipo data
        self.colunas_numericas = ["id", "valor"] # nome das colunas do tipo numérico
        self.colunas_tree_view  = ["id", "descricao", "data_recebimento","valor"] # colunas do tree view
        self.ordenacao_colunas = {"id": "crescente", "descricao": "crescente", "data_recebimento": "crescente", "valor": "crescente"}    
        
        self.tree_view_recebimento = ttk.Treeview(frame_recebimento)      
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10, "bold"))
        self.tree_view_recebimento['columns'] = tuple(self.colunas_tree_view)
        self.tree_view_recebimento.column("#0", width=0, stretch=False)
        self.tree_view_recebimento.column("id",  width=60)
        self.tree_view_recebimento.column("descricao",  width=500)
        self.tree_view_recebimento.column("data_recebimento", anchor="center", width=150)
        self.tree_view_recebimento.column("valor", anchor="e", width=200)
        self.tree_view_recebimento.heading("id", text="ID", command=lambda: self.ordenar_por_coluna_click_cabecalho("id"))
        self.tree_view_recebimento.heading("descricao", text="Descrição", command=lambda: self.ordenar_por_coluna_click_cabecalho("descricao"))
        self.tree_view_recebimento.heading("data_recebimento", text="Data Pagamento", command=lambda: self.ordenar_por_coluna_click_cabecalho("data_recebimento"))
        self.tree_view_recebimento.heading("valor",  text="Valor", command=lambda: self.ordenar_por_coluna_click_cabecalho("valor"))
        self.tree_view_recebimento.bind("<Button-1>", lambda event: self.on_item_double_click_bind(event)) 
        self.tree_view_recebimento.bind("<KeyPress>", lambda event: self.on_item_double_click_bind(event)) 
        self.tree_view_recebimento.tag_configure('orow', background='#EEEEEE')             
        
        self.lista_contas_receber = self.contasReceber.listar(True)
        
        self.idx_coluna_id = 0
        self.tree_view_recebimento_id_selecionado = 0
        self.paginacao = page.PaginatedTreeView(self.tamanho_pagina, 
                                                0, 
                                                self.paginar_tree_view, 
                                                self.nome_coluna_ordenar, 
                                                self.colunas_data, 
                                                self.colunas_numericas, 
                                                self.colunas_tree_view, 
                                                self.ordenacao_colunas,
                                                self.tree_view_recebimento,
                                                self.lista_contas_receber,
                                                self.idx_coluna_id,
                                                self.tree_view_recebimento_id_selecionado
                                                )
        
        self.label = ct.CTkLabel(frame_recebimento, text="Contas à Receber", font=ct.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=10)        
        
        self.frame_recebimento_label_organizacao = ct.CTkLabel(frame_recebimento, text="Organização:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_organizacao.grid(row=1, column=0, padx=10, pady=5, sticky="w")            
        self.frame_recebimento_label_descricao = ct.CTkLabel(frame_recebimento, text="Descrição:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_descricao.grid(row=2, column=0, padx=10, pady=5, sticky="w")    
        
        self.frame_recebimento_label_data_receb = ct.CTkLabel(frame_recebimento, text="Data Recebimento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_data_receb.grid(row=3, column=0, padx=10, pady=5 ,sticky="w")   

        self.frame_recebimento_label_valor = ct.CTkLabel(frame_recebimento, text="Valor:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_valor.grid(row=3, column=1, padx=170, pady=5 ,sticky="w")   
        
        self.frame_recebimento_label_obs = ct.CTkLabel(frame_recebimento, text="Observações:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_obs.grid(row=4, column=0, padx=10, pady=5 ,sticky="w")            
                
        #INPUTS
        self.ctk_entry_var_descricao = tk.StringVar()
        self.ctk_entry_var_id = tk.StringVar()
        self.ctk_entry_var_data_receb = tk.StringVar()
        self.ctk_entry_var_valor = tk.StringVar()
        self.ctk_entry_var_obs = tk.StringVar()
        self.ctk_combobox_var_organizacao = tk.StringVar()
        self.ctk_entry_var_valor_total = tk.StringVar()
        self.ctk_entry_var_filtro = tk.StringVar()       
                
        p = pessoa.Pessoa()
        self.organizacoes = p.listar(True)
        
        self.frame_recebimento_combobox_organizacoes = ct.CTkComboBox(frame_recebimento, values=[item['nome'] for item in self.organizacoes], width=905,
                                                                        command=self.selecionar_organizacao, variable=self.ctk_combobox_var_organizacao)
        self.frame_recebimento_combobox_organizacoes.grid(row=1, column=1, padx=10, pady=5, sticky="w") 
        self.frame_recebimento_combobox_organizacoes.tabindex = 1
        
        self.frame_recebimento_entry_descricao = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_descricao, height=30, width=905)
        self.frame_recebimento_entry_descricao.grid(row=2, column=1, padx=10, pady=5, sticky="w") 
        self.frame_recebimento_entry_descricao.tabindex = 2
        self.frame_recebimento_entry_descricao.bind("<Tab>", self.format.mover_foco)
        
        self.frame_recebimento_entry_data_receb = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_data_receb, height=30, width=150)
        self.frame_recebimento_entry_data_receb.grid(row=3, column=1, padx=10, pady=5, sticky="w")     
        self.frame_recebimento_entry_data_receb.bind("<KeyPress>", lambda event: self.format.formatar_data(event, self.frame_recebimento_entry_data_receb))          
        self.frame_recebimento_entry_data_receb.tabindex = 3
        self.frame_recebimento_entry_data_receb.bind("<Tab>", self.format.mover_foco)
        
        self.frame_recebimento_entry_valor= ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_valor, height=30, width=150, justify="right")
        self.frame_recebimento_entry_valor.grid(row=3, column=1, padx=210, pady=5, sticky="w")   
        self.frame_recebimento_entry_valor.bind("<KeyPress>", lambda event: self.format.formatar_valor(event, self.frame_recebimento_entry_valor))
        self.frame_recebimento_entry_valor.tabindex = 4
        self.frame_recebimento_entry_valor.bind("<Tab>", self.format.mover_foco)
        
        self.frame_recebimento_textbox_obs = ct.CTkTextbox(frame_recebimento,  width=910, height=100, border_width=2)
        self.frame_recebimento_textbox_obs.grid(row=4, column=1, padx=10, pady=5, sticky="w")     
        self.frame_recebimento_textbox_obs.tabindex = 5
        self.frame_recebimento_textbox_obs.bind("<Tab>", self.format.mover_foco)
        
        
        self.frame_recebimento_button_novo = ct.CTkButton(frame_recebimento, text="Novo", command=self.novo,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_novo.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        CTkToolTip(self.frame_recebimento_button_novo, delay=0.5, message="Nova receita", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        self.frame_recebimento_button_altera = ct.CTkButton(frame_recebimento, text="Alterar", command=self.alterar,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_altera.grid(row=5, column=1, padx=155, pady=5, sticky="w")
        CTkToolTip(self.frame_recebimento_button_altera, delay=0.5, message="Alterar receita", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")        
        
        self.frame_recebimento_button_cancelar = ct.CTkButton(frame_recebimento, text="Cancelar", command=self.cancelar,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_cancelar.grid(row=5, column=1, padx=300, pady=5, sticky="w")
        CTkToolTip(self.frame_recebimento_button_cancelar, delay=0.5, message="Cancelar receita!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")        
        
        self.frame_recebimento_button_salvar = ct.CTkButton(frame_recebimento, text="Salvar", command=self.salvar, compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_salvar.grid(row=5, column=1, padx=445, pady=5, sticky="w")   
        CTkToolTip(self.frame_recebimento_button_salvar, delay=0.5, message="Salvar receita", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
               
        self.frame_recebimento_button_excluir = ct.CTkButton(frame_recebimento, text="Excluir", command=self.remover, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_excluir.grid(row=5, column=1, padx=590, pady=5, sticky="w")     
        CTkToolTip(self.frame_recebimento_button_excluir, delay=0.5, message="Exclui receita selecionado!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        #INPUT FILTRAR
        self.frame_label_filtro = ct.CTkLabel(frame_recebimento, text="Filtro:",  compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_label_filtro.grid(row=6, column=1, padx=630, pady=5 ,sticky="w")         
        self.frame_entry_filtro = ct.CTkEntry(frame_recebimento, height=30, width=250, textvariable=self.ctk_entry_var_filtro)
        self.frame_entry_filtro.grid(row=6, column=1, padx=675, pady=1, sticky="w")       
        self.frame_entry_filtro.bind("<KeyRelease>", self.filtrar_bind)
        
        self.tree_view_recebimento.grid(row=7, column=1, columnspan=4, rowspan=5, padx=10, pady=1, sticky="w")
        
        #TOTALIZADORES
        valor_total = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_valor_total, border_width=0, justify="right",
                                    height=30, width=150, state=tk.DISABLED, font=ct.CTkFont(size=14, weight="bold"))      
        valor_total.grid(row=20, column=1, padx=775, pady=1, sticky="w")   
        
        if self.paginar_tree_view == 1:
            self.first_button  = ct.CTkButton(frame_recebimento, text="Primeiro", command=self.primeira_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            self.next_button  = ct.CTkButton(frame_recebimento, text="Próximo", command=self.proxima_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            self.prev_button = ct.CTkButton(frame_recebimento, text="Anterior", command=self.pagina_anterior, compound="right",  text_color=("gray10", "#DCE4EE"))
            self.last_button  = ct.CTkButton(frame_recebimento, text="Último", command=self.ultima_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            self.first_button.grid(row=20, column=1, padx=10, pady=1, sticky="w")
            self.next_button.grid(row=20, column=1, padx=155, pady=1, sticky="w")
            self.prev_button.grid(row=20, column=1, padx=300, pady=1, sticky="w")
            self.last_button.grid(row=20, column=1, padx=445, pady=1, sticky="w")  
     
        
        self.acao = 6 #1=novo, #2=altera, 3=salvar, 4=deletar, 5=cancelar, 6=listar, 7=limpar
        self.update_tree_view()
        self.habilita_desabilita_entry(tk.DISABLED)

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
        self.ctk_entry_var_descricao.set("")
        self.ctk_entry_var_data_receb.set("")
        self.ctk_entry_var_valor.set("")
        self.frame_recebimento_textbox_obs.delete("1.0", "end") 
        self.acao = 7
    
    def cancelar(self):
        self.acao = 5
        self.controla_botoes()
        
        
    def remover(self):
        desc = str(self.ctk_entry_var_descricao.get())
        resposta = messagebox.askyesno("Confirmação", f"Deseja excluir a receita {desc}?")
        if (resposta):      
            id = str(self.ctk_entry_var_id.get())
            if (self.contasReceber.delete(id)):
                self.acao = 4
                self.lista_contas_receber = self.contasReceber.listar(True)                   
                self.update_tree_view()         
            
    def salvar(self):
        id          = str(self.ctk_entry_var_id.get())
        desc        = str(self.ctk_entry_var_descricao.get())
        data_recb   = str(self.ctk_entry_var_data_receb.get())
        valor       = str(self.ctk_entry_var_valor.get())
        obs         = str(self.frame_recebimento_textbox_obs.get('1.0', 'end'))  
        org         = str(self.ctk_combobox_var_organizacao.get())
        
        valor = valor.replace("R$","").replace(",","").replace(" ","")
        
        if org == "":
            messagebox.showinfo("Informação", "O campo organização é de preenchimento obrigatório")
            self.frame_recebimento_entry_descricao.focus()
            return False        
        if desc == "":
            messagebox.showinfo("Informação", "O campo descrição é de preenchimento obrigatório")
            self.frame_recebimento_entry_descricao.focus()
            return False
        if data_recb == "":
            messagebox.showinfo("Informação", "O campo data do recebimento é de preenchimento obrigatório")
            self.frame_recebimento_entry_data_venc.focus()
            return False        
        if valor == "":
            messagebox.showinfo("Informação", "O campo valor é de preenchimento obrigatório")
            self.frame_recebimento_entry_valor.focus()
            return False
        
        sucesso = self.contasReceber.insert_update(id, desc, data_recb, valor, obs, org)
        if (sucesso):  
            resposta = messagebox.askyesno("Confirmação", f"Confirma {' inclusão' if not id else 'alteração'} dessa receita?")
            if resposta:    
                new_id =  self.contasReceber.new_id
                self.lista_contas_receber = self.contasReceber.listar(True)
                if id == "":
                    messagebox.showinfo("Sucesso", f"Receita inserida com sucesso")
                    self.ctk_entry_var_filtro.set("")
                    if (new_id != None):
                        self.tree_view_recebimento_id_selecionado = new_id
                    else:
                        self.tree_view_recebimento_id_selecionado = self.lista_contas_receber[len(self.lista_contas_receber)-1]['id']
                else:
                    messagebox.showinfo("Sucesso", f"Receita alterada com sucesso")
                
                self.paginacao.verificar_pagina_item = True
                self.acao = 3
                self.update_tree_view() 
                self.paginacao.verificar_pagina_item = False
                
            
        
    def update_tree_view(self):
        vl_tot = 0.0
        for data in self.tree_view_recebimento.get_children():
            self.tree_view_recebimento.delete(data) 
            
        self.data_filtro_original = []
        for result in self.lista_contas_receber:
            val = result['valor']
            vl_tot = vl_tot + float(val)
            result['valor'] = self.format.formatar_valor_real(float(val))
                                
            result = list(result.values())
            #Para auxiliar no buscar
            self.data_filtro_original.append(result)  

        #TOTALIZADORES
        self.ctk_entry_var_valor_total.set( self.format.formatar_valor_real(vl_tot)  )
        
        if self.acao == 4:
            self.tree_view_id_selecionado = 0
            self.paginacao.tree_view_id_selecionado = self.tree_view_recebimento_id_selecionado
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
            item = self.tree_view_recebimento.identify('item', event.x, event.y)
            if item:
                self.tree_view_recebimento.selection_set(item)
                self.tree_view_recebimento.focus(item)                
                self.on_item_double_click()
            else:
                if event.keysym in ('Up', 'Down'):
                    if event.keysym == 'Up':
                        item = self.tree_view_recebimento.prev(self.tree_view_recebimento.focus())
                    elif event.keysym == 'Down':
                        item = self.tree_view_recebimento.next(self.tree_view_recebimento.focus())

                    if item:
                        self.tree_view_recebimento.selection_set(item)
                        self.tree_view_recebimento.focus(item)                        
                        self.on_item_double_click()
        
    def on_item_double_click(self):
        self.buscar()
        self.controla_botoes()
        
    def buscar(self):    
        if len(self.tree_view_recebimento.selection()) > 0:
            item = self.tree_view_recebimento.selection()[0]
            values = self.tree_view_recebimento.item(item, 'values')
            self.tree_view_recebimento_id_selecionado = values[0]
            self.paginacao.tree_view_id_selecionado = self.tree_view_recebimento_id_selecionado
            res = self.contasReceber.buscar(self.tree_view_recebimento_id_selecionado, True)
            if res != None:
                self.ctk_combobox_var_organizacao.set(res['organizacao'])
                self.ctk_entry_var_id.set(res['id'])
                self.ctk_entry_var_descricao.set(res['descricao'])
                self.ctk_entry_var_data_receb.set(res['data_recebimento'])
                self.ctk_entry_var_valor.set(res['valor'])
                self.frame_recebimento_textbox_obs.configure(state=tk.NORMAL)
                self.frame_recebimento_textbox_obs.delete("1.0", "end") 
                if (res['observacoes'] != None and res['observacoes'] != ""):
                    self.frame_recebimento_textbox_obs.insert("1.0", res['observacoes'])
                self.frame_recebimento_textbox_obs.configure(state=tk.DISABLED)
            else:
                messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
                        
    def filtrar_bind(self, event):
        self.filtrar()

    def filtrar(self):
        filtro = self.frame_entry_filtro.get().lower()
        if filtro:
            items = []
            for item in self.data_filtro_original:
                if any(str(value).lower().find(filtro) != -1 for value in item):
                    items.append(item)
                    self.tree_view_recebimento_id_selecionado = items[0][0]
                    self.paginacao.tree_view_id_selecionado = self.tree_view_recebimento_id_selecionado
            self.atualizar_treeview(items)
                          
        else:
            #self.atualizar_treeview(self.data_filtro_original)
            self.monta_paginacao(False)
            self.tree_view_recebimento_id_selecionado = 0
            self.paginacao.tree_view_id_selecionado = self.tree_view_recebimento_id_selecionado            
            self.selecionar_linha_tree_view_por_id()   
            self.on_item_double_click()       
            
    def atualizar_treeview(self, items):
        self.tree_view_recebimento.delete(*self.tree_view_recebimento.get_children())
        tot = 0
        tot_p = 0
        for item in items:
            val = item[3]
            val = val.replace("R$","").replace(" ","").replace(".","").replace(",",".")
            tot = tot + float(val)
                                   
            self.tree_view_recebimento.insert("", "end", values=item)  
            
        self.paginacao.idx_coluna_id            = self.idx_coluna_id
        self.paginacao.tree_view_paginada = self.tree_view_recebimento
        self.selecionar_linha_tree_view_por_id()
        self.tree_view_recebimento = self.paginacao.tree_view_paginada
        self.on_item_double_click()

        self.ctk_entry_var_valor_total.set( self.format.formatar_valor_real(tot)  )

        self.acao = 6
        self.controla_botoes()
    
    
    def selecionar_organizacao(self, selected):
        self.ctk_combobox_var_organizacao.set( selected)


    def ordenar_por_coluna_click_cabecalho(self, coluna):
        self.nome_coluna_ordenar = coluna
        self.paginacao.nome_coluna_ordenar      = self.nome_coluna_ordenar
        self.paginacao.ordencao(True)
        self.on_item_double_click()
        self.paginacao.tree_view_id_selecionado = self.tree_view_recebimento_id_selecionado
        self.paginacao.idx_coluna_id            = self.idx_coluna_id        
        self.selecionar_linha_tree_view_por_id()
        
    def selecionar_linha_tree_view_por_id(self):
        self.paginacao.selecionar_linha_tree_view_por_id()
        self.tree_view_recebimento = self.paginacao.tree_view_paginada
        
    def monta_paginacao(self, alternar_ascendencia):
        self.paginacao.tree_view_paginada       = self.tree_view_recebimento
        self.paginacao.dados_all                = self.lista_contas_receber
        self.paginacao.tree_view_id_selecionado = self.tree_view_recebimento_id_selecionado
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
        self.frame_recebimento_combobox_organizacoes.configure(state=state)
        self.frame_recebimento_entry_descricao.configure(state=state)
        self.frame_recebimento_entry_data_receb.configure(state=state)
        self.frame_recebimento_entry_valor.configure(state=state)
        self.frame_recebimento_textbox_obs.configure(state=state)
            
    def controla_botoes(self):
        verifica = False
        
        if self.paginar_tree_view == 1:
            if len(self.tree_view_recebimento.get_children()) <= int(self.tamanho_pagina ):
                self.next_button.configure(state=tk.DISABLED)
                self.prev_button.configure(state=tk.DISABLED)
                self.first_button.configure(state=tk.DISABLED)
                self.last_button.configure(state=tk.DISABLED)

        if self.acao == 1:#novo
            self.frame_recebimento_button_novo.configure(state=tk.DISABLED)
            self.frame_recebimento_button_altera.configure(state=tk.DISABLED)
            self.frame_recebimento_button_excluir.configure(state=tk.DISABLED) 
            self.frame_recebimento_button_cancelar.configure(state=tk.NORMAL)
            self.frame_recebimento_button_salvar.configure(state=tk.NORMAL)
            self.next_button.configure(state=tk.DISABLED)
            self.prev_button.configure(state=tk.DISABLED)
            self.first_button.configure(state=tk.DISABLED)
            self.last_button.configure(state=tk.DISABLED)       
            self.tree_view_recebimento.configure(selectmode="none")
            self.frame_entry_filtro.configure(state=tk.DISABLED)
            self.habilita_desabilita_entry(tk.NORMAL)
            
        if self.acao == 2:#altera
            self.frame_recebimento_button_novo.configure(state=tk.DISABLED)
            self.frame_recebimento_button_altera.configure(state=tk.DISABLED)
            self.frame_recebimento_button_excluir.configure(state=tk.DISABLED) 
            self.frame_recebimento_button_cancelar.configure(state=tk.NORMAL)
            self.frame_recebimento_button_salvar.configure(state=tk.NORMAL)
            self.next_button.configure(state=tk.DISABLED)
            self.prev_button.configure(state=tk.DISABLED)
            self.first_button.configure(state=tk.DISABLED)
            self.last_button.configure(state=tk.DISABLED)             
            self.tree_view_recebimento.configure(selectmode="none")
            self.frame_entry_filtro.configure(state=tk.DISABLED)            
            self.habilita_desabilita_entry(tk.NORMAL)
            
        if self.acao == 3:#Salvar
            self.frame_recebimento_button_novo.configure(state=tk.NORMAL)
            self.frame_recebimento_button_altera.configure(state=tk.NORMAL)
            self.frame_recebimento_button_excluir.configure(state=tk.NORMAL) 
            self.frame_recebimento_button_cancelar.configure(state=tk.DISABLED)
            self.frame_recebimento_button_salvar.configure(state=tk.DISABLED)            
            self.tree_view_recebimento.configure(selectmode="browse")
            self.frame_entry_filtro.configure(state=tk.NORMAL)            
            self.habilita_desabilita_entry(tk.DISABLED)
            self.atualizar_estado_botoes_paginacao()    
            
        if self.acao == 4:#deletar
            self.frame_recebimento_button_novo.configure(state=tk.NORMAL)
            self.frame_recebimento_button_cancelar.configure(state=tk.DISABLED)
            self.frame_recebimento_button_salvar.configure(state=tk.DISABLED)       
            if len(self.tree_view_recebimento.get_children()) == 0:
                self.limpar()              
            verifica = True                 
            
        if self.acao == 5:#cancelar
            self.limpar()
            self.frame_recebimento_button_novo.configure(state=tk.NORMAL)
            self.frame_recebimento_button_cancelar.configure(state=tk.DISABLED)
            self.frame_recebimento_button_salvar.configure(state=tk.DISABLED)
            self.tree_view_recebimento.configure(selectmode="browse")
            self.frame_entry_filtro.configure(state=tk.NORMAL)            
            self.habilita_desabilita_entry(tk.DISABLED)
            self.selecionar_linha_tree_view_por_id()
            self.buscar()          
            verifica = True
            
        if self.acao == 6 or verifica:
            verifica = False
            self.frame_recebimento_button_salvar.configure(state=tk.DISABLED)
            self.frame_recebimento_button_cancelar.configure(state=tk.DISABLED)
            
            if len(self.tree_view_recebimento.get_children()) == 0:
                self.frame_recebimento_button_excluir.configure(state=tk.DISABLED) 
                self.frame_recebimento_button_altera.configure(state=tk.DISABLED)           
            else:        
                item = self.tree_view_recebimento.focus()
                if item:
                    self.frame_recebimento_button_excluir.configure(state=tk.NORMAL)
                    self.frame_recebimento_button_altera.configure(state=tk.NORMAL)  
                else:
                    self.frame_recebimento_button_excluir.configure(state=tk.DISABLED)
                    self.frame_recebimento_button_altera.configure(state=tk.DISABLED)  
            self.atualizar_estado_botoes_paginacao()        
           
