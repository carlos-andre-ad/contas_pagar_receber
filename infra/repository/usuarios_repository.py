from infra.configs.connection import DBConnectionHandler
from infra.entities.usuarios import Usuarios
from sqlalchemy.orm.exc import NoResultFound
from tkinter import messagebox
from sqlalchemy import text

class UsuariosRepository:
    
    def login(self, email,senha, resposta=None):
        with DBConnectionHandler() as db:
            try:
                
                data = self.listar(resposta)
                if len(data) == 0:
                    self.insert( email, senha)
                    


    
    def listar(self, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Usuarios).all()
                if data == None:
                    return []
                if (resposta == None):
                    return data
                else:
                    return [ self.monta_dados(item,resposta) for item in data]
            except Exception as e:
                db.session.rollback()
                messagebox.showerror("Erro", f"{str(e)}")
                return False 

    def insert_update(self, id, email, senha):
        user = self.buscar_email(email, True)
        if (id == ""):
            if (user != None):
                messagebox.showinfo("Atenção", f"O usuário {email} já está cadastrada")
                return False
            
            return self.insert(email, senha)
        else:
            
            if user != None and id != user['id']:
                messagebox.showinfo("Atenção", f"O usuário {email} já está cadastrada")
                return False
            
            return self.update(id, email)
  
    def update(self, id, email):
      with DBConnectionHandler() as db:
          try:
              db.session.query(Usuarios).filter(Usuarios.id == id).update({ "email": email })
              db.session.commit()
              return True, None
          except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível alterar a organização: {str(e)}")
                return False, None
          
            
    def insert(self, email, senha):

        with DBConnectionHandler() as db:
            try:
                query = text("SELECT nextval('usuario_id_seq')")
                result = db.session.execute(query)
                id_seq = result.scalar()
                data_isert = Usuarios(id=id_seq, email=email)
                db.session.add(data_isert)
                db.session.commit()
                return True, id_seq
            except Exception as e:
                db.session.rollback()
                messagebox.showerror("Erro", f"Não foi possível salvar a organização: {str(e)}")
                return False, None
            
            
    def buscar(self, id, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Usuarios).filter(Usuarios.id==id).one()
                if data == None:
                    return None
                
                if (resposta == None):
                    return data
                else:
                    return self.monta_dados(data,resposta)
                                        
            except NoResultFound:
                return None
            except Exception as exception:
                db.session.rollback()
                raise exception

  
    def buscar_email(self, email, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Usuarios).filter(Usuarios.email==email).one()

                if data == None:
                    return None

                if (resposta == None):
                    return data
                else:
                    return self.monta_dados(data,resposta)

            except NoResultFound:
                return None
            except Exception as exception:
                db.session.rollback()
                raise exception
            
            
    def delete(self, id):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Usuarios).filter(Usuarios.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                messagebox.showerror("Erro", f"Não foi possível excluir essa organização: {str(e)}")
                return False

    def monta_dados(self,item, resposta):   
        if resposta == True:
            return {'id': item.id,'email': item.email}
        else:
            return {item.id, item.email}
