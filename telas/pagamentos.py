import customtkinter as ct
import tkinter as tk
from Utils import formatacao
from Utils import paginacao as page
from tkinter import ttk
from tkinter import messagebox
from CTkToolTip import *
from dotenv import load_dotenv
import os
from infra.repository.despesas_repository import DespesasRepository
from infra.repository.organizacoes_repository import OrganizacoesRepository
from telas import pdfview, relatorios, toolbar

class Pagamentos():
    def __init__(self):
        load_dotenv()
        self.paginar_tree_view = int(os.getenv('PAGINACAO'))
        self.tamanho_pagina    = int(os.getenv('TAMANHO_PAGINA'))
        self.listar(self)
        super().__init__()
        
    def listar(self, tupla):
        self.repo_despesas = DespesasRepository()
        sucesso, self.lista_contas_pagar = self.repo_despesas.listar(tupla)
        if sucesso == False:
            messagebox.showerror("Erro", self.lista_contas_pagar)
            self.lista_contas_pagar = []
        return sucesso
        
    def pagar(self,frame_pagamento):
        
        self.format = formatacao.Util()    
        
        self.listar(True)
        
        self.nome_coluna_ordenar = "descricao" #ordenação default
        self.colunas_data   = ["data_pagamento", "data_vencimento"] # Nome das colunas do tipo data
        self.colunas_numericas = ["id", "valor", "valor_pago"] # nome das colunas do tipo numérico
        self.colunas_tree_view  = ["id", "descricao", "data_pagamento", "data_vencimento","valor","valor_pago"] # colunas do tree view
        self.ordenacao_colunas = {"id": "crescente", "descricao": "crescente", "data_pagamento": "crescente", "data_vencimento": "crescente", "valor": "crescente", "valor_pago": "crescente"}        
        
        self.tree_view_pagamento = ttk.Treeview(frame_pagamento)      
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10, "bold"))
        self.tree_view_pagamento['columns'] = tuple(self.colunas_tree_view)
        self.tree_view_pagamento.column("#0", width=0, stretch=False)
        self.tree_view_pagamento.column("id",  width=50)
        self.tree_view_pagamento.column("descricao",  width=300)
        self.tree_view_pagamento.column("data_pagamento", anchor="center", width=130)
        self.tree_view_pagamento.column("data_vencimento", anchor="center", width=130)
        self.tree_view_pagamento.column("valor", anchor="e", width=150)
        self.tree_view_pagamento.column("valor_pago", anchor="e", width=150)
        self.tree_view_pagamento.heading("id", text="ID", command=lambda: self.ordenar_por_coluna_click_cabecalho("id"))
        self.tree_view_pagamento.heading("descricao", text="Descrição", command=lambda: self.ordenar_por_coluna_click_cabecalho("descricao"))
        self.tree_view_pagamento.heading("data_pagamento", text="Data Pagamento", command=lambda: self.ordenar_por_coluna_click_cabecalho("data_pagamento"))
        self.tree_view_pagamento.heading("data_vencimento", text="Data Vencimento", command=lambda: self.ordenar_por_coluna_click_cabecalho("data_vencimento"))
        self.tree_view_pagamento.heading("valor",  text="Valor", command=lambda: self.ordenar_por_coluna_click_cabecalho("valor"))
        self.tree_view_pagamento.heading("valor_pago",  text="Valor Pago", command=lambda: self.ordenar_por_coluna_click_cabecalho("valor_pago"))
        self.tree_view_pagamento.bind("<Button-1>", lambda event: self.on_item_double_click_bind(event)) 
        self.tree_view_pagamento.bind("<KeyPress>", lambda event: self.on_item_double_click_bind(event)) 
        self.tree_view_pagamento.tag_configure('orow', background='#EEEEEE')        
        
        self.idx_coluna_id = 0
        self.tree_view_pagamento_id_selecionado = 0
        self.paginacao = page.PaginatedTreeView(self.tamanho_pagina, 
                                                0, 
                                                self.paginar_tree_view, 
                                                self.nome_coluna_ordenar, 
                                                self.colunas_data, 
                                                self.colunas_numericas, 
                                                self.colunas_tree_view, 
                                                self.ordenacao_colunas,
                                                self.tree_view_pagamento,
                                                self.lista_contas_pagar,
                                                self.idx_coluna_id,
                                                self.tree_view_pagamento_id_selecionado
                                                )
        
        self.label = ct.CTkLabel(frame_pagamento, text="Contas à Pagar", font=ct.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=10)        
        
        self.frame_pagamento_label_organizacao = ct.CTkLabel(frame_pagamento, text="Organização:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_organizacao.grid(row=1, column=0, padx=10, pady=5, sticky="w")            
        self.frame_pagamento_label_descricao = ct.CTkLabel(frame_pagamento, text="Descrição:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_descricao.grid(row=2, column=0, padx=10, pady=5, sticky="w")    
        
        self.frame_pagamento_label_data_venc = ct.CTkLabel(frame_pagamento, text="Data Vencimento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_data_venc.grid(row=3, column=0, padx=10, pady=5 ,sticky="w")   

        self.frame_pagamento_label_data_pag = ct.CTkLabel(frame_pagamento, text="Data Pagamento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_data_pag.grid(row=3, column=1, padx=170, pady=5 ,sticky="w")  
        
        self.frame_pagamento_label_valor = ct.CTkLabel(frame_pagamento, text="Valor:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_valor.grid(row=3, column=1, padx=460, pady=5 ,sticky="w") 
        
        self.frame_pagamento_label_valor_pag = ct.CTkLabel(frame_pagamento, text="Valor Pago:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_valor_pag.grid(row=3, column=1, padx=680, pady=5 ,sticky="w")       
        
        self.frame_pagamento_label_obs = ct.CTkLabel(frame_pagamento, text="Observações:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_obs.grid(row=4, column=0, padx=10, pady=5 ,sticky="w")              
                
        #INPUTS
        self.ctk_entry_var_descricao = tk.StringVar()
        self.ctk_entry_var_id = tk.StringVar()
        self.ctk_entry_var_data_venc = tk.StringVar()
        self.ctk_entry_var_data_pag = tk.StringVar()
        self.ctk_entry_var_valor = tk.StringVar()
        self.ctk_entry_var_valor_pago = tk.StringVar()
        self.ctk_entry_var_obs = tk.StringVar()
        self.ctk_combobox_var_organizacao = tk.StringVar()
        self.ctk_entry_var_valor_total = tk.StringVar()
        self.ctk_entry_var_valor_pago_total = tk.StringVar()   
        self.ctk_entry_var_filtro = tk.StringVar()       
                
        self.repo_org = OrganizacoesRepository()
        sucesso, organizacoes = self.repo_org.listar(True)
        
        self.frame_pagamento_combobox_organizacoes = ct.CTkComboBox(frame_pagamento, values=[item['nome'] for item in organizacoes], width=905,
                                                                        command=self.selecionar_organizacao, variable=self.ctk_combobox_var_organizacao)
        self.frame_pagamento_combobox_organizacoes.grid(row=1, column=1, padx=10, pady=5, sticky="w") 
        self.frame_pagamento_combobox_organizacoes.tabindex = 1
        
        self.frame_pagamento_entry_descricao = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_descricao, height=30, width=905)
        self.frame_pagamento_entry_descricao.grid(row=2, column=1, padx=10, pady=5, sticky="w") 
        self.frame_pagamento_entry_descricao.tabindex = 2
        self.frame_pagamento_entry_descricao.bind("<Tab>", self.format.mover_foco)
        
        self.frame_pagamento_entry_data_venc = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_data_venc, height=30, width=150)
        self.frame_pagamento_entry_data_venc.grid(row=3, column=1, padx=10, pady=5, sticky="w")     
        self.frame_pagamento_entry_data_venc.bind("<KeyPress>", lambda event: self.format.formatar_data(event, self.frame_pagamento_entry_data_venc))          
        self.frame_pagamento_entry_data_venc.tabindex = 3
        self.frame_pagamento_entry_data_venc.bind("<Tab>", self.format.mover_foco)
        
        self.frame_pagamento_entry_data_pag = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_data_pag, height=30, width=150)
        self.frame_pagamento_entry_data_pag.grid(row=3, column=1, padx=290, pady=5, sticky="w")     
        self.frame_pagamento_entry_data_pag.bind("<KeyPress>", lambda event: self.format.formatar_data(event, self.frame_pagamento_entry_data_pag))  
        self.frame_pagamento_entry_data_pag.tabindex = 4
        self.frame_pagamento_entry_data_pag.bind("<Tab>", self.format.mover_foco)
        
        self.frame_pagamento_entry_valor= ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor, height=30, width=150, justify="right")
        self.frame_pagamento_entry_valor.grid(row=3, column=1, padx=510, pady=5, sticky="w")   
        self.frame_pagamento_entry_valor.bind("<KeyPress>", lambda event: self.format.formatar_valor(event, self.frame_pagamento_entry_valor))
        self.frame_pagamento_entry_valor.tabindex = 5
        self.frame_pagamento_entry_valor.bind("<Tab>", self.format.mover_foco)
        
        self.frame_pagamento_entry_valor_pago= ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor_pago, height=30, width=150, justify="right")
        self.frame_pagamento_entry_valor_pago.grid(row=3, column=1, padx=765, pady=5, sticky="w")   
        self.frame_pagamento_entry_valor_pago.bind("<KeyPress>", lambda event: self.format.formatar_valor(event, self.frame_pagamento_entry_valor_pago))  
        self.frame_pagamento_entry_valor_pago.tabindex = 6
        self.frame_pagamento_entry_valor_pago.bind("<Tab>", self.format.mover_foco)
        
        self.frame_pagamento_textbox_obs = ct.CTkTextbox(frame_pagamento,  width=910, height=100, border_width=2)
        self.frame_pagamento_textbox_obs.grid(row=4, column=1, padx=10, pady=5, sticky="w")     
        self.frame_pagamento_textbox_obs.tabindex = 7
        self.frame_pagamento_textbox_obs.bind("<Tab>", self.format.mover_foco)
        
        #BOTÕES DE AÇÃO    
        bar = toolbar.toolbar() 
        bar.botoes_acao(self, frame_pagamento, 80, 28, 5, 1, 'w', 5, 10, 95, 180, 265,350, 6, 1, 630, 5, "w",250, 30,675, 1)
        # TREE
        self.tree_view_pagamento.grid(row=7, column=1, columnspan=4, rowspan=5, padx=10, pady=1, sticky="w")
        
        #TOTALIZADORES
        valor_total = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor_total, border_width=0, justify="right",
                                    height=30, width=150, state=tk.DISABLED, font=ct.CTkFont(size=14, weight="bold"))      
        valor_total.grid(row=20, column=1, padx=615, pady=1, sticky="w")
        valor_total_pago = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor_pago_total, border_width=0, justify="right",
                                    height=30, width=150, state=tk.DISABLED, font=ct.CTkFont(size=14, weight="bold"))  
        valor_total_pago.grid(row=20, column=1, padx=775, pady=1, sticky="w")     
        
        
        #BOTOES DE NAVEGAÇÃO CRIADOS E CONFIGURADOS EM PAGINACAO
        self.paginacao.navegacao(self,frame_pagamento, self.paginar_tree_view, 60, 28, 20, 1, "w",1, 10, 75, 140, 205, 300)
        
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
        self.ctk_entry_var_data_venc.set("")
        self.ctk_entry_var_data_pag.set("")
        self.ctk_entry_var_valor.set("")
        self.ctk_entry_var_valor_pago.set("")
        self.frame_pagamento_textbox_obs.delete("1.0", "end") 
        self.acao = 7
    
    def cancelar(self):
        self.acao = 5
        self.controla_botoes()
        
        
    def remover(self):
        desc = str(self.ctk_entry_var_descricao.get())
        resposta = messagebox.askyesno("Confirmação", f"Deseja excluir a despesa {desc}?")
        if (resposta):      
            id = str(self.ctk_entry_var_id.get())
            if (self.repo_despesas.delete(id)):
                self.acao = 4
                self.listar(True)                 
                self.update_tree_view()         
            
    def salvar(self):
        id          = str(self.ctk_entry_var_id.get())
        desc        = str(self.ctk_entry_var_descricao.get())
        data_pag    = str(self.ctk_entry_var_data_pag.get())
        data_venc   = str(self.ctk_entry_var_data_venc.get())
        valor       = str(self.ctk_entry_var_valor.get())
        valor_pago  = str(self.ctk_entry_var_valor_pago.get())
        obs         = str(self.frame_pagamento_textbox_obs.get('1.0', 'end'))  
        org         = str(self.ctk_combobox_var_organizacao.get())
        
        valor = valor.replace("R$","").replace(",","").replace(" ","")
        valor_pago = valor_pago.replace("R$","").replace(",","").replace(" ","")
        
        if desc == "":
            messagebox.showinfo("Informação", "O campo organização é de preenchimento obrigatório")
            self.frame_pagamento_entry_descricao.focus()
            return False        
        if desc == "":
            messagebox.showinfo("Informação", "O campo descrição é de preenchimento obrigatório")
            self.frame_pagamento_entry_descricao.focus()
            return False
        if data_venc == "":
            messagebox.showinfo("Informação", "O campo data do vencimento é de preenchimento obrigatório")
            self.frame_pagamento_entry_data_venc.focus()
            return False        
        if data_pag == "":
            messagebox.showinfo("Informação", "O campo data do pagamento é de preenchimento obrigatório")
            self.frame_pagamento_entry_data_pag.focus()
            return False
        if valor == "":
            messagebox.showinfo("Informação", "O campo valor é de preenchimento obrigatório")
            self.frame_pagamento_entry_valor.focus()
            return False
        if valor_pago == "":
            messagebox.showinfo("Informação", "O campo valor pago é de preenchimento obrigatório")
            self.frame_pagamento_entry_valor_pago.focus()
            return False
        
        sucesso, objects = self.repo_despesas.insert_update(id, desc, data_pag, data_venc,valor, valor_pago, obs, org)
        if (sucesso):  
            resposta = messagebox.askyesno("Confirmação", f"Confirma {' inclusão' if not id else 'alteração'} dessa despesa?")
            if resposta:    
                self.listar(True)
                if id == "":
                    messagebox.showinfo("Sucesso", f"Despesa inserida com sucesso")
                    self.ctk_entry_var_filtro.set("")
                    if (objects != None):
                        self.tree_view_pagamento_id_selecionado = objects
                    else:
                        self.tree_view_pagamento_id_selecionado = self.lista_contas_pagar[len(self.lista_contas_pagar)-1]['id']
                else:
                    messagebox.showinfo("Sucesso", f"Despesa alterada com sucesso")
                
                self.paginacao.verificar_pagina_item = True
                self.acao = 3
                self.update_tree_view() 
                self.paginacao.verificar_pagina_item = False
        else:
            messagebox.showerror("Erro", objects)                
            
        
    def update_tree_view(self):
        vl_tot = 0.0
        vlp_tot = 0.0
        for data in self.tree_view_pagamento.get_children():
            self.tree_view_pagamento.delete(data) 
            
        self.data_filtro_original = []
        for result in self.lista_contas_pagar:
            val = result['valor']
            vl_tot = vl_tot + float(val)
            result['valor'] = self.format.formatar_valor_real(float(val))
                
            val = result['valor_pago']
            vlp_tot = vlp_tot + float(val)
            result['valor_pago'] = self.format.formatar_valor_real(float(val))
            
            data_pagamento = result['data_pagamento']
            data_pagamento = data_pagamento.strftime("%d/%m/%Y")
            result['data_pagamento'] = data_pagamento
            
            data_vencimento = result['data_vencimento']
            data_vencimento = data_vencimento.strftime("%d/%m/%Y")
            result['data_vencimento'] = data_vencimento            
                                
            #result = list(result.values())
            #Para auxiliar no buscar
            self.data_filtro_original.append(result)  

            
        #TOTALIZADORES
        self.ctk_entry_var_valor_total.set( self.format.formatar_valor_real(vl_tot)  )
        self.ctk_entry_var_valor_pago_total.set( self.format.formatar_valor_real(vlp_tot) )
        
        if self.acao == 4:
            self.tree_view_pagamento_id_selecionado = 0
            self.paginacao.tree_view_id_selecionado = self.tree_view_pagamento_id_selecionado
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
            item = self.tree_view_pagamento.identify('item', event.x, event.y)
            if item:
                self.tree_view_pagamento.selection_set(item)
                self.tree_view_pagamento.focus(item)                
                self.on_item_double_click()
            else:
                if event.keysym in ('Up', 'Down'):
                    if event.keysym == 'Up':
                        item = self.tree_view_pagamento.prev(self.tree_view_pagamento.focus())
                    elif event.keysym == 'Down':
                        item = self.tree_view_pagamento.next(self.tree_view_pagamento.focus())

                    if item:
                        self.tree_view_pagamento.selection_set(item)
                        self.tree_view_pagamento.focus(item)                        
                        self.on_item_double_click()
        
    def on_item_double_click(self):
        self.buscar()
        self.controla_botoes()
        
    def buscar(self):    
        if len(self.tree_view_pagamento.selection()) > 0:
            item = self.tree_view_pagamento.selection()[0]
            values = self.tree_view_pagamento.item(item, 'values')
            self.tree_view_pagamento_id_selecionado = values[0]
            self.paginacao.tree_view_id_selecionado = self.tree_view_pagamento_id_selecionado
            sucesso, res = self.repo_despesas.buscar(self.tree_view_pagamento_id_selecionado, None)
                        
            if sucesso:
                self.ctk_combobox_var_organizacao.set(res.organizacao.nome)
                self.ctk_entry_var_id.set(res.id)
                self.ctk_entry_var_descricao.set(res.descricao)
                self.ctk_entry_var_data_venc.set(res.data_vencimento.strftime("%d/%m/%Y"))
                self.ctk_entry_var_data_pag.set(res.data_pagamento.strftime("%d/%m/%Y"))
                self.ctk_entry_var_valor.set(res.valor)
                self.ctk_entry_var_valor_pago.set(res.valor_pago)
                self.frame_pagamento_textbox_obs.configure(state=tk.NORMAL)
                self.frame_pagamento_textbox_obs.delete("1.0", "end") 
                if (res.observacoes != None and res.observacoes != ""):
                    self.frame_pagamento_textbox_obs.insert("1.0", res.observacoes)
                self.frame_pagamento_textbox_obs.configure(state=tk.DISABLED)
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
                    self.tree_view_pagamento_id_selecionado = items[0][0]
                    self.paginacao.tree_view_id_selecionado = self.tree_view_pagamento_id_selecionado
            self.atualizar_treeview(items)
                          
        else:
            #self.atualizar_treeview(self.data_filtro_original)
            self.monta_paginacao(False)
            self.tree_view_pagamento_id_selecionado = 0
            self.paginacao.tree_view_id_selecionado = self.tree_view_pagamento_id_selecionado            
            self.selecionar_linha_tree_view_por_id()   
            self.on_item_double_click()       
            
    def atualizar_treeview(self, items):
        self.tree_view_pagamento.delete(*self.tree_view_pagamento.get_children())
        tot = 0
        tot_p = 0
        for item in items:
            val = item[4]
            val = val.replace("R$","").replace(" ","").replace(".","").replace(",",".")
            tot = tot + float(val)
            
            val = item[5]
            val = val.replace("R$","").replace(" ","").replace(".","").replace(",",".")
            tot_p = tot_p + float(val)
            
            self.tree_view_pagamento.insert("", "end", values=item )  
            
        self.paginacao.idx_coluna_id            = self.idx_coluna_id
        self.paginacao.tree_view_paginada = self.tree_view_pagamento
        self.selecionar_linha_tree_view_por_id()
        self.tree_view_pagamento = self.paginacao.tree_view_paginada
        self.on_item_double_click()

        self.ctk_entry_var_valor_total.set( self.format.formatar_valor_real(tot)  )
        self.ctk_entry_var_valor_pago_total.set( self.format.formatar_valor_real(tot_p) )
        self.acao = 6
        self.controla_botoes()
    
    
    def selecionar_organizacao(self, selected):
        self.ctk_combobox_var_organizacao.set( selected)


    def ordenar_por_coluna_click_cabecalho(self, coluna):
        self.nome_coluna_ordenar = coluna
        self.paginacao.nome_coluna_ordenar      = self.nome_coluna_ordenar
        self.paginacao.ordencao(True)
        self.on_item_double_click()
        self.paginacao.tree_view_id_selecionado = self.tree_view_pagamento_id_selecionado
        self.paginacao.idx_coluna_id            = self.idx_coluna_id        
        self.selecionar_linha_tree_view_por_id()
        
    def selecionar_linha_tree_view_por_id(self):
        self.paginacao.selecionar_linha_tree_view_por_id()
        self.tree_view_pagamento = self.paginacao.tree_view_paginada
        
    def monta_paginacao(self, alternar_ascendencia):
        self.paginacao.tree_view_paginada       = self.tree_view_pagamento
        self.paginacao.dados_all                = self.lista_contas_pagar
        self.paginacao.tree_view_id_selecionado = self.tree_view_pagamento_id_selecionado
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
        self.frame_pagamento_combobox_organizacoes.configure(state=state)
        self.frame_pagamento_entry_descricao.configure(state=state)
        self.frame_pagamento_entry_data_pag.configure(state=state)
        self.frame_pagamento_entry_data_venc.configure(state=state)
        self.frame_pagamento_entry_valor.configure(state=state)
        self.frame_pagamento_entry_valor_pago.configure(state=state)
        self.frame_pagamento_textbox_obs.configure(state=state)
            
    def controla_botoes(self):
        verifica = False
        
        if self.paginar_tree_view == 1:
            if len(self.tree_view_pagamento.get_children()) <= int(self.tamanho_pagina ):
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
            self.tree_view_pagamento.configure(selectmode="none")
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
            self.tree_view_pagamento.configure(selectmode="none")
            self.frame_entry_filtro.configure(state=tk.DISABLED)            
            self.habilita_desabilita_entry(tk.NORMAL)
            
        if self.acao == 3:#Salvar
            self.button_novo.configure(state=tk.NORMAL)
            self.button_altera.configure(state=tk.NORMAL)
            self.button_excluir.configure(state=tk.NORMAL) 
            self.button_cancelar.configure(state=tk.DISABLED)
            self.button_salvar.configure(state=tk.DISABLED)            
            self.tree_view_pagamento.configure(selectmode="browse")
            self.frame_entry_filtro.configure(state=tk.NORMAL)            
            self.habilita_desabilita_entry(tk.DISABLED)
            self.atualizar_estado_botoes_paginacao()    
            
        if self.acao == 4:#deletar
            self.button_novo.configure(state=tk.NORMAL)
            self.button_cancelar.configure(state=tk.DISABLED)
            self.button_salvar.configure(state=tk.DISABLED)  
            if len(self.tree_view_pagamento.get_children()) == 0:
                self.limpar()                 
            verifica = True                 
            
        if self.acao == 5:#cancelar
            self.limpar()
            self.button_novo.configure(state=tk.NORMAL)
            self.button_cancelar.configure(state=tk.DISABLED)
            self.button_salvar.configure(state=tk.DISABLED)
            self.tree_view_pagamento.configure(selectmode="browse")
            self.frame_entry_filtro.configure(state=tk.NORMAL)            
            self.habilita_desabilita_entry(tk.DISABLED)
            self.selecionar_linha_tree_view_por_id()
            self.buscar()          
            verifica = True
            
        if self.acao == 6 or verifica:
            verifica = False
            self.button_salvar.configure(state=tk.DISABLED)
            self.button_cancelar.configure(state=tk.DISABLED)
            
            if len(self.tree_view_pagamento.get_children()) == 0:
                self.button_excluir.configure(state=tk.DISABLED) 
                self.button_altera.configure(state=tk.DISABLED)           
            else:        
                item = self.tree_view_pagamento.focus()
                if item:
                    self.button_excluir.configure(state=tk.NORMAL)
                    self.button_altera.configure(state=tk.NORMAL)  
                else:
                    self.button_excluir.configure(state=tk.DISABLED)
                    self.button_altera.configure(state=tk.DISABLED)  
            self.atualizar_estado_botoes_paginacao()        
           
