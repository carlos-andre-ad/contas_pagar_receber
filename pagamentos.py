import customtkinter as ct
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import DB.contas_pagar as cp
import Utils.formatacao as formatacao
from PIL import Image
   

class Pagamentos():
    def __init__(self):
        super().__init__()
        
    def pagar(self,frame_pagamento):
        
        self.label = ct.CTkLabel(frame_pagamento, text="Contas à Pagar", font=ct.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=10)        

        self.frame_pagamento_label_descricao = ct.CTkLabel(frame_pagamento, text="Descrição:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_descricao.grid(row=1, column=0, padx=10, pady=5, sticky="w")    
        
        self.frame_pagamento_label_data_venc = ct.CTkLabel(frame_pagamento, text="Data Vencimento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_data_venc.grid(row=2, column=0, padx=10, pady=5 ,sticky="w")   
               
        self.frame_pagamento_label_data_pag = ct.CTkLabel(frame_pagamento, text="Data Pagamento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_data_pag.grid(row=2, column=1, padx=180, pady=5 ,sticky="w")  
        
        self.frame_pagamento_label_valor = ct.CTkLabel(frame_pagamento, text="Valor:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_valor.grid(row=2, column=1, padx=460, pady=5 ,sticky="w") 
        
        self.frame_pagamento_label_valor_pag = ct.CTkLabel(frame_pagamento, text="Valor Pago:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_valor_pag.grid(row=2, column=1, padx=680, pady=5 ,sticky="w")       
        
        self.frame_pagamento_label_obs = ct.CTkLabel(frame_pagamento, text="Observações:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_pagamento_label_obs.grid(row=3, column=0, padx=10, pady=5 ,sticky="w")              
                
        #INPUTS
        self.ctk_entry_var_descricao = tk.StringVar()
        self.ctk_entry_var_id = tk.StringVar()
        self.ctk_entry_var_data_venc = tk.StringVar()
        self.ctk_entry_var_data_pag = tk.StringVar()
        self.ctk_entry_var_valor = tk.StringVar()
        self.ctk_entry_var_valor_pago = tk.StringVar()
        self.ctk_entry_var_obs = tk.StringVar()
        
        format = formatacao.Util()
        
        self.frame_pagamento_entry_descricao = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_descricao, height=30, width=905)
        self.frame_pagamento_entry_descricao.grid(row=1, column=1, padx=5, pady=5, sticky="w") 
        self.frame_pagamento_entry_descricao.tabindex = 1
        self.frame_pagamento_entry_descricao.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_entry_data_venc = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_data_venc, height=30, width=150)
        self.frame_pagamento_entry_data_venc.grid(row=2, column=1, padx=5, pady=5, sticky="w")     
        self.frame_pagamento_entry_data_venc.bind("<KeyPress>", lambda event: format.formatar_data(event, self.frame_pagamento_entry_data_venc))          
        self.frame_pagamento_entry_data_venc.tabindex = 2
        self.frame_pagamento_entry_data_venc.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_entry_data_pag = ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_data_pag, height=30, width=150)
        self.frame_pagamento_entry_data_pag.grid(row=2, column=1, padx=290, pady=5, sticky="w")     
        self.frame_pagamento_entry_data_pag.bind("<KeyPress>", lambda event: format.formatar_data(event, self.frame_pagamento_entry_data_pag))  
        self.frame_pagamento_entry_data_pag.tabindex = 3
        self.frame_pagamento_entry_data_pag.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_entry_valor= ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor, height=30, width=150)
        self.frame_pagamento_entry_valor.grid(row=2, column=1, padx=510, pady=5, sticky="w")   
        self.frame_pagamento_entry_valor.bind("<KeyPress>", lambda event: format.formatar_valor(event, self.frame_pagamento_entry_valor))
        self.frame_pagamento_entry_valor.tabindex = 4
        self.frame_pagamento_entry_valor.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_entry_valor_pago= ct.CTkEntry(frame_pagamento, textvariable=self.ctk_entry_var_valor_pago, height=30, width=150)
        self.frame_pagamento_entry_valor_pago.grid(row=2, column=1, padx=760, pady=5, sticky="w")   
        self.frame_pagamento_entry_valor_pago.bind("<KeyPress>", lambda event: format.formatar_valor(event, self.frame_pagamento_entry_valor_pago))    
        self.frame_pagamento_entry_valor_pago.tabindex = 5
        self.frame_pagamento_entry_valor_pago.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_textbox_obs = ct.CTkTextbox(frame_pagamento,  width=910, height=100, border_width=2)
        self.frame_pagamento_textbox_obs.grid(row=3, column=1, padx=5, pady=5, sticky="w")     
        self.frame_pagamento_textbox_obs.tabindex = 6
        self.frame_pagamento_textbox_obs.bind("<Tab>", format.mover_foco)
        
        self.frame_pagamento_button_novo = ct.CTkButton(frame_pagamento, text="Novo", command=self.novo,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_novo.grid(row=4, column=1, padx=5, pady=5, sticky="w")   
        self.frame_pagamento_button_salvar = ct.CTkButton(frame_pagamento, text="Salvar", command=self.salvar, compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_salvar.grid(row=4, column=1, padx=150, pady=5, sticky="w")          
        self.frame_pagamento_button_excluir = ct.CTkButton(frame_pagamento, text="Excluir", command=self.remover, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_pagamento_button_excluir.grid(row=4, column=1, padx=295, pady=5, sticky="w")     
        self.frame_pagamento_button_excluir.configure(state=tk.DISABLED) 
        
        self.tree_view_data = ttk.Treeview(frame_pagamento)      
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10, "bold"))

        self.tree_view_data['columns'] = ("ID", "descricao", "data_pagamento", "data_vencimento","valor","valor_pago")
        self.tree_view_data.column("#0", width=0, stretch=False)
        self.tree_view_data.column("ID",  width=50)
        self.tree_view_data.column("descricao",  width=300)
        self.tree_view_data.column("data_pagamento", anchor="center", width=130)
        self.tree_view_data.column("data_vencimento", anchor="center", width=130)
        self.tree_view_data.column("valor", anchor="e", width=150)
        self.tree_view_data.column("valor_pago", anchor="e", width=150)
        self.tree_view_data.heading("ID", text="ID")
        self.tree_view_data.heading("descricao", text="Descrição")
        self.tree_view_data.heading("data_pagamento", text="Data Pagamento")
        self.tree_view_data.heading("data_vencimento", text="Data Vencimento")
        self.tree_view_data.heading("valor",  text="Valor")
        self.tree_view_data.heading("valor_pago",  text="Valor Pago")
        
        
        self.tree_view_data.bind("<Double-1>", lambda event: self.on_item_double_click(event, self.tree_view_data)) 
        self.tree_view_data.tag_configure('orow', background='#EEEEEE')
        self.tree_view_data.grid(row=5, column=1, columnspan=4, rowspan=5, padx=5, pady=30, sticky="w")
        
        rd = cp.ContasPagar()
        for result in self.reverse(rd.read()):
            self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")
           
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
                        
                for result in self.reverse(dlt.read()):
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
        
        valor = valor.replace("R$","").replace(",","").replace(" ","")
        valor_pago = valor_pago.replace("R$","").replace(",","").replace(" ","")
        
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
        if (ins.insert_update(id, desc, data_pag, data_venc,valor, valor_pago, obs)):
            for data in self.tree_view_data.get_children():
                self.tree_view_data.delete(data)    
                
            for result in self.reverse(ins.read()):
                self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")  
            
            if id == "":
                messagebox.showinfo("Sucesso", f"Despesa inserida com sucesso")
            else:
                messagebox.showinfo("Sucesso", f"Despesa alterada com sucesso")
            self.novo()     
        
        
    def on_item_double_click(self, event, tree_view_data):
        item = tree_view_data.selection()[0]
        values = tree_view_data.item(item, 'values')
        id = values[0]
        bus = cp.ContasPagar()
        res = bus.buscar(id)[0]
        if len(res) > 0:
            self.ctk_entry_var_id.set(res[0])
            self.ctk_entry_var_descricao.set(res[1])
            self.ctk_entry_var_data_venc.set(res[2])
            self.ctk_entry_var_data_pag.set(res[3])
            self.ctk_entry_var_valor.set(res[4])
            self.ctk_entry_var_valor_pago.set(res[5])
            self.frame_pagamento_textbox_obs.delete("1.0", "end") 
            self.frame_pagamento_textbox_obs.insert("1.0", res[6]) 
            self.frame_pagamento_button_excluir.configure(state=tk.NORMAL) 
        else:
            messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
            
    def reverse(self,tuples):
        new_tup = tuples[::-1]
        return new_tup   