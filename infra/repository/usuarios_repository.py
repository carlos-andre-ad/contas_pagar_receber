from infra.configs.connection import DBConnectionHandler
from infra.configs.migrate import Migrate
from infra.entities.usuarios import Usuarios
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text

class UsuariosRepository:
    
    def login(self, email,senha, resposta=None):
        with DBConnectionHandler() as db:
            try:
                migrate = Migrate(db)
                sucesso, exception = migrate.create_table()
                
                if (sucesso):
                    data = self.listar(resposta)
                    if len(data) == 0:
                        sucesso, excp = self.insert( email, senha)
                        if (sucesso):
                            db.session.commit()
                            return self.buscar_email(email)
                        else:
                            return False, excp
                    else:
                        return self.buscar_email_senha(email,senha)
                else:
                    return False, exception
            except Exception as e:
                db.session.rollback()
                return False, e


    
    def listar(self, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Usuarios).all()
                if data == None:
                    return True, []
                if (resposta == None):
                    return True, data
                else:
                    return [ self.monta_dados(item,resposta) for item in data]
            except Exception as exception:
                db.session.rollback()
                return False, exception

    def insert_update(self, id, email, senha):
        
        user = self.buscar_email(email, True)
        if (id == ""):
            if (user != None):
                return False, f"O usuário {email} já está cadastrada"
            
            return self.insert(email, senha)
        else:
            if user != None and id != user['id']:
                return False, f"O usuário {email} já está cadastrada"
            
            return self.update(id, email)
  
    def update(self, id, email):
      with DBConnectionHandler() as db:
          try:
              db.session.query(Usuarios).filter(Usuarios.id == id).update({ "email": email })
              db.session.commit()
              return True, None
          except Exception as e:
                return False, e
          
            
    def insert(self, email, senha):

        with DBConnectionHandler() as db:
            try:
                query = text("SELECT nextval('usuario_id_seq')")
                result = db.session.execute(query)
                id_seq = result.scalar()
                data_isert = Usuarios(id=id_seq, email=email, senha=senha)
                db.session.add(data_isert)
                db.session.commit()
                return True, id_seq
            except Exception as e:
                db.session.rollback()
                return False, e
            
            
    def buscar(self, id, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Usuarios).filter(Usuarios.id==id).one()
                if data == None:
                    return False, None
                
                if (resposta == None):
                    return True, data
                else:
                    return True, self.monta_dados(data,resposta)
                                        
            except NoResultFound:
                return False, None
            except Exception as exception:
                db.session.rollback()
                return False, exception

  
    def buscar_email(self, email, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Usuarios).filter(Usuarios.email==email).one()

                if data == None:
                    return False, None

                if (resposta == None):
                    return True, data
                else:
                    return True, self.monta_dados(data,resposta)

            except NoResultFound:
                return False, None
            except Exception as exception:
                db.session.rollback()
                return False, exception
            
            
    def buscar_email_senha(self, email,senha):
        with DBConnectionHandler() as db:
            try:
                msg = "Email ou senha inválido"
                data = db.session.query(Usuarios).filter(Usuarios.email==email, Usuarios.senha==senha).one()
                if data == None:
                    return False, msg
                else:
                    return True, None
            except NoResultFound:
                return False, msg
            except Exception as exception:
                return False, exception
            
            
    def delete(self, id):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Usuarios).filter(Usuarios.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                return False, e

    def monta_dados(self,item, resposta):   
        if resposta == True:
            return {'id': item.id,'email': item.email}
        else:
            return {item.id, item.email}
