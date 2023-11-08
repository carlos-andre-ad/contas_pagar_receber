
import infra.conn as bd
from tkinter import messagebox

class Pessoa():
    def __init__(self):
        pass
    
    def insert_update(self, id, nome, idOrganizacao, tipoFornecedor, tipoPrestador, tipoCliente, tipoInstFinan):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn == None):
            return False
        try:
            cursor = conn.cursor()
            if (id == ""):
                cursor.execute("INSERT INTO pessoa(nome, id_organizacao,  tipo_fornecedor, tipo_prestador,tipo_cliente, tipo_instit_financ) " +
                               "VALUES ('" + str(nome) + "'," + idOrganizacao + "," + tipoFornecedor + "," + tipoPrestador + "," + tipoCliente + "," + tipoInstFinan + ")")
                
            else:
                if len(self.buscar(int(id))) == 0:
                    messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
                    return False
                else:
                    cursor.execute("UPDATE pessoa set nome = '" + str(nome) + "'," +
                                "id_organizacao = " + idOrganizacao  + "," +
                                "tipo_fornecedor = " + tipoFornecedor  + "," +
                                "tipo_prestador = " + tipoPrestador  + "," +
                                "tipo_cliente = " + tipoCliente  + "," +
                                "tipo_instit_financ = " + tipoInstFinan  + "," + "' WHERE id = " + id 
                                ) 
            conn.commit() 
            conn.close()
        except Exception as e:
            conn.rollback
            conn.close()
            messagebox.showerror("Erro", f"Não foi possível salvar o registor: {str(e)}")
            return False
        
        return True


    def buscar(self,id, tupla=True):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT ID, 
                                    nome, 
                                    id_organizacao,
                                    tipo_fornecedor,
                                    tipo_prestador,
                                    tipo_cliente,
                                    tipo_instit_financ
                                    FROM pessoa WHERE id = {id}""")
            
            resultado = conexao.tupla_ou_lista(cursor,tupla)
            conn.close()
            if len(resultado) == 0:
                return None
            else:
                return resultado[0]
        
    def buscar_nome(self,nome, tupla=True):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT id, nome FROM pessoa WHERE nome = '{nome}'""")
            
            resultado = conexao.tupla_ou_lista(cursor,tupla)
            conn.close()
            if len(resultado) == 0:
                return None
            else:
                return resultado[0]
        
        
    def listar(self, tupla = False):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute(f"""SELECT ID, 
                                    nome, 
                                    id_organizacao,
                                    tipo_fornecedor,
                                    tipo_prestador,
                                    tipo_cliente,
                                    tipo_instit_financ
                                FROM pessoa""")
            resultado = conexao.tupla_ou_lista(cursor,tupla)
            conn.close()
            return resultado

        
    def delete(self,id):
            conexao = bd.Conexao()
            conn = conexao.conexao()
            if (conn != None):
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM pessoa WHERE id = '" + str(id) + "'")
                    conn.commit()
                    conn.close()
                except Exception as e:
                    conn.rollback()
                    conn.close()
                    messagebox.showerror("Erro", f"Não foi possível excluir o registro: {str(e)}")
                    return False
                
            return True            
