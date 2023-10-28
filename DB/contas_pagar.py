
import DB.conn as bd
from tkinter import messagebox

class ContasPagar():
    def __init__(self):
        pass
    
    def insert_update(self, id, desc, data_pag, data_ven,valor, valor_pago, obs):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn == None):
            return False
        try:
            cursor = conn.cursor()
            if (id == ""):
                cursor.execute("INSERT INTO contas_pagar(descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes) " +
                            "VALUES ('" + str(desc) + "','" + data_pag + "','" + data_ven + "'," + valor + "," + valor_pago + ",'" + obs + "')")
                
            else:
                if len(self.buscar(int(id))) == 0:
                    messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
                    return False
                else:
                    cursor.execute("UPDATE contas_pagar set descricao = '" + str(desc) + "'," +
                                "data_pagamento = '" + data_pag  + "'," +
                                "data_vencimento = '" + data_ven  + "'," +
                                "valor = " + valor  + "," +
                                "valor_pago = " + valor_pago  + "," +
                                "observacoes = '" + str(obs)  + "' WHERE id = " + id 
                                ) 
            conn.commit() 
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar essa despesa: {str(e)}")
            conn.close()
            return False
        
        return True


    def buscar(self,id):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT ID, 
                                    descricao, 
                                    to_char(data_pagamento, 'DD/MM/YYYY') as data_pagamento, 
                                    to_char(data_vencimento, 'DD/MM/YYYY') as data_vencimento,
                                    valor,
                                    valor_pago, 
                                    observacoes 
                                    FROM contas_pagar WHERE id = {id}""")
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
                                      to_char(data_pagamento, 'DD/MM/YYYY') as data_pagamento, 
                                      to_char(data_vencimento, 'DD/MM/YYYY') as data_vencimento,
                                      to_char(valor, 'R$999,999,999.99'),
                                      to_char(valor_pago, 'R$999,999,999.99') 
                                      FROM contas_pagar""")
            results = cursor.fetchall()
            conn.close()
            return results 
        
        
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
                    messagebox.showerror("Erro", f"Não foi possível excluir essa despesa: {str(e)}")
                    conn.close()
                    return False
                
            return True            
