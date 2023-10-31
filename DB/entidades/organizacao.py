
import DB.conn as bd
import DB.entidades.pessoa as pessoa
from tkinter import messagebox

class Organizacao():
    def __init__(self):
        pass
    
    def insert_update(self, id, nome):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn == None):
            return False
        try:
            cursor = conn.cursor()       
            p = pessoa.Pessoa()
            
            if (id == ""):
                org = p.buscar_nome(nome, True)
                if (org != None):
                    messagebox.showinfo("Atenção", f"A organização {nome} já está cadastrada")
                    return False                  
                cursor.execute("INSERT INTO pessoa(nome) " + "VALUES ('" + str(nome) +  "')")
                
            else:
                org = self.buscar(int(id))
                
                if (org == None):
                    messagebox.showinfo("Atenção", f"O ID {id} não está presente na tabela")
                    return False
                else:
                    cursor.execute("UPDATE pessoa set nome = '" + str(nome) + "' WHERE id = " + str(org['id']) + "" ) 
            conn.commit() 
            conn.close()
        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Erro", f"Não foi possível salvar a organização: {str(e)}")
            return False
        
        return True


    def buscar(self,id, tupla=True):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT id, nome, id_organizacao,tipo_fornecedor, tipo_prestador,tipo_cliente, tipo_instit_financ FROM pessoa  WHERE id = {id}""")
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
            cursor.execute(f"""SELECT id, nome, id_organizacao,tipo_fornecedor, tipo_prestador,tipo_cliente, tipo_instit_financ FROM pessoa""")
            
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
                    messagebox.showerror("Erro", f"Não foi possível excluir essa organização: {str(e)}")
                    return False
                
            return True            
