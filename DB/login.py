
import DB.conn as bd

class Login():
    def __init__(self):
        pass
        
    def logar(self,email,senha, tupla=True):
        conexao = bd.Conexao()
        conn = conexao.conexao()
        if (conn != None):
            cursor = conn.cursor()
            cursor.execute(f"""SELECT id FROM usuario WHERE email = '{email}' AND senha = '{senha}'""")
            
            resultado = conexao.tupla_ou_lista(cursor,tupla)
            conn.close()
            if len(resultado) == 0:
                return None
            else:
                return resultado[0]