import customtkinter as ct
from CTkToolTip import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import DB.contas_pagar as cp
import DB.pessoa as pessoa
import Utils.formatacao as formatacao

   

class Pagamentos():
    def __init__(self):
        super().__init__()
        
    def pagar(self,frame_pagamento):
        
        self.label = ct.CTkLabel(frame_pagamento, text="Contas à Pagar", font=ct.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=10)        
        
        self.frame_pagamento_label_organizacao = ct.CTkLabel(frame_pagamento, text="Organização:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_organizacao.grid(row=1, column=0, padx=10, pady=5, sticky="w")            

        self.frame_pagamento_label_descricao = ct.CTkLabel(frame_pagamento, text="Descrição:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_descricao.grid(row=2, column=0, padx=10, pady=5, sticky="w")    
        
        self.frame_pagamento_label_data_venc = ct.CTkLabel(frame_pagamento, text="Data Vencimento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_data_venc.grid(row=3, column=0, padx=10, pady=5 ,sticky="w")   
               
        self.frame_pagamento_label_data_pag = ct.CTkLabel(frame_pagamento, text="Data Pagamento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_data_pag.grid(row=3, column=1, padx=180, pady=5 ,sticky="w")  
        
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
        
        format = formatacao.Util()
        p = pessoa.Pessoa()
        self.organizacoes = p.listar(True)
        
        self.frame_pagamento_combobox_organizacoes = ct.CTkComboBox(frame_pagamento, values=[item['nome'] for item in self.organizacoes],
                                                                        command=self.selecionar_organizacao, variable=self.ctk_combobox_var_organizacao)
        self.frame_pagamento_combobox_organizacoes.grid(row=1, column=1, padx=5, pady=5, sticky="w") 
        self.frame_pagamento_combobox_organizacoes.tabindex = 1
        
        self.frame_pagamento_entry_descricao = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_descricao, height=30, width=905)
        self.frame_pagamento_entry_descricao.grid(row=2, column=1, padx=5, pady=5, sticky="w") 
        self.frame_pagamento_entry_descricao.tabindex = 2
        self.frame_pagamento_entry_descricao.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_entry_data_venc = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_data_venc, height=30, width=150)
        self.frame_pagamento_entry_data_venc.grid(row=3, column=1, padx=5, pady=5, sticky="w")     
        self.frame_pagamento_entry_data_venc.bind("<KeyPress>", lambda event: format.formatar_data(event, self.frame_pagamento_entry_data_venc))          
        self.frame_pagamento_entry_data_venc.tabindex = 3
        self.frame_pagamento_entry_data_venc.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_entry_data_pag = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_data_pag, height=30, width=150)
        self.frame_pagamento_entry_data_pag.grid(row=3, column=1, padx=290, pady=5, sticky="w")     
        self.frame_pagamento_entry_data_pag.bind("<KeyPress>", lambda event: format.formatar_data(event, self.frame_pagamento_entry_data_pag))  
        self.frame_pagamento_entry_data_pag.tabindex = 4
        self.frame_pagamento_entry_data_pag.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_entry_valor= ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor, height=30, width=150)
        self.frame_pagamento_entry_valor.grid(row=3, column=1, padx=510, pady=5, sticky="w")   
        self.frame_pagamento_entry_valor.bind("<KeyPress>", lambda event: format.formatar_valor(event, self.frame_pagamento_entry_valor))
        self.frame_pagamento_entry_valor.tabindex = 5
        self.frame_pagamento_entry_valor.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_entry_valor_pago= ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor_pago, height=30, width=150)
        self.frame_pagamento_entry_valor_pago.grid(row=3, column=1, padx=760, pady=5, sticky="w")   
        self.frame_pagamento_entry_valor_pago.bind("<KeyPress>", lambda event: format.formatar_valor(event, self.frame_pagamento_entry_valor_pago))    
        self.frame_pagamento_entry_valor_pago.tabindex = 6
        self.frame_pagamento_entry_valor_pago.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_textbox_obs = ct.CTkTextbox(frame_pagamento,  width=910, height=100, border_width=2)
        self.frame_pagamento_textbox_obs.grid(row=4, column=1, padx=5, pady=5, sticky="w")     
        self.frame_pagamento_textbox_obs.tabindex = 7
        self.frame_pagamento_textbox_obs.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_button_novo = ct.CTkButton(frame_pagamento, text="Novo", command=self.novo,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_novo.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        CTkToolTip(self.frame_pagamento_button_novo, delay=0.5, message="Inicia um novo lançamento!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        self.frame_pagamento_button_salvar = ct.CTkButton(frame_pagamento, text="Salvar", command=self.salvar, compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_salvar.grid(row=5, column=1, padx=150, pady=5, sticky="w")   
        CTkToolTip(self.frame_pagamento_button_salvar, delay=0.5, message="Inclui um novo lançamento ou altera o existe!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
               
        self.frame_pagamento_button_excluir = ct.CTkButton(frame_pagamento, text="Excluir", command=self.remover, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_excluir.grid(row=5, column=1, padx=295, pady=5, sticky="w")     
        self.frame_pagamento_button_excluir.configure(state=tk.DISABLED) 
        CTkToolTip(self.frame_pagamento_button_excluir, delay=0.5, message="Exclui lançamento selecionado!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
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
        
        self.tree_view_data.bind("<Double-1>", lambda event: self.on_item_double_click(self.tree_view_data)) 
        self.tree_view_data.tag_configure('orow', background='#EEEEEE')
        self.tree_view_data.grid(row=6, column=1, columnspan=4, rowspan=5, padx=5, pady=30, sticky="w")
        
        rd = cp.ContasPagar()
        lst = rd.listar(False)
        for result in self.reverse(lst):
            self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")
        
        if len(lst) > 0: 
            self.tree_view_data.selection_set(self.tree_view_data.get_children()[0])   
            self.on_item_double_click(self.tree_view_data)

    def selecionar_organizacao(self, selected):
        self.ctk_combobox_var_organizacao.set( selected)
        
    def ordenar_por_coluna(self, coluna):
        estado_atual = self.ordenacao_colunas[coluna]
        data = [(self.tree_view_data.set(item, coluna), item) for item in self.tree_view_data.get_children('')]
        data.sort(reverse=estado_atual == "crescente", key=lambda x: x[0])
        for index, (val, item) in enumerate(data):
            self.tree_view_data.move(item, '', index)
        # Inverta o estado de ordenação para a próxima vez
        self.ordenacao_colunas[coluna] = "crescente" if estado_atual == "decrescente" else "decrescente"         
           
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
            dlt = cp.ContasPagar()
            if (dlt.delete(id)):
                for data in self.tree_view_data.get_children():
                    self.tree_view_data.delete(data)  
                        
                for result in self.reverse(dlt.listar(False)):
                    self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")   
                self.novo()             
            
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
        
        ins = cp.ContasPagar()
        if (ins.insert_update(id, desc, data_pag, data_venc,valor, valor_pago, obs, org)):
            for data in self.tree_view_data.get_children():
                self.tree_view_data.delete(data)    
                
            for result in self.reverse(ins.listar(False)):
                self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")  
            
            if id == "":
                messagebox.showinfo("Sucesso", f"Despesa inserida com sucesso")
            else:
                messagebox.showinfo("Sucesso", f"Despesa alterada com sucesso")
            self.novo()     
        
        
    def on_item_double_click(self, tree_view_data):
        item = tree_view_data.selection()[0]
        values = tree_view_data.item(item, 'values')
        id = values[0]
        bus = cp.ContasPagar()
        res = bus.buscar(id, True)
        if len(res) > 0:
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
            
    def reverse(self,tuples):
        new_tup = tuples[::-1]
        return new_tup   