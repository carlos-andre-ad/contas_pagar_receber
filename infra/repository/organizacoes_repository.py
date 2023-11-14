from infra.configs.connection import DBConnectionHandler
from infra.entities.organizacoes import Organizacoes
from infra.configs.log import LogApp
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text

class OrganizacoesRepository:
    def __init__(self) -> None:
        self.log = LogApp("OrganizacoesRepository")    
    
    def listar(self, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Organizacoes).all()
                if data == None:
                    r=True 
                    d=[]
                else:                
                    if (resposta == None):
                        r=True 
                        d=data
                    else:
                        r=True
                        d=[ self.monta_dados(item,resposta) for item in data]
                
                self.log.logg(metodo="listar()", tipo_mensagem="i")
                return r, d
            
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception
            

    def insert_update(self, id, nome):
        
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Organizacoes).filter(Organizacoes.nome==nome).one_or_none()
                msg = "Já existe uma organização com esse nome"
                if (id == ""):
                    
                    if (data != None):
                        
                        self.log.logg(metodo="insert_update()", mensagem=msg ,tipo_mensagem="w")
                        
                        return False, msg
                    
                    return self.insert(nome, db)
                
                else:
                    
                    if data != None and int(id) != int(data['id']):
                        
                        self.log.logg(metodo="insert_update()", mensagem=msg ,tipo_mensagem="w")
                        
                        return False, msg
                    
                    return self.update(id, nome, db)
                
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception        
        
        
    def update(self, id, nome, db):

          try:
              db.session.query(Organizacoes).filter(Organizacoes.id == id).update({ "nome": nome })
              db.session.commit()
              self.log.logg(metodo=f"update({id})", tipo_mensagem="i")
              return True, None
          except Exception as exception:
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception
            
            
    def insert(self, nome, db):
            try:
                query = text("SELECT nextval('pessoa_id_seq')")
                result = db.session.execute(query)
                id_seq = result.scalar()
                data_isert = Organizacoes(id=id_seq, nome=nome)
                db.session.add(data_isert)
                db.session.commit()
                self.log.logg(metodo=f"insert({id_seq})", tipo_mensagem="i")
                return True, id_seq
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception
            
            
    def buscar(self, id, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Organizacoes).filter(Organizacoes.id==id).one_or_none()
                msg = "Sucesso"
                tipo_mensagem = "i"                
                if data == None:
                    r=False, 
                    d=msg
                    tipo_mensagem = "w" 
                    msg = "Organização não encontrada"
                else:
                    if (resposta == None):
                        r=True, 
                        d=data
                    else:
                        r=True, 
                        d=self.monta_dados(data,resposta)
                        
                self.log.logg(metodo=f"buscar({id})", mensagem=msg, tipo_mensagem=tipo_mensagem)
                                            
                return r, d
            
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception

  
    def buscar_nome(self, nome, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Organizacoes).filter(Organizacoes.nome==nome).one_or_none()
                msg = "Sucesso"
                tipo_mensagem = "i"                
                if data == None:
                    r=False, 
                    d=msg
                    tipo_mensagem = "w" 
                    msg = "Organização não encontrada"
                else:
                    if (resposta == None):
                        r=True, 
                        d=data
                    else:
                        r=True, 
                        d=self.monta_dados(data,resposta)
                        
                self.log.logg(metodo=f"buscar({nome})", mensagem=msg, tipo_mensagem=tipo_mensagem)

                return r, d
            
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception
            
            
    def delete(self, id):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Organizacoes).filter(Organizacoes.id == id).delete()
                db.session.commit()
                return True,None
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception

    def monta_dados(self,item, resposta):   
        if resposta == True:
            return {'id': item.id,'nome': item.nome} 
        else:
            return {item.id, item.nome}
        
