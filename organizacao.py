import customtkinter as ct
import tkinter as tk
from DB.entidades import organizacao as org
from Utils import formatacao
from tkinter import ttk
from tkinter import messagebox
from CTkToolTip import *

class Organizacao():
    def __init__(self):
        super().__init__()
        
    def organizacao(self,frame_organizacao):
        
        self.label = ct.CTkLabel(frame_organizacao, text="Organizações", font=ct.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=10, sticky="e")       

        self.frame_organizacao_label_nome = ct.CTkLabel(frame_organizacao, text="Nome:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_organizacao_label_nome.grid(row=1, column=0, padx=10, pady=5, sticky="w")    
                  
        #INPUTS
        self.ctk_entry_var_nome = tk.StringVar()
        self.ctk_entry_var_id = tk.StringVar()

        format = formatacao.Util()
        
        self.frame_organizacao_entry_nome = ct.CTkEntry(frame_organizacao, textvariable=self.ctk_entry_var_nome, height=30, width=905)
        self.frame_organizacao_entry_nome.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.frame_organizacao_entry_nome.tabindex = 1
        self.frame_organizacao_entry_nome.bind("<Tab>", format.mover_foco)
        
        self.frame_organizacao_button_novo = ct.CTkButton(frame_organizacao, text="Novo", command=self.novo,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_novo.grid(row=5, column=1, padx=10, pady=5, sticky="w")   
        CTkToolTip(self.frame_organizacao_button_novo, delay=0.5, message="Iniciar uma nova organização!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        self.frame_organizacao_button_salvar = ct.CTkButton(frame_organizacao, text="Salvar", command=self.salvar, compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_salvar.grid(row=5, column=1, padx=150, pady=5, sticky="w")     
        CTkToolTip(self.frame_organizacao_button_salvar, delay=0.5, message="Incluir ou alterar organização!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
             
        self.frame_organizacao_button_excluir = ct.CTkButton(frame_organizacao, text="Excluir", command=self.remover, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_organizacao_button_excluir.grid(row=5, column=1, padx=295, pady=5, sticky="w")     
        self.frame_organizacao_button_excluir.configure(state=tk.DISABLED) 
        CTkToolTip(self.frame_organizacao_button_excluir, delay=0.5, message="Exclui organização selecionado!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        self.ordenacao_colunas = {"ID": "crescente", "nome": "crescente"}
         
        self.tree_view_data = ttk.Treeview(frame_organizacao)      
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10, "bold"))

        self.tree_view_data['columns'] = ("ID", "nome")
        self.tree_view_data.column("#0", width=0, stretch=False)
        self.tree_view_data.column("ID",  width=50)
        self.tree_view_data.column("nome",  width=850)
        self.tree_view_data.heading("ID", text="ID", command=lambda: self.ordenar_por_coluna("ID"))
        self.tree_view_data.heading("nome", text="Nome", command=lambda: self.ordenar_por_coluna("nome"))
        
        self.tree_view_data.bind("<Double-1>", lambda event: self.on_item_double_click(self.tree_view_data)) 
        self.tree_view_data.tag_configure('orow', background='#EEEEEE')
        self.tree_view_data.grid(row=6, column=1, columnspan=4, rowspan=5, padx=10, pady=30, sticky="w")
        
        rd = org.Organizacao()
        lst = rd.listar(False)
        for result in self.reverse(lst):
            self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")
            
        if len(lst) > 0: 
            self.tree_view_data.selection_set(self.tree_view_data.get_children()[0])   
            self.on_item_double_click(self.tree_view_data)
          
    def ordenar_por_coluna(self, coluna):
        estado_atual = self.ordenacao_colunas[coluna]
        data = [(self.tree_view_data.set(item, coluna), item) for item in self.tree_view_data.get_children('')]
        data.sort(reverse=estado_atual == "crescente", key=lambda x: x[0])
        for index, (val, item) in enumerate(data):
            self.tree_view_data.move(item, '', index)
        self.ordenacao_colunas[coluna] = "crescente" if estado_atual == "decrescente" else "decrescente"
               
    def novo(self):
        self.ctk_entry_var_id.set("")
        self.ctk_entry_var_nome.set("")
        self.frame_organizacao_button_excluir.configure(state=tk.DISABLED)    
        
        
    def remover(self):
        desc = str(self.ctk_entry_var_nome.get())
        resposta = messagebox.askyesno("Confirmação", f"Deseja excluir a organização {desc}?")
        if (resposta):      
            id = str(self.ctk_entry_var_id.get())
            dlt = org.Organizacao()
            if (dlt.delete(id)):
                for data in self.tree_view_data.get_children():
                    self.tree_view_data.delete(data)  
                        
                for result in self.reverse(dlt.listar(False)):
                    self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")   
                self.novo()             
            
    def salvar(self):
        id          = str(self.ctk_entry_var_id.get())
        desc        = str(self.ctk_entry_var_nome.get())
          
        if desc == "":
            messagebox.showinfo("Informação", "O campo nome é de preenchimento obrigatório")
            self.frame_organizacao_entry_descricao.focus()
            return False
        
        ins = org.Organizacao()
        if (ins.insert_update(id, desc)):
            for data in self.tree_view_data.get_children():
                self.tree_view_data.delete(data)    
                
            for result in self.reverse(ins.listar(False)):
                self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")  
            
            if id == "":
                messagebox.showinfo("Sucesso", f"Organização inserida com sucesso")
            else:
                messagebox.showinfo("Sucesso", f"Organização alterada com sucesso")
            self.novo()     
        
        
    def on_item_double_click(self, tree_view_data):
        item = tree_view_data.selection()[0]
        values = tree_view_data.item(item, 'values')
        id = values[0]
        bus = org.Organizacao()
        res = bus.buscar(id, True)
        if res != None:
            self.ctk_entry_var_id.set(res['id'])
            self.ctk_entry_var_nome.set(res['nome'])
            self.frame_organizacao_button_excluir.configure(state=tk.NORMAL) 
        else:
            messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
            
    def reverse(self,tuples):
        new_tup = tuples[::-1]
        return new_tup   