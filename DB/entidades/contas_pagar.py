
import DB.conn as bd
import DB.entidades.pessoa as pessoa
from tkinter import messagebox
from datetime import datetime


class ContasPagar():
    def __init__(self):
        pass
    
    def insert_update(self, id, desc, data_pag, data_ven,valor, valor_pago, obs, o):
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
            
            data_pag = datetime.strptime(data_pag, "%d/%m/%Y").strftime("%Y-%m-%d")
            data_ven = datetime.strptime(data_ven, "%d/%m/%Y").strftime("%Y-%m-%d")
            
            if (id == ""):
                cursor.execute("INSERT INTO contas_pagar(descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes, id_organizacao) " +
                               "VALUES ('" + str(desc) + "','" + data_pag + "','" + data_ven + "'," + valor + "," + valor_pago + ",'" + obs + "'," + str(org['id']) + ")")
                
            else:
                if len(self.buscar(int(id))) == 0:
                    messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
                    return False
                else:
                    cursor.execute("UPDATE contas_pagar set descricao = '" + str(desc) + "'," +
                                "data_pagamento = '" + data_pag  + "'," +
                                "data_vencimento = '" + data_ven  + "'," +
                                "valor = " + valor  + "," +
                                "id_organizacao = " + str(org['id'])  + "," +
                                "valor_pago = " + valor_pago  + "," +
                                "observacoes = '" + str(obs)  + "' WHERE id = " + id 
                                ) 
            conn.commit() 
            conn.close()
        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Erro", f"Não foi possível salvar essa despesa: {str(e)}")
            return False
        
        return True


    def buscar(self,id, tupla=True):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT c.ID, 
                                    c.descricao, 
                                    to_char(c.data_pagamento, 'DD/MM/YYYY') as data_pagamento, 
                                    to_char(c.data_vencimento, 'DD/MM/YYYY') as data_vencimento,
                                    c.valor,
                                    c.valor_pago, 
                                    c.observacoes,
                                    p.nome as organizacao
                                    FROM contas_pagar c
                                    INNER JOIN pessoa p on p.id = c.id_organizacao
                                    WHERE c.id = {id}""")
            resultado = conexao.tupla_ou_lista(cursor,tupla)
            conn.close()
            if len(resultado) == 0:
                return None
            else:
                return resultado[0]
        
        
    def listar(self, tupla=False):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT ID, 
                                    descricao, 
                                    to_char(data_pagamento, 'DD/MM/YYYY') as data_pagamento, 
                                    to_char(data_vencimento, 'DD/MM/YYYY') as data_vencimento,
                                    to_char(valor, 'R$999,999,999.99') as valor,
                                    to_char(valor_pago, 'R$999,999,999.99') as valor_pago
                                FROM contas_pagar""")
            
            resultado = conexao.tupla_ou_lista(cursor,tupla)
            conn.close()
            return resultado

        
        
    def delete(self,id):
            conexao = bd.Conexao()
            conn = conexao.conexao()
            if (conn != None):
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM contas_pagar WHERE id = '" + str(id) + "'")
                    conn.commit() 
                    conn.close()
                except Exception as e:
                    conn.rollback()
                    conn.close()
                    messagebox.showerror("Erro", f"Não foi possível excluir essa despesa: {str(e)}")
                    return False
                
            return True            
