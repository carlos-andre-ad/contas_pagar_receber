
from tkinter import messagebox
import os
import psycopg2
from dotenv import load_dotenv

class Conexao():
    def __init__(self):
        pass
     
    def criar_tabelas(self):
        try:
            conn = self.conexao()
            if conn:
                comando = conn.cursor()
                comando.execute(""" CREATE TABLE IF NOT EXISTS migration(
                                    id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
                                    arquivo varchar(200)  NOT NULL,
                                    conteudo text  NOT NULL,
                                    data date NOT NULL
                                    )""")

                dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "migration")
                for sql in os.listdir(dir):
                    if sql.endswith('.sql'):
                        comando.execute("SELECT id FROM migration WHERE arquivo = '" + sql + "'")
                        results = comando.fetchall()
                        if len(results) == 0:
                            sql_path = os.path.join(dir, sql)
                            
                            with open(sql_path, 'r') as f:
                                conteudo = f.read()
                            comando.execute(conteudo)
                            comando.execute("INSERT INTO migration(arquivo, conteudo, data) VALUES('"+ sql + "','" + conteudo +"', CURRENT_DATE )")
                
                conn.commit()   
                conn.close()
                return True
        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Erro", f"Erro ao criar tabela: {str(e)}")
            return False
        

    def conexao(self):
        
        load_dotenv()
        
        try:
            conn = psycopg2.connect(database=os.getenv('NAME'), 
                                    user=os.getenv('USER'), 
                                    password=os.getenv('PASS'), 
                                    port=os.getenv('PORT'))
            if conn:
                return conn
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {str(e)}")
            return None  
        
    def tupla_ou_lista(self, cursor,tupla):
            results = []
            if (tupla == False):
                results = cursor.fetchall()
            else:   
                rows = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                for row in rows:
                    data_dict = {}
                    for i in range(len(column_names)):
                        data_dict[column_names[i]] = row[i]
                    results.append(data_dict)     
            return results   
          