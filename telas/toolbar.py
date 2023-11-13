
import customtkinter as ct
from CTkToolTip import *
import tkinter as tk

class toolbar():

    def botoes_acao(self, tela_toolbar, frame, width=60, height=28, row=0, column=1, sticky='w', pady=1, 
                                padx_novo=10, padx_alterar=75, padx_cancelar=140, padx_salvar=205,padx_excluir=290,
                                row_filtro=6, column_filtro=1, padx_text_filtro=0, pady_text_filtro=0, sticky_filtro="w",
                                width_entry_filtro=250, height_entry_filtro=30, padx_entry_filtro=675, pady_entry_filtro=0):
        
            tela_toolbar.button_novo = ct.CTkButton(frame, text="Novo", command=tela_toolbar.novo,  compound="right", width=width, text_color=("gray10", "#DCE4EE"))
            tela_toolbar.button_novo.grid(row=row, column=column, padx=padx_novo, pady=pady, sticky=sticky)
            CTkToolTip(tela_toolbar.button_novo, delay=0.5, message="Nova lançamento", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
            
            tela_toolbar.button_altera = ct.CTkButton(frame, text="Alterar", command=tela_toolbar.alterar,  compound="right", width=width, text_color=("gray10", "#DCE4EE"))
            tela_toolbar.button_altera.grid(row=row, column=column, padx=padx_alterar, pady=pady, sticky=sticky)
            CTkToolTip(tela_toolbar.button_altera, delay=0.5, message="Alterar lançamento", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")        
            
            tela_toolbar.button_cancelar = ct.CTkButton(frame, text="Cancelar", command=tela_toolbar.cancelar,  compound="right", width=width, text_color=("gray10", "#DCE4EE"))
            tela_toolbar.button_cancelar.grid(row=row, column=column, padx=padx_cancelar, pady=pady, sticky=sticky)
            CTkToolTip(tela_toolbar.button_cancelar, delay=0.5, message="Cancelar lançamento!", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")        
            
            tela_toolbar.button_salvar = ct.CTkButton(frame, text="Salvar", command=tela_toolbar.salvar, compound="right", width=width, text_color=("gray10", "#DCE4EE"))
            tela_toolbar.button_salvar.grid(row=row, column=column, padx=padx_salvar, pady=pady, sticky=sticky)   
            CTkToolTip(tela_toolbar.button_salvar, delay=0.5, message="Salvar lançamento", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
                
            tela_toolbar.button_excluir = ct.CTkButton(frame, text="Excluir", command=tela_toolbar.remover, compound="right", width=width,  text_color=("gray10", "#DCE4EE"))
            tela_toolbar.button_excluir.grid(row=row, column=column, padx=padx_excluir, pady=pady, sticky=sticky)     
            CTkToolTip(tela_toolbar.button_excluir, delay=0.5, message="Excluir lançamento", font=ct.CTkFont(size=14, weight="bold"), border_color="#FC9727", bg_color="#FC9727", text_color="#000")
            
            #INPUT FILTRAR
            tela_toolbar.frame_label_filtro = ct.CTkLabel(frame, text="Filtro:",  compound="left", font=ct.CTkFont(size=12, weight="bold"))
            tela_toolbar.frame_label_filtro.grid(row=row_filtro, column=column_filtro, padx=padx_text_filtro, pady=pady_text_filtro ,sticky=sticky_filtro)         
            tela_toolbar.frame_entry_filtro = ct.CTkEntry(frame, height=height_entry_filtro, width=width_entry_filtro, textvariable=tela_toolbar.ctk_entry_var_filtro)
            tela_toolbar.frame_entry_filtro.grid(row=row_filtro, column=column_filtro, padx=padx_entry_filtro, pady=pady_entry_filtro, sticky=sticky_filtro)       
            tela_toolbar.frame_entry_filtro.bind("<KeyRelease>", tela_toolbar.filtrar_bind)    
