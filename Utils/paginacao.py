
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import re
import customtkinter as ct
from CTkToolTip import *

class PaginatedTreeView():
    
    def __init__(self, 
                 page_size, 
                 current_page, 
                 paginate, 
                 nome_coluna_ordenar, 
                 colunas_data, 
                 colunas_numericas, 
                 colunas_tree_view, 
                 ordenacao_colunas,
                 tree_view_paginada,
                 dados,
                 idx_coluna_id,
                 tree_view_id_selecionado
                 ):
        
        self.page_size                  = page_size # Número de itens por página
        self.current_page               = current_page
        self.paginate                   = paginate
        self.ordenacao_colunas          = ordenacao_colunas
        self.nome_coluna_ordenar        = nome_coluna_ordenar
        self.tree_view_id_selecionado   = tree_view_id_selecionado
        self.idx_coluna_id              = idx_coluna_id
        self.colunas_tree_view          = colunas_tree_view
        self.colunas_numericas          = colunas_numericas
        self.colunas_data               = colunas_data
        self.tree_view_paginada         = tree_view_paginada
        self.dados_all                  = dados
        #valor de comparação entre uma cheve do self.dados_all uma coluna no tree_view_paginada
        #para fazer a ordenação
        self.chave_dados_all            = "id"
        
        self.treeview_temp = ttk.Treeview(None, columns=(tuple(self.colunas_tree_view)))
        
        self.data_page = []
        
        self.verificar_pagina_item = False
        
        self.lista_de_dados = []

    def monta_paginacao(self, alternar_ascendencia):
        
        #page_number = self.current_page
        
        self.ordem(alternar_ascendencia)
        self.lista_de_dados = []
        for result in self.dados_all:
            result = list(result.values())
            self.lista_de_dados.append(result)
        
        if self.paginate == 1:
            # No salvar verifica a pagina que o dado está e vai até ela
            if (self.verificar_pagina_item  and self.tree_view_id_selecionado != None and int(self.tree_view_id_selecionado) > 0):
                self.current_page = 0
                conta_pagina = 0
                for item in self.dados_all:
                    conta_pagina +=1
                    if conta_pagina > self.page_size:
                        conta_pagina = 0
                        self.current_page +=1
                    if int(item[self.chave_dados_all]) == int(self.tree_view_id_selecionado):     
                        break            
                        
            start = self.current_page * self.page_size
            end = start + self.page_size
            self.data_page = self.lista_de_dados[start:end]

            self.tree_view_paginada.delete(*self.tree_view_paginada.get_children())

            for item in self.data_page:
                self.tree_view_paginada.insert('', 'end', values=item)
                
            self.ordenar_coluna()
            

    def proxima_pagina(self):
        if self.current_page < len(self.lista_de_dados) // self.page_size:
            self.current_page += 1
            
    def pagina_anterior(self):
        if self.current_page > 0:
            self.current_page -= 1
            
    def primeira_pagina(self):
        self.current_page = 0

    def ultima_pagina(self):
        total_pages = len(self.lista_de_dados) // self.page_size
        self.current_page = total_pages
                 
            
    def atualizar_estado_botoes_paginacao(self):
        total_pages = len(self.lista_de_dados) // self.page_size
        next_button = tk.DISABLED
        prev_button = tk.DISABLED
        first_button = tk.DISABLED
        last_button = tk.DISABLED
            
        if self.current_page == 0 and total_pages == 0:
            prev_button = tk.DISABLED
            next_button = tk.DISABLED
            first_button = tk.DISABLED
            last_button = tk.DISABLED

        if self.current_page == 0 and total_pages > 0:
            prev_button = tk.DISABLED
            next_button = tk.NORMAL
            first_button = tk.DISABLED
            last_button = tk.NORMAL

        if self.current_page > 0 and self.current_page < total_pages:
            prev_button = tk.NORMAL
            next_button = tk.NORMAL
            first_button = tk.NORMAL
            last_button = tk.NORMAL

        if self.current_page > 0 and self.current_page == total_pages:
            prev_button = tk.NORMAL
            next_button = tk.DISABLED
            first_button = tk.NORMAL
            last_button = tk.DISABLED
            
        if ((self.current_page+1) * self.page_size) + 1 >= len(self.lista_de_dados):
            next_button = tk.DISABLED
            last_button = tk.DISABLED
            prev_button = tk.NORMAL
            first_button = tk.NORMAL      
            
        if len(self.lista_de_dados) == 0:
            next_button = tk.DISABLED
            prev_button = tk.DISABLED
            first_button = tk.DISABLED
            last_button = tk.DISABLED               
            
        return next_button, prev_button , first_button, last_button
   
    
    
    def selecionar_linha_tree_view_por_id(self):
        tam = len(self.tree_view_paginada.get_children())
        if tam > 0:
            if int(self.tree_view_id_selecionado) <= 0:    
                item = self.tree_view_paginada.get_children()[0]          
                self.tree_view_paginada.selection_set(item)
                self.tree_view_paginada.focus(item)
                self.tree_view_paginada.see(item)
            else:       
                for item in self.tree_view_paginada.get_children():
                    valores = self.tree_view_paginada.item(item, 'values')
                    if valores and len(valores) > 0:
                        if int(valores[self.idx_coluna_id]) == int(self.tree_view_id_selecionado):                     
                            self.tree_view_paginada.selection_set(item)
                            self.tree_view_paginada.focus(item)
                            self.tree_view_paginada.see(item)
                            break
                        

    # coluna: Nome da coluna que será ordenada, 
    # ordenacao_colunas: tupla das colunas que podem ser ordenadas. Nome e ascendencia: {nome: cescente} 
    # colunas_tree_view: Nomes das Colunas do tree view, 
    # colunas_numericas: somente os nomes das colunas numericas que estão em colunas_tree_view
    # colunas_data: somente os nomes das colunas de data que estão em colunas_tree_view
    # dados_all: lista de DADOS
    # view: TreeView
    def ordenar_coluna(self):
            
        self.treeview_temp.delete(*self.treeview_temp.get_children())
        
        _todas_as_linhas = self.tree_view_paginada.get_children()
        for linha in _todas_as_linhas:
            valores = self.tree_view_paginada.item(linha, 'values')
            self.treeview_temp.insert('', 'end', values=valores)
            
        self.tree_view_paginada.delete(*self.tree_view_paginada.get_children())
        
        for item in self.dados_all:
            for p in self.data_page:
                if int(p[0]) == int(item[self.chave_dados_all]):
                    for _item in self.treeview_temp.get_children():
                        valores = self.treeview_temp.item(_item, 'values')
                        if valores and len(valores) > 0:
                            if str(valores[self.idx_coluna_id]) == str(item[self.chave_dados_all]): 
                                item_id = self.tree_view_paginada.insert('', 'end', values=[item[column] for column in self.colunas_tree_view])
                                item['treeview_item'] = item_id


    def ordem(self, alternar_ascendencia):
        estado_atual = "crescente"
        _reverse = False
        if alternar_ascendencia:
            _reverse = estado_atual == self.ordenacao_colunas[self.nome_coluna_ordenar]
            if (_reverse ==False):
                estado_atual = self.ordenacao_colunas[self.nome_coluna_ordenar]
        
        if self.nome_coluna_ordenar in self.colunas_numericas:
            self.dados_all.sort(reverse=_reverse, key=lambda x: int(''.join(re.findall(r'\d+', str(x[self.nome_coluna_ordenar])) )))
        elif self.nome_coluna_ordenar in self.colunas_data:
            self.dados_all.sort(reverse=_reverse, key=lambda x: datetime.strptime(x[self.nome_coluna_ordenar], "%d/%m/%Y"))
        else:
            self.dados_all.sort(reverse=_reverse, key=lambda x: x[self.nome_coluna_ordenar].casefold())       
            
        self.ordenacao_colunas[self.nome_coluna_ordenar] = "crescente" if estado_atual == "decrescente" else "decrescente"
        
        
    def ordencao(self,alternar_ascendencia):
        self.ordem(alternar_ascendencia)
        self.ordenar_coluna()
        
    def navegacao(self, tela_paginacao,frame, paginar_tree_view=1,
                  width=60, height=28, row=0, column=1, sticky='w', pady=1, padx_f=10, padx_n=75, padx_p=140, padx_l=205, padx_v=300):
        if paginar_tree_view == 1:
            tela_paginacao.first_button  = ct.CTkButton(frame, width=width, text="Primeiro", command=tela_paginacao.primeira_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            tela_paginacao.next_button  = ct.CTkButton(frame, width=width,text="Próximo", command=tela_paginacao.proxima_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            tela_paginacao.prev_button = ct.CTkButton(frame,width=width, text="Anterior", command=tela_paginacao.pagina_anterior, compound="right",  text_color=("gray10", "#DCE4EE"))
            tela_paginacao.last_button  = ct.CTkButton(frame, width=width, text="Último", command=tela_paginacao.ultima_pagina, compound="right",  text_color=("gray10", "#DCE4EE"))
            tela_paginacao.first_button.grid(row=row, column=column, padx=padx_f, pady=pady, sticky=sticky)
            tela_paginacao.next_button.grid(row=row, column=column, padx=padx_n, pady=pady, sticky=sticky)
            tela_paginacao.prev_button.grid(row=row, column=column, padx=padx_p, pady=pady, sticky=sticky)
            tela_paginacao.last_button.grid(row=row, column=column, padx=padx_l, pady=pady, sticky=sticky) 
            
        frame_button_view_pdf = ct.CTkButton(frame, text="Visualização", command=tela_paginacao.imprimir, compound="right",  text_color=("gray10", "#DCE4EE"))
        frame_button_view_pdf.grid(row=row, column=column, padx=padx_v, pady=pady, sticky=sticky)     
        CTkToolTip(frame_button_view_pdf, delay=0.5, message="Visualizar Organizações", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")        
                

