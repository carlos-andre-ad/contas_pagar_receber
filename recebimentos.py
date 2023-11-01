import customtkinter as ct
import tkinter as tk
from DB.entidades import contas_receber as cr
from DB.entidades import pessoa
from Utils import formatacao
from tkinter import ttk
from tkinter import messagebox
from CTkToolTip import *

class Recebimentos():
    def __init__(self):
        super().__init__()
        
    def receber(self,frame_recebimento):
        
        self.contasReceber =  cr.ContasReceber()
        self.format = formatacao.Util()
        
        self.label = ct.CTkLabel(frame_recebimento, text="Contas à Receber", font=ct.CTkFont(size=25, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=10)       
        
        self.frame_recebimento_label_organizacao = ct.CTkLabel(frame_recebimento, text="Organização:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_organizacao.grid(row=1, column=0, padx=10, pady=5, sticky="w")                

        self.frame_recebimento_label_descricao = ct.CTkLabel(frame_recebimento, text="Descrição:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_descricao.grid(row=2, column=0, padx=10, pady=5, sticky="w")    
        
        self.frame_recebimento_label_data = ct.CTkLabel(frame_recebimento, text="Data Recebimento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_data.grid(row=3, column=0, padx=10, pady=5 ,sticky="w")   

        self.frame_recebimento_label_valor = ct.CTkLabel(frame_recebimento, text="Valor Recebimento:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_valor.grid(row=3, column=1, padx=180, pady=5 ,sticky="w") 
        
        self.frame_recebimento_label_obs = ct.CTkLabel(frame_recebimento, text="Observações:", compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_recebimento_label_obs.grid(row=4, column=0, padx=10, pady=5 ,sticky="w")              
                
        #INPUTS
        self.ctk_entry_var_descricao = tk.StringVar()
        self.ctk_entry_var_id = tk.StringVar()
        self.ctk_entry_var_data = tk.StringVar()
        self.ctk_entry_var_valor = tk.StringVar()
        self.ctk_entry_var_valor_total = tk.StringVar()
        self.ctk_entry_var_obs = tk.StringVar()
        self.ctk_combobox_var_organizacao = tk.StringVar()
        self.ctk_entry_var_filtro = tk.StringVar()  
        
        p = pessoa.Pessoa()
        self.organizacoes = p.listar(True)
        
        self.frame_recebimento_combobox_organizacoes = ct.CTkComboBox(frame_recebimento, values=[item['nome'] for item in self.organizacoes],
                                                                        command=self.selecionar_organizacao, variable=self.ctk_combobox_var_organizacao)
        self.frame_recebimento_combobox_organizacoes.grid(row=1, column=1, padx=10, pady=5, sticky="w") 
        self.frame_recebimento_combobox_organizacoes.tabindex = 1
        
        self.frame_recebimento_entry_descricao = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_descricao, height=30, width=905)
        self.frame_recebimento_entry_descricao.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.frame_recebimento_entry_descricao.tabindex = 2
        self.frame_recebimento_entry_descricao.bind("<Tab>", self.format.mover_foco)
        
        self.frame_recebimento_entry_data = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_data, height=30, width=150)
        self.frame_recebimento_entry_data.grid(row=3, column=1, padx=10, pady=5, sticky="w")     
        self.frame_recebimento_entry_data.bind("<KeyPress>", lambda event: self.format.formatar_data(event, self.frame_recebimento_entry_data))  
        self.frame_recebimento_entry_data.tabindex = 3
        self.frame_recebimento_entry_data.bind("<Tab>", self.format.mover_foco)    
        
        self.frame_recebimento_entry_valor= ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_valor, height=30, width=150)
        self.frame_recebimento_entry_valor.grid(row=3, column=1, padx=320, pady=5, sticky="w")   
        self.frame_recebimento_entry_valor.bind("<KeyPress>", lambda event: self.format.formatar_valor(event, self.frame_recebimento_entry_valor))
        self.frame_recebimento_entry_valor.tabindex = 4
        self.frame_recebimento_entry_valor.bind("<Tab>", self.format.mover_foco)
            
        self.frame_recebimento_textbox_obs = ct.CTkTextbox(frame_recebimento,  width=910, height=100, border_width=2)
        self.frame_recebimento_textbox_obs.grid(row=4, column=1, padx=10, pady=5, sticky="w")    
        self.frame_recebimento_textbox_obs.tabindex = 5
        self.frame_recebimento_textbox_obs.bind("<Tab>", self.format.mover_foco)
        
        self.frame_recebimento_button_novo = ct.CTkButton(frame_recebimento, text="Novo", command=self.novo,  compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_novo.grid(row=5, column=1, padx=10, pady=5, sticky="w")   
        CTkToolTip(self.frame_recebimento_button_novo, delay=0.5, message="Iniciar um novo lançamento!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        self.frame_recebimento_button_salvar = ct.CTkButton(frame_recebimento, text="Salvar", command=self.salvar, compound="right", text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_salvar.grid(row=5, column=1, padx=150, pady=5, sticky="w")     
        CTkToolTip(self.frame_recebimento_button_salvar, delay=0.5, message="Inclui um novo lançamento ou altera o existe!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
             
        self.frame_recebimento_button_excluir = ct.CTkButton(frame_recebimento, text="Excluir", command=self.remover, compound="right",  text_color=("gray10", "#DCE4EE"))
        self.frame_recebimento_button_excluir.grid(row=5, column=1, padx=295, pady=5, sticky="w")     
        self.frame_recebimento_button_excluir.configure(state=tk.DISABLED) 
        CTkToolTip(self.frame_recebimento_button_excluir, delay=0.5, message="Exclui lançamento selecionado!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
        
        
        #INPUT FILTRAR
        self.frame_label_filtro = ct.CTkLabel(frame_recebimento, text="Filtro:",  compound="left", font=ct.CTkFont(size=12, weight="bold"))
        self.frame_label_filtro.grid(row=6, column=1, padx=630, pady=5 ,sticky="w")         
        self.frame_entry_filtro = ct.CTkEntry(frame_recebimento, height=30, width=250, textvariable=self.ctk_entry_var_filtro)
        self.frame_entry_filtro.grid(row=6, column=1, padx=675, pady=1, sticky="w")       
        self.frame_entry_filtro.bind("<KeyRelease>", self.filtrar_bind)
                
        self.ordenacao_colunas = {"ID": "crescente", "descricao": "crescente", "data_recebimento": "crescente",  "valor": "crescente"}
         
        self.tree_view_data = ttk.Treeview(frame_recebimento)      
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial bold', 10, "bold"))
        self.tree_view_data['columns'] = ("ID", "descricao", "data_recebimento","valor")
        self.tree_view_data.column("#0", width=0, stretch=False)
        self.tree_view_data.column("ID",  width=60)
        self.tree_view_data.column("descricao",  width=500)
        self.tree_view_data.column("data_recebimento", anchor="center", width=150)
        self.tree_view_data.column("valor", anchor="e", width=200)
        self.tree_view_data.heading("ID", text="ID", command=lambda: self.ordenar_por_coluna("ID"))
        self.tree_view_data.heading("descricao", text="Descrição", command=lambda: self.ordenar_por_coluna("descricao"))
        self.tree_view_data.heading("data_recebimento", text="Data Recebimento", command=lambda: self.ordenar_por_coluna("data_recebimento"))
        self.tree_view_data.heading("valor",  text="Valor", command=lambda: self.ordenar_por_coluna("valor"))
        self.tree_view_data.bind("<Double-1>", lambda event: self.on_item_double_click(self.tree_view_data)) 
        self.tree_view_data.tag_configure('orow', background='#EEEEEE')
        self.tree_view_data.grid(row=7, column=1, columnspan=4, rowspan=5, padx=10, pady=1, sticky="w")
        #TOTALIZADORES
        valor_total = ct.CTkEntry(frame_recebimento, textvariable=self.ctk_entry_var_valor_total, border_width=0, justify="right",
                                    height=30, width=200, state=tk.DISABLED, font=ct.CTkFont(size=14, weight="bold"))      
        valor_total.grid(row=20, column=1, padx=720, pady=1, sticky="w")
      
        #Preenche tree view
        lst = self.contasReceber.listar(True)
        #self.update_tree_view(lst)

    def selecionar_organizacao(self, selected):
        self.ctk_combobox_var_organizacao.set( selected)
              
              
    def ordenar_por_coluna(self, coluna):
        estado_atual = self.ordenacao_colunas[coluna]
        data = [(self.tree_view_data.set(item, coluna), item) for item in self.tree_view_data.get_children('')]
        data.sort(reverse=estado_atual == "crescente", key=lambda x: x[0])
        for index, (val, item) in enumerate(data):
            self.tree_view_data.move(item, '', index)
        self.ordenacao_colunas[coluna] = "crescente" if estado_atual == "decrescente" else "decrescente"                        

           
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
            if (self.contasReceber.delete(id)):
                for data in self.tree_view_data.get_children():
                    self.tree_view_data.delete(data)  
                        
                for result in self.reverse(self.contasReceber.listar(False)):
                    self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")   
                self.novo()             
            
    def salvar(self):
        id          = str(self.ctk_entry_var_id.get())
        desc        = str(self.ctk_entry_var_descricao.get())
        data_rec   = str(self.ctk_entry_var_data.get())
        valor       = str(self.ctk_entry_var_valor.get())
        obs         = str(self.ctk_entry_var_obs.get())  
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
        if data_rec == "":
            messagebox.showinfo("Informação", "O campo data do recebimento é de preenchimento obrigatório")
            self.frame_recebimento_entry_data.focus()
            return False        
        if valor == "":
            messagebox.showinfo("Informação", "O campo valor é de preenchimento obrigatório")
            self.frame_recebimento_entry_valor.focus()
            return False
        
        if (self.contasReceber.insert_update(id, desc, data_rec, valor, obs, org)):
            for data in self.tree_view_data.get_children():
                self.tree_view_data.delete(data)    
                
            for result in self.reverse(self.contasReceber.listar(False)):
                self.tree_view_data.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")  
            
            if id == "":
                messagebox.showinfo("Sucesso", f"Receita inserida com sucesso")
            else:
                messagebox.showinfo("Sucesso", f"Receita alterada com sucesso")
            self.novo()     
        
        
    def on_item_double_click(self, tree_view_data):
        item = tree_view_data.selection()[0]
        values = tree_view_data.item(item, 'values')
        id = values[0]
        res = self.contasReceber.buscar(id, True)
        if res != None:
            self.ctk_combobox_var_organizacao.set(res['organizacao'])
            self.ctk_entry_var_id.set(res['id'])
            self.ctk_entry_var_descricao.set(res['descricao'])
            self.ctk_entry_var_data.set(res['data_recebimento'])
            self.ctk_entry_var_valor.set(res['valor'])
            if (res['observacoes'] != "" and res['observacoes'] != None):
                self.frame_recebimento_textbox_obs.delete("1.0", "end") 
                self.frame_recebimento_textbox_obs.insert("1.0", res['observacoes']) 
            self.frame_recebimento_button_excluir.configure(state=tk.NORMAL) 
        else:
            messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
            
    def update_tree_view(self, lst):
        vl_tot = 0.0
        vlp_tot = 0.0
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
            
            
    def filtrar_bind(self, event):
        self.filtrar()

    def filtrar(self):
        pass
        #filtro = self.frame_entry_filtro.get().lower()
        #if filtro:
        #    items = []
        #    for item in self.data_original:
        #        if any(str(value).lower().find(filtro) != -1 for value in item):
        #            items.append(item)
        #    self.atualizar_treeview(items)
        #else:
        #    self.atualizar_treeview(self.data_original)                
        #  
                    
    def reverse(self,tuples):
        new_tup = tuples[::-1]
        return new_tup   