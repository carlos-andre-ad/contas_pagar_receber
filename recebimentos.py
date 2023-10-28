import customtkinter as ct
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import DB.contas_receber as cr
import Utils.formatacao as formatacao
from PIL import Image
   

class Recebimentos():
    def __init__(self):
        super().__init__()
        
    def receber(self,frame_recebimento):
        
        self.label = ct.CTkLabel(frame_recebimento, text="Contas à Receber", font=ct.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=10, sticky="e")        

        self.frame_recebimento_label_descricao = ct.CTkLabel(frame_recebimento, text="Descrição:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_descricao.grid(row=1, column=0, padx=10, pady=5, sticky="w")    
        
        self.frame_recebimento_label_data = ct.CTkLabel(frame_recebimento, text="Data Recebimento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_data.grid(row=2, column=0, padx=10, pady=5 ,sticky="w")   

        self.frame_recebimento_label_valor = ct.CTkLabel(frame_recebimento, text="Valor Recebimento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_valor.grid(row=2, column=1, padx=180, pady=5 ,sticky="w") 
        
        self.frame_recebimento_label_obs = ct.CTkLabel(frame_recebimento, text="Observações:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_obs.grid(row=3, column=0, padx=10, pady=5 ,sticky="w")              
                
        #INPUTS
        self.ctk_entry_var_descricao = tk.StringVar()
        self.ctk_entry_var_id = tk.StringVar()
        self.ctk_entry_var_data = tk.StringVar()
        self.ctk_entry_var_valor = tk.StringVar()
        self.ctk_entry_var_obs = tk.StringVar()
        
        format = formatacao.Util()
        
        self.frame_recebimento_entry_descricao = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_descricao, height=30, width=905)
        self.frame_recebimento_entry_descricao.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.frame_recebimento_entry_descricao.tabindex = 1
        self.frame_recebimento_entry_descricao.bind("<Tab>", format.mover_foco)
        
        self.frame_recebimento_entry_data = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_data, height=30, width=150)
        self.frame_recebimento_entry_data.grid(row=2, column=1, padx=5, pady=5, sticky="w")     
        self.frame_recebimento_entry_data.bind("<KeyPress>", lambda event: format.formatar_data(event, self.frame_recebimento_entry_data))  
        self.frame_recebimento_entry_data.tabindex = 2   
        self.frame_recebimento_entry_data.bind("<Tab>", format.mover_foco)    
        
        self.frame_recebimento_entry_valor= ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_valor, height=30, width=150)
        self.frame_recebimento_entry_valor.grid(row=2, column=1, padx=300, pady=5, sticky="w")   
        self.frame_recebimento_entry_valor.bind("<KeyPress>", lambda event: format.formatar_valor(event, self.frame_recebimento_entry_valor))
        self.frame_recebimento_entry_valor.tabindex = 3
        self.frame_recebimento_entry_valor.bind("<Tab>", format.mover_foco)
            
        self.frame_recebimento_textbox_obs = ct.CTkTextbox(frame_recebimento,  width=910, height=100, border_width=2)
        self.frame_recebimento_textbox_obs.grid(row=3, column=1, padx=5, pady=5, sticky="w")    
        self.frame_recebimento_textbox_obs.tabindex = 4
        self.frame_recebimento_textbox_obs.bind("<Tab>", format.mover_foco)
        
        self.frame_recebimento_button_novo = ct.CTkButton(frame_recebimento, text="Novo", command=self.novo,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_novo.grid(row=4, column=1, padx=5, pady=5, sticky="w")   
        self.frame_recebimento_button_salvar = ct.CTkButton(frame_recebimento, text="Salvar", command=self.salvar, compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_salvar.grid(row=4, column=1, padx=150, pady=5, sticky="w")          
        self.frame_recebimento_button_excluir = ct.CTkButton(frame_recebimento, text="Excluir", command=self.remover, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_excluir.grid(row=4, column=1, padx=295, pady=5, sticky="w")     
        self.frame_recebimento_button_excluir.configure(state=tk.DISABLED) 
        
        self.tree_view_data = ttk.Treeview(frame_recebimento)      
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10, "bold"))

        self.tree_view_data['columns'] = ("ID", "descricao", "data_recebimento","valor")
        self.tree_view_data.column("#0", width=0, stretch=False)
        self.tree_view_data.column("ID",  width=50)
        self.tree_view_data.column("descricao",  width=500)
        self.tree_view_data.column("data_recebimento", anchor="center", width=150)
        self.tree_view_data.column("valor", anchor="e", width=200)
        self.tree_view_data.heading("ID", text="ID")
        self.tree_view_data.heading("descricao", text="Descrição")
        self.tree_view_data.heading("data_recebimento", text="Data Recebimento")
        self.tree_view_data.heading("valor",  text="Valor")
        
        self.tree_view_data.bind("<Double-1>", lambda event: self.on_item_double_click(event, self.tree_view_data)) 
        self.tree_view_data.tag_configure('orow', background='#EEEEEE')
        self.tree_view_data.grid(row=5, column=1, columnspan=4, rowspan=5, padx=5, pady=30, sticky="w")
        
        rd = cr.ContasReceber()
        for result in self.reverse(rd.read()):
            self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")
           
    def novo(self):
        self.ctk_entry_var_id.set("")
        self.ctk_entry_var_descricao.set("")
        self.ctk_entry_var_data.set("")
        self.ctk_entry_var_valor.set("")
        self.frame_recebimento_textbox_obs.delete("1.0", "end") 
        self.frame_recebimento_textbox_obs.insert("1.0", "")  
        self.frame_recebimento_button_excluir.configure(state=tk.DISABLED)    
        
        
    def remover(self):
        desc = str(self.ctk_entry_var_descricao.get())
        resposta = messagebox.askyesno("Confirmação", f"Deseja excluir a receita {desc}?")
        if (resposta):      
            id = str(self.ctk_entry_var_id.get())
            dlt = cr.ContasReceber()
            if (dlt.delete(id)):
                for data in self.tree_view_data.get_children():
                    self.tree_view_data.delete(data)  
                        
                for result in self.reverse(dlt.read()):
                    self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")   
                self.novo()             
            
    def salvar(self):
        id          = str(self.ctk_entry_var_id.get())
        desc        = str(self.ctk_entry_var_descricao.get())
        data_rec   = str(self.ctk_entry_var_data.get())
        valor       = str(self.ctk_entry_var_valor.get())
        obs         = str(self.ctk_entry_var_obs.get())  
        
        valor = valor.replace("R$","").replace(",","").replace(" ","")
        
        if desc == "":
            messagebox.showinfo("Informação", "O campo descrição é de preenchimento obrigatório")
            self.frame_recebimento_entry_descricao.focus()
            return False
        if data_rec == "":
            messagebox.showinfo("Informação", "O campo data do recebimento é de preenchimento obrigatório")
            self.frame_recebimento_entry_data.focus()
            return False        
        if valor == "":
            messagebox.showinfo("Informação", "O campo valor é de preenchimento obrigatório")
            self.frame_recebimento_entry_valor.focus()
            return False
        
        ins = cr.ContasReceber()
        if (ins.insert_update(id, desc, data_rec, valor, obs)):
            for data in self.tree_view_data.get_children():
                self.tree_view_data.delete(data)    
                
            for result in self.reverse(ins.read()):
                self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")  
            
            if id == "":
                messagebox.showinfo("Sucesso", f"Receita inserida com sucesso")
            else:
                messagebox.showinfo("Sucesso", f"Receita alterada com sucesso")
            self.novo()     
        
        
    def on_item_double_click(self, event, tree_view_data):
        item = tree_view_data.selection()[0]
        values = tree_view_data.item(item, 'values')
        id = values[0]
        bus = cr.ContasReceber()
        res = bus.buscar(id)[0]
        if len(res) > 0:
            self.ctk_entry_var_id.set(res[0])
            self.ctk_entry_var_descricao.set(res[1])
            self.ctk_entry_var_data.set(res[2])
            self.ctk_entry_var_valor.set(res[3])
            self.frame_recebimento_textbox_obs.delete("1.0", "end") 
            self.frame_recebimento_textbox_obs.insert("1.0", res[4]) 
            self.frame_recebimento_button_excluir.configure(state=tk.NORMAL) 
        else:
            messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
            
    def reverse(self,tuples):
        new_tup = tuples[::-1]
        return new_tup   