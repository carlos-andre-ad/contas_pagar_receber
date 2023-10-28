
import DB.conn as bd
from tkinter import messagebox

class ContasReceber():
    def __init__(self):
        pass
    
    def insert_update(self, id, desc, data, valor, obs):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn == None):
            return False
        try:
            cursor = conn.cursor()
            if (id == ""):
                cursor.execute("INSERT INTO contas_receber(descricao, data_recebimento,  valor, observacoes) " +
                            "VALUES ('" + str(desc) + "','" + data + "'," + valor + ",'" + obs + "')")
                
            else:
                if len(self.buscar(int(id))) == 0:
                    messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
                    return False
                else:
                    cursor.execute("UPDATE contas_receber set descricao = '" + str(desc) + "'," +
                                "data_recebimento = '" + data  + "'," +
                                "valor = " + valor  + "," +
                                "observacoes = '" + str(obs)  + "' WHERE id = " + id 
                                ) 
            conn.commit() 
            conn.close()
        except Exception as e:
            conn.close()
            messagebox.showerror("Erro", f"Não foi possível salvar essa receita: {str(e)}")
            return False
        
        return True


    def buscar(self,id):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT ID, 
                                    descricao, 
                                    to_char(data_recebimento, 'DD/MM/YYYY') as data,
                                    valor,
                                    observacoes 
                                    FROM contas_receber WHERE id = {id}""")
            results = cursor.fetchall()
            conn.close()
            return results 
        
        
    def read(self):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT ID, 
                                      descricao, 
                                      to_char(data_recebimento, 'DD/MM/YYYY') as data, 
                                      to_char(valor, 'R$999,999,999.99')
                                      FROM contas_receber""")
            results = cursor.fetchall()
            conn.close()
            return results 
        
        
    def delete(self,id):
            conexao = bd.Conexao()
            conn = conexao.conexao()
            if (conn != None):
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM contas_receber WHERE id = '" + str(id) + "'")
                    conn.commit()
                    conn.close()
                except Exception as e:
                    conn.close()
                    messagebox.showerror("Erro", f"Não foi possível excluir essa receita: {str(e)}")
                    return False
                
            return True            
