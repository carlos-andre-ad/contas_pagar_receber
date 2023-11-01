import customtkinter as ct
import tkinter as tk
from DB.entidades import contas_pagar as cp
from DB.entidades import pessoa
from Utils import formatacao
from tkinter import ttk
from tkinter import messagebox
from CTkToolTip import *



class Pagamentos():
    def __init__(self):
        super().__init__()
        
    def pagar(self,frame_pagamento):
        
        self.contasPagar = cp.ContasPagar()
        self.format = formatacao.Util()
        
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
                
        p = pessoa.Pessoa()
        self.organizacoes = p.listar(True)
        
        self.frame_pagamento_combobox_organizacoes = ct.CTkComboBox(frame_pagamento, values=[item['nome'] for item in self.organizacoes],
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
        
        self.frame_pagamento_button_novo = ct.CTkButton(frame_pagamento, text="Novo", command=self.novo,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_novo.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        CTkToolTip(self.frame_pagamento_button_novo, delay=0.5, message="Inicia um novo lançamento!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        self.frame_pagamento_button_salvar = ct.CTkButton(frame_pagamento, text="Salvar", command=self.salvar, compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_salvar.grid(row=5, column=1, padx=150, pady=5, sticky="w")   
        CTkToolTip(self.frame_pagamento_button_salvar, delay=0.5, message="Inclui um novo lançamento ou altera o existe!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
               
        self.frame_pagamento_button_excluir = ct.CTkButton(frame_pagamento, text="Excluir", command=self.remover, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_excluir.grid(row=5, column=1, padx=295, pady=5, sticky="w")     
        self.frame_pagamento_button_excluir.configure(state=tk.DISABLED) 
        CTkToolTip(self.frame_pagamento_button_excluir, delay=0.5, message="Exclui lançamento selecionado!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        #INPUT FILTRAR
        self.frame_label_filtro = ct.CTkLabel(frame_pagamento, text="Filtro:",  compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_label_filtro.grid(row=6, column=1, padx=630, pady=5 ,sticky="w")         
        self.frame_entry_filtro = ct.CTkEntry(frame_pagamento, height=30, width=250, textvariable=self.ctk_entry_var_filtro)
        self.frame_entry_filtro.grid(row=6, column=1, padx=675, pady=1, sticky="w")       
        self.frame_entry_filtro.bind("<KeyRelease>", self.filtrar_bind)
        
        self.tree_view_data = ttk.Treeview(frame_pagamento)      
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10, "bold"))
        
        self.ordenacao_colunas = {"ID": "crescente", "descricao": "crescente", "data_pagamento": "crescente", "data_vencimento": "crescente", "valor": "crescente", "valor_pago": "crescente"}
        self.tree_view_data['columns'] = ("ID", "descricao", "data_pagamento", "data_vencimento","valor","valor_pago")
        self.tree_view_data.column("#0", width=0, stretch=False)
        self.tree_view_data.column("ID",  width=50)
        self.tree_view_data.column("descricao",  width=300)
        self.tree_view_data.column("data_pagamento", anchor="center", width=130)
        self.tree_view_data.column("data_vencimento", anchor="center", width=130)
        self.tree_view_data.column("valor", anchor="e", width=150)
        self.tree_view_data.column("valor_pago", anchor="e", width=150)
        self.tree_view_data.heading("ID", text="ID", command=lambda: self.ordenar_por_coluna("ID"))
        self.tree_view_data.heading("descricao", text="Descrição", command=lambda: self.ordenar_por_coluna("descricao"))
        self.tree_view_data.heading("data_pagamento", text="Data Pagamento", command=lambda: self.ordenar_por_coluna("data_pagamento"))
        self.tree_view_data.heading("data_vencimento", text="Data Vencimento", command=lambda: self.ordenar_por_coluna("data_vencimento"))
        self.tree_view_data.heading("valor",  text="Valor", command=lambda: self.ordenar_por_coluna("valor"))
        self.tree_view_data.heading("valor_pago",  text="Valor Pago", command=lambda: self.ordenar_por_coluna("valor_pago"))
        self.tree_view_data.bind("<Double-1>", lambda event: self.on_item_double_click()) 
        self.tree_view_data.tag_configure('orow', background='#EEEEEE')
        self.tree_view_data.grid(row=7, column=1, columnspan=4, rowspan=5, padx=10, pady=1, sticky="w")
        
        #TOTALIZADORES
        valor_total = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor_total, border_width=0, justify="right",
                                    height=30, width=150, state=tk.DISABLED, font=ct.CTkFont(size=14, weight="bold"))      
        valor_total.grid(row=20, column=1, padx=615, pady=1, sticky="w")
        valor_total_pago = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor_pago_total, border_width=0, justify="right",
                                    height=30, width=150, state=tk.DISABLED, font=ct.CTkFont(size=14, weight="bold"))  
        valor_total_pago.grid(row=20, column=1, padx=775, pady=1, sticky="w")             

        #Preenche tree view
        lst = self.contasPagar.listar(True)
        self.tree_view_data_id_selecionado = 0
        self.acao = 4 #1=inserir, 2=atualizar, 3=deletar, 4=listar
        self.update_tree_view(lst)
           
           
    def novo(self):
        self.ctk_entry_var_id.set("")
        self.ctk_entry_var_descricao.set("")
        self.ctk_entry_var_data_venc.set("")
        self.ctk_entry_var_data_pag.set("")
        self.ctk_entry_var_valor.set("")
        self.ctk_entry_var_valor_pago.set("")
        self.frame_pagamento_textbox_obs.delete("1.0", "end") 
        self.frame_pagamento_textbox_obs.insert("1.0", "")  
        self.frame_pagamento_button_excluir.configure(state=tk.DISABLED)    
        
        
    def remover(self):
        desc = str(self.ctk_entry_var_descricao.get())
        resposta = messagebox.askyesno("Confirmação", f"Deseja excluir a despesa {desc}?")
        if (resposta):      
            id = str(self.ctk_entry_var_id.get())
            if (self.contasPagar.delete(id)):
                self.acao = 3
                lst = self.contasPagar.listar(True) 
                if len(lst) > 0:
                    self.tree_view_data_id_selecionado = lst[0]['id']                   
                self.update_tree_view(lst)               
            
    def salvar(self):
        id          = str(self.ctk_entry_var_id.get())
        desc        = str(self.ctk_entry_var_descricao.get())
        data_pag    = str(self.ctk_entry_var_data_pag.get())
        data_venc   = str(self.ctk_entry_var_data_venc.get())
        valor       = str(self.ctk_entry_var_valor.get())
        valor_pago  = str(self.ctk_entry_var_valor_pago.get())
        obs         = str(self.ctk_entry_var_obs.get())  
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
        
        if (self.contasPagar.insert_update(id, desc, data_pag, data_venc,valor, valor_pago, obs, org)):   
            lst = self.contasPagar.listar(True)
            if id == "":
                self.acao = 1
                messagebox.showinfo("Sucesso", f"Despesa inserida com sucesso")
                self.ctk_entry_var_filtro.set("")  
                self.tree_view_data_id_selecionado = lst[len(lst)-1]['id']             
            else:
                self.acao = 2
                messagebox.showinfo("Sucesso", f"Despesa alterada com sucesso") 
            self.update_tree_view( lst ) 
            
        
    def update_tree_view(self, lst):
        vl_tot = 0.0
        vlp_tot = 0.0
        
        for data in self.tree_view_data.get_children():
            self.tree_view_data.delete(data) 
                        
        for result in lst:
            val = result['valor']
            vl_tot = vl_tot + float(val)
            result['valor'] = self.format.formatar_valor_real(float(val))
                
            val = result['valor_pago']
            vlp_tot = vlp_tot + float(val)
            result['valor_pago'] = self.format.formatar_valor_real(float(val))
                                
            result = list(result.values())
            self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")
            
        #TOTALIZADORES
        self.ctk_entry_var_valor_total.set( self.format.formatar_valor_real(vl_tot)  )
        self.ctk_entry_var_valor_pago_total.set( self.format.formatar_valor_real(vlp_tot) )
        
        self.data_original = [self.tree_view_data.item(item)["values"] for item in self.tree_view_data.get_children()] 
        
        self.filtrar()
        self.selecionar_linha_tree_view_por_id()
        self.ordenacao_colunas['descricao'] = 'decrescente'
        self.ordenar_por_coluna("descricao")           
        
        
    def selecionar_linha_tree_view_por_id(self):
        tam = len(self.tree_view_data.get_children())
        if tam > 0:
            if int(self.tree_view_data_id_selecionado) <= 0:
                self.tree_view_data.selection_set(self.tree_view_data.get_children()[0])   
            else:       
                coluna_id = 0
                for item in self.tree_view_data.get_children():
                    valores = self.tree_view_data.item(item, 'values')
                    if valores and len(valores) > 0:
                        if int(valores[coluna_id]) == int(self.tree_view_data_id_selecionado):                            
                            self.tree_view_data.selection_set(item)
                            self.tree_view_data.focus(item)
                            self.tree_view_data.see(item)
                            break
            self.on_item_double_click() 
        else:
            self.novo()          
        
    def on_item_double_click(self):
        item = self.tree_view_data.selection()[0]
        values = self.tree_view_data.item(item, 'values')
        self.tree_view_data_id_selecionado = values[0]
        res = self.contasPagar.buscar(self.tree_view_data_id_selecionado, True)
        if res != None:
            self.ctk_combobox_var_organizacao.set(res['organizacao'])
            self.ctk_entry_var_id.set(res['id'])
            self.ctk_entry_var_descricao.set(res['descricao'])
            self.ctk_entry_var_data_venc.set(res['data_vencimento'])
            self.ctk_entry_var_data_pag.set(res['data_pagamento'])
            self.ctk_entry_var_valor.set(res['valor'])
            self.ctk_entry_var_valor_pago.set(res['valor_pago'])
            if (res['observacoes'] != "" and res['observacoes'] != None):
                self.frame_pagamento_textbox_obs.delete("1.0", "end") 
                self.frame_pagamento_textbox_obs.insert("1.0", res['observacoes']) 
            self.frame_pagamento_button_excluir.configure(state=tk.NORMAL) 
        else:
            messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
            
    def filtrar_bind(self, event):
        self.filtrar()

    def filtrar(self):
        filtro = self.frame_entry_filtro.get().lower()
        if filtro:
            items = []
            for item in self.data_original:
                if any(str(value).lower().find(filtro) != -1 for value in item):
                    items.append(item)
                    if self.acao != 2:
                        self.tree_view_data_id_selecionado = items[0][0]
            self.atualizar_treeview(items)
        else:
            self.atualizar_treeview(self.data_original)   
            
        self.ordenacao_colunas['descricao'] = 'decrescente'
        self.ordenar_por_coluna("descricao")                     
            
    def atualizar_treeview(self, items):
        self.tree_view_data.delete(*self.tree_view_data.get_children())
        tot = 0
        tot_p = 0
        for item in items:
            val = item[4]
            val = val.replace("R$","").replace(" ","").replace(".","").replace(",",".")
            tot = tot + float(val)
            
            val = item[5]
            val = val.replace("R$","").replace(" ","").replace(".","").replace(",",".")
            tot_p = tot_p + float(val)
                        
            self.tree_view_data.insert("", "end", values=item)  

        self.ctk_entry_var_valor_total.set( self.format.formatar_valor_real(tot)  )
        self.ctk_entry_var_valor_pago_total.set( self.format.formatar_valor_real(tot_p) )
        self.selecionar_linha_tree_view_por_id()
        self.acao = 4


    def selecionar_organizacao(self, selected):
        self.ctk_combobox_var_organizacao.set( selected)
        
    def ordenar_por_coluna(self, coluna):
        estado_atual = self.ordenacao_colunas[coluna]
        data = [(self.tree_view_data.set(item, coluna), item) for item in self.tree_view_data.get_children('')]
        data.sort(reverse=estado_atual == "crescente", key=lambda x: x[0].casefold())
        for index, (val, item) in enumerate(data):
            self.tree_view_data.move(item, '', index)
        self.ordenacao_colunas[coluna] = "crescente" if estado_atual == "decrescente" else "decrescente"
    
    
    