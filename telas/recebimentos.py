import customtkinter as ct
import tkinter as tk
from Utils import formatacao
from Utils import paginacao as page
from tkinter import ttk
from tkinter import messagebox
from CTkToolTip import *
from dotenv import load_dotenv
import os
from infra.repository.receitas_repository import ReceitasRepository
from infra.repository.organizacoes_repository import OrganizacoesRepository
from telas import pdfview, relatorios, toolbar


class Recebimentos():
    def __init__(self):
        load_dotenv()
        self.paginar_tree_view = int(os.getenv('PAGINACAO'))
        self.tamanho_pagina    = int(os.getenv('TAMANHO_PAGINA'))
        super().__init__()
        
    def listar(self, tupla):
        self.repo_receitas = ReceitasRepository()
        sucesso, self.lista_contas_receber = self.repo_receitas.listar(tupla)
        if sucesso == False:
            messagebox.showerror("Erro", self.lista_contas_receber)
            self.lista_contas_receber = []
        return sucesso        
        
    def receber(self,frame_recebimento, root):
        self.root = root
        self.listar(True)
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
                
        self.repo_org = OrganizacoesRepository()
        sucesso, organizacoes = self.repo_org.listar(True)
        
        self.frame_recebimento_combobox_organizacoes = ct.CTkComboBox(frame_recebimento, values=[item['nome'] for item in organizacoes], width=905,
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
        
        #BOTÕES DE AÇÃO    
        bar = toolbar.toolbar() 
        bar.botoes_acao(self, frame_recebimento, 80, 28, 5, 1, 'w', 5, 10, 95, 180, 265,350, 6, 1, 630, 5, "w",250, 30,675, 1)
        # TREE
        self.tree_view_recebimento.grid(row=7, column=1, columnspan=4, rowspan=5, padx=10, pady=1, sticky="w")
        
        #TOTALIZADORES
        valor_total = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_valor_total, border_width=0, justify="right",
                                    height=30, width=150, state=tk.DISABLED, font=ct.CTkFont(size=14, weight="bold"))      
        valor_total.grid(row=20, column=1, padx=775, pady=1, sticky="w")   
        
        #BOTOES DE NAVEGAÇÃO CRIADOS E CONFIGURADOS EM PAGINACAO
        self.paginacao.navegacao(self,frame_recebimento, self.paginar_tree_view, 60, 28, 20, 1, "w",1, 10, 75, 140, 205, 300)
        
        self.acao = 6 #1=novo, #2=altera, 3=salvar, 4=deletar, 5=cancelar, 6=listar, 7=limpar
        self.update_tree_view()
        self.habilita_desabilita_entry(tk.DISABLED)
        
        
    def imprimir(self):
        pass        

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
            if (self.repo_receitas.delete(id)):
                self.acao = 4
                self.listar(True)                  
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
        
        sucesso, objects = self.repo_receitas.insert_update(id, desc, data_recb, valor, obs, org)
        if (sucesso):  
            resposta = messagebox.askyesno("Confirmação", f"Confirma {' inclusão' if not id else 'alteração'} dessa receita?")
            if resposta:    
                self.listar(True)
                if id == "":
                    messagebox.showinfo("Sucesso", f"Receita inserida com sucesso")
                    self.ctk_entry_var_filtro.set("")
                    if (objects != None):
                        self.tree_view_recebimento_id_selecionado = objects
                    else:
                        self.tree_view_recebimento_id_selecionado = self.lista_contas_receber[len(self.lista_contas_receber)-1]['id']
                else:
                    messagebox.showinfo("Sucesso", f"Receita alterada com sucesso")
                
                self.paginacao.verificar_pagina_item = True
                self.acao = 3
                self.update_tree_view() 
                self.paginacao.verificar_pagina_item = False
        else:
            messagebox.showerror("Erro", objects)                   
            
        
    def update_tree_view(self):
        vl_tot = 0.0
        for data in self.tree_view_recebimento.get_children():
            self.tree_view_recebimento.delete(data) 
            
        self.data_filtro_original = []
        for result in self.lista_contas_receber:
            val = result['valor']
            vl_tot = vl_tot + float(val)
            result['valor'] = self.format.formatar_valor_real(float(val))
            
            data_recebimento = result['data_recebimento']
            data_recebimento = data_recebimento.strftime("%d/%m/%Y")
            result['data_recebimento'] = data_recebimento
            
            #result = list(result.values())
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
            sucesso, res = self.repo_receitas.buscar(self.tree_view_recebimento_id_selecionado, None)
            if sucesso:
                self.ctk_combobox_var_organizacao.set(res.organizacao.nome)
                self.ctk_entry_var_id.set(res.id)
                self.ctk_entry_var_descricao.set(res.descricao)
                self.ctk_entry_var_data_receb.set(res.data_recebimento.strftime("%d/%m/%Y"))
                self.ctk_entry_var_valor.set(res.valor)
                self.frame_recebimento_textbox_obs.configure(state=tk.NORMAL)
                self.frame_recebimento_textbox_obs.delete("1.0", "end") 
                if (res.observacoes != None and res.observacoes != ""):
                    self.frame_recebimento_textbox_obs.insert("1.0", res.observacoes)
                self.frame_recebimento_textbox_obs.configure(state=tk.DISABLED)
            else:
                messagebox.showinfo("Atenção", f"{res}. O ID {id} não está presente na tabela")
                        
    def filtrar_bind(self, event):
        self.filtrar()

    def filtrar(self):
        filtro = self.frame_entry_filtro.get().lower()
        if filtro:
            items = []
            for item in self.data_filtro_original:
                novo_item = [item.get(atributo, None) for atributo in self.colunas_tree_view]
                if any(str(value).lower().find(filtro) != -1 for value in novo_item):
                    items.append(novo_item)
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
            self.button_novo.configure(state=tk.DISABLED)
            self.button_altera.configure(state=tk.DISABLED)
            self.button_excluir.configure(state=tk.DISABLED) 
            self.button_cancelar.configure(state=tk.NORMAL)
            self.button_salvar.configure(state=tk.NORMAL)
            self.next_button.configure(state=tk.DISABLED)
            self.prev_button.configure(state=tk.DISABLED)
            self.first_button.configure(state=tk.DISABLED)
            self.last_button.configure(state=tk.DISABLED)       
            self.tree_view_recebimento.configure(selectmode="none")
            self.frame_entry_filtro.configure(state=tk.DISABLED)
            self.habilita_desabilita_entry(tk.NORMAL)
            
        if self.acao == 2:#altera
            self.button_novo.configure(state=tk.DISABLED)
            self.button_altera.configure(state=tk.DISABLED)
            self.button_excluir.configure(state=tk.DISABLED) 
            self.button_cancelar.configure(state=tk.NORMAL)
            self.button_salvar.configure(state=tk.NORMAL)
            self.next_button.configure(state=tk.DISABLED)
            self.prev_button.configure(state=tk.DISABLED)
            self.first_button.configure(state=tk.DISABLED)
            self.last_button.configure(state=tk.DISABLED)             
            self.tree_view_recebimento.configure(selectmode="none")
            self.frame_entry_filtro.configure(state=tk.DISABLED)            
            self.habilita_desabilita_entry(tk.NORMAL)
            
        if self.acao == 3:#Salvar
            self.button_novo.configure(state=tk.NORMAL)
            self.button_altera.configure(state=tk.NORMAL)
            self.button_excluir.configure(state=tk.NORMAL) 
            self.button_cancelar.configure(state=tk.DISABLED)
            self.button_salvar.configure(state=tk.DISABLED)            
            self.tree_view_recebimento.configure(selectmode="browse")
            self.frame_entry_filtro.configure(state=tk.NORMAL)            
            self.habilita_desabilita_entry(tk.DISABLED)
            self.atualizar_estado_botoes_paginacao()    
            
        if self.acao == 4:#deletar
            self.button_novo.configure(state=tk.NORMAL)
            self.button_cancelar.configure(state=tk.DISABLED)
            self.button_salvar.configure(state=tk.DISABLED)       
            if len(self.tree_view_recebimento.get_children()) == 0:
                self.limpar()              
            verifica = True                 
            
        if self.acao == 5:#cancelar
            self.limpar()
            self.button_novo.configure(state=tk.NORMAL)
            self.button_cancelar.configure(state=tk.DISABLED)
            self.button_salvar.configure(state=tk.DISABLED)
            self.tree_view_recebimento.configure(selectmode="browse")
            self.frame_entry_filtro.configure(state=tk.NORMAL)            
            self.habilita_desabilita_entry(tk.DISABLED)
            self.selecionar_linha_tree_view_por_id()
            self.buscar()          
            verifica = True
            
        if self.acao == 6 or verifica:
            verifica = False
            self.button_salvar.configure(state=tk.DISABLED)
            self.button_cancelar.configure(state=tk.DISABLED)
            
            if len(self.tree_view_recebimento.get_children()) == 0:
                self.button_excluir.configure(state=tk.DISABLED) 
                self.button_altera.configure(state=tk.DISABLED)           
            else:        
                item = self.tree_view_recebimento.focus()
                if item:
                    self.button_excluir.configure(state=tk.NORMAL)
                    self.button_altera.configure(state=tk.NORMAL)  
                else:
                    self.button_excluir.configure(state=tk.DISABLED)
                    self.button_altera.configure(state=tk.DISABLED)  
            self.atualizar_estado_botoes_paginacao()        
           
