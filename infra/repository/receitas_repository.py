from infra.configs.connection import DBConnectionHandler
from infra.entities.receitas import Receitas
from infra.entities.organizacoes import Organizacoes
from infra.configs.log import LogApp
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text
from datetime import datetime
from sqlalchemy.orm import joinedload

class ReceitasRepository:
    def __init__(self) -> None:
        self.log = LogApp("ReceitasRepository")
            
    def listar(self, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Receitas).all()
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
    

    def insert_update(self, id, descricao, data_recebimento, valor, observacoes, nome_org):
        
        data_recebimento = datetime.strptime(data_recebimento, "%d/%m/%Y").strftime("%Y-%m-%d")
        
        with DBConnectionHandler() as db:
            data = db.session.query(Organizacoes).filter(Organizacoes.nome==nome_org).one_or_none()   
            if (data == None):
                msg = f"Não foi possivel encontrar a organização {nome_org}"
                self.log.logg(metodo=f"insert_update({id})", mensagem=msg, tipo_mensagem="w")
                return False, msg
            else:   
                id_org = data.id           
                if (id == ""):
                    return self.insert(db, descricao, data_recebimento, valor, observacoes, id_org)
                else:
                    return self.update(db, id, descricao, data_recebimento, valor, observacoes, id_org)
        
  
    def update(self,db, id, descricao, data_recebimento, valor, observacoes, id_org):
          try:
              db.session.query(Receitas).filter(Receitas.id == id).update({ 'descricao': descricao,
                                                                            'id_organizacao' : id_org,
                                                                            'data_recebimento': data_recebimento,
                                                                            'valor': valor,
                                                                            'observacoes': observacoes })
              db.session.commit()
              self.log.logg(metodo=f"update({id})", tipo_mensagem="i")
              return True, None
          except Exception as exception:
              self.log.logg(mensagem=exception,tipo_mensagem="e")
              return False, exception
          
            
    def insert(self, db, descricao, data_recebimento, valor, observacoes, id_org):
            try:
                query = text("SELECT nextval('contas_receber_id_seq')")
                result = db.session.execute(query)
                id_seq = result.scalar()
                data_isert = Receitas(id=id_seq, 
                                      id_organizacao=id_org,
                                      descricao=descricao,
                                      data_recebimento=data_recebimento,
                                      valor=valor,
                                      observacoes=observacoes)
                db.session.add(data_isert)
                db.session.commit()
                self.log.logg(metodo=f"insert({iid_seqd})", tipo_mensagem="i")
                return True, id_seq
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception
            

    def buscar(self, id, resposta=None):
        with DBConnectionHandler() as db:
            try:
                
                data = db.session.query(Receitas).filter(Receitas.id == id).options(joinedload(Receitas.organizacao)).one_or_none()
                
                if data == None:
                    r=False
                    d=None
                else:
                    if (resposta == None):
                        r=True
                        d=data
                    else:
                        r=True
                        d=self.monta_dados(data,resposta)
                        
                self.log.logg(metodo=f"buscar({id})", tipo_mensagem="i")
                
                return r, d
            
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, None
            
            
    def delete(self, id):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Receitas).filter(Receitas.id == id).delete()
                db.session.commit()
                self.log.logg(metodo=f"delete({id})", tipo_mensagem="i")
                return True, None
            except Exception as exception:
                db.session.rollback()
                self.log.logg(mensagem=exception,tipo_mensagem="e")
                return False, exception


    def monta_dados(self,item, resposta):   
        if resposta == True:
            return {'id': item.id,
                    'organizacao': item.organizacao,
                    'descricao': item.descricao,
                    'data_recebimento': item.data_recebimento,
                    'valor': item.valor,
                    'observacoes': item.observacoes}
        else:
            return {item.id, 
                    item.organizacao,
                    item.descricao, 
                    item.data_recebimento,
                    item.valor,
                    item.observacoes}