
from tkinter import messagebox
import psycopg2

class Conexao():
    def __init__(self):
        pass
     
    def criar_tabelas(self):
        try:
            conn = self.conexao()
            if conn:
                comando = conn.cursor()
                comando.execute(""" CREATE TABLE IF NOT EXISTS contas_pagar(
                                    id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
                                    descricao varchar(100)  NOT NULL,
                                    observacoes text,
                                    data_pagamento date NOT NULL,
                                    data_vencimento date NOT NULL,
                                    valor float8 NOT NULL,
                                    valor_pago float8 NOT NULL
                                    )""")
                comando.execute(""" CREATE TABLE IF NOT EXISTS contas_receber(
                                    id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
                                    descricao varchar(100)  NOT NULL,
                                    observacoes text,
                                    data_recebimento date NOT NULL,
                                    valor float8 NOT NULL
                                    )""")                
                
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar tabela: {str(e)}")
            return False
        

    def conexao(self):
        try:
            conn = psycopg2.connect(database="contas", user="postgres", password="758198758198", port="15432")
            if conn:
                return conn
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {str(e)}")
            return None  
        
        
          