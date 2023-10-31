
import DB.conn as bd
import DB.entidades.pessoa as pessoa
from tkinter import messagebox
from datetime import datetime

class ContasReceber():
    def __init__(self):
        pass
    
    def insert_update(self, id, desc, data, valor, obs, o):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn == None):
            return False
        try:
            cursor = conn.cursor()
            
            p = pessoa.Pessoa()
            org = p.buscar_nome(o, True)
            if (org == None):
                messagebox.showinfo("Atenção", f"Não foi possivel encontrar a organização {o} ")
                return False          
            
            data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
            
            if (id == ""):
                cursor.execute("INSERT INTO contas_receber(descricao, data_recebimento,  valor, observacoes,id_organizacao) " +
                            "VALUES ('" + str(desc) + "','" + data + "'," + valor + ",'" + obs + "'," + str(org['id']) + ")")
                
            else:
                if len(self.buscar(int(id))) == 0:
                    messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
                    return False
                else:
                    cursor.execute("UPDATE contas_receber set descricao = '" + str(desc) + "'," +
                                "data_recebimento = '" + data  + "'," +
                                "valor = " + valor  + "," +
                                "id_organizacao = " + str(org['id'])  + "," +
                                "observacoes = '" + str(obs)  + "' WHERE id = " + id 
                                ) 
            conn.commit() 
            conn.close()
        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Erro", f"Não foi possível salvar essa receita: {str(e)}")
            return False
        
        return True


    def buscar(self,id, tupla=True):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT c.ID, 
                                    c.descricao, 
                                    to_char(c.data_recebimento, 'DD/MM/YYYY') as data_recebimento,
                                    c.valor,
                                    c.observacoes,
                                    p.nome as organizacao
                                    FROM contas_receber c
                                    INNER JOIN pessoa p on p.id = c.id_organizacao
                                    WHERE c.id = {id}""")
            resultado = conexao.tupla_ou_lista(cursor,tupla)
            conn.close()
            if len(resultado) == 0:
                return None
            else:
                return resultado[0]
        
        
    def listar(self, tupla = False):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT ID, 
                                      descricao, 
                                      to_char(data_recebimento, 'DD/MM/YYYY') as data, 
                                      to_char(valor, 'R$999,999,999.99')
                                      FROM contas_receber""")
            
            resultado = conexao.tupla_ou_lista(cursor,tupla)
            conn.close()
            return resultado

        
        
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
                    conn.rollback()
                    conn.close()
                    messagebox.showerror("Erro", f"Não foi possível excluir essa receita: {str(e)}")
                    return False
                
            return True            
