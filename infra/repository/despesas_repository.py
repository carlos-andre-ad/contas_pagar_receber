from infra.configs.connection import DBConnectionHandler
from infra.entities.despesas import Despesas
from infra.entities.organizacoes import Organizacoes
from infra.configs.log import LogApp
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from datetime import datetime

class DespesasRepository:
    def __init__(self) -> None:
        self.log = LogApp("DespesasRepository")
        
    def listar(self, resposta=None):

        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Despesas).all()
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
    

    def insert_update(self, id, descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes, nome_org):
        
        data_pagamento = datetime.strptime(data_pagamento, "%d/%m/%Y").strftime("%Y-%m-%d")
        data_vencimento = datetime.strptime(data_vencimento, "%d/%m/%Y").strftime("%Y-%m-%d")    
        
        with DBConnectionHandler() as db:
            data = db.session.query(Organizacoes).filter(Organizacoes.nome==nome_org).one_or_none()   
            if (data == None):
                msg = f"Não foi possivel encontrar a organização {nome_org}"
                self.log.logg(metodo=f"insert_update({id})", mensagem=msg, tipo_mensagem="w")
                return False, msg
            else:
                id_org = data.id           
                if (id == ""):
                    return self.insert(db, descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes, id_org)
                else:
                    return self.update(db, id, descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes, id_org)
            
    
  
    def update(self, db,id, descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes, id_org):
          try:
              db.session.query(Despesas).filter(Despesas.id == id).update({ 'descricao': descricao,
                                                                            'data_pagamento': data_pagamento,
                                                                            'data_vencimento': data_vencimento,
                                                                            'valor': valor,
                                                                            'valor_pago': valor_pago,
                                                                            'id_organizacao' : id_org,
                                                                            'observacoes': observacoes })
              db.session.commit()
              self.log.logg(metodo=f"update({id})", tipo_mensagem="i")
              return True, None
          except Exception as exception:
              db.session.rollback()
              self.log.logg(mensagem=exception,tipo_mensagem="e")
              return False, exception
          
            
    def insert( self, db,descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes, id_org):
        
            try:
                query = text("SELECT nextval('contas_pagar_id_seq')")
                result = db.session.execute(query)
                id_seq = result.scalar()
                data_isert = Despesas(id=id_seq, 
                                      descricao=descricao,
                                      id_organizacao=id_org,
                                      data_pagamento=data_pagamento,
                                      data_vencimento=data_vencimento,
                                      valor=valor,
                                      valor_pago=valor_pago,
                                      observacoes=observacoes)
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
                data = db.session.query(Despesas).filter(Despesas.id == id).options(joinedload(Despesas.organizacao)).one_or_none()
                
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
                return False, exception
            
            
    def delete(self, id):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Despesas).filter(Despesas.id == id).delete()
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
                    'data_pagamento': item.data_pagamento,
                    'data_vencimento': item.data_vencimento,
                    'valor': item.valor,
                    'valor_pago': item.valor_pago,
                    'observacoes': item.observacoes}
        else:
            return {item.id, 
                    item.organizacao,
                    item.descricao, 
                    item.data_pagamento,
                    item.data_vencimento,
                    item.valor,
                    item.valor_pago,
                    item.observacoes}