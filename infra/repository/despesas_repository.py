from infra.configs.connection import DBConnectionHandler
from infra.entities.despesas import Despesas
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text

class DespesasRepository:
    def listar(self, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Despesas).all()
                if data == None:
                    return True, []
                if (resposta == None):
                    return True, data
                else:
                   return True, [ self.monta_dados(item,resposta) for item in data]

            except Exception as exception:
                db.session.rollback()
                return False, exception
    

    def insert_update(self, id, descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes):
        if (id == ""):
            return self.insert(descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes)
        else:
            return self.update(id, descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes)
        
  
    def update(self, id, descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes):
      with DBConnectionHandler() as db:
          try:
              db.session.query(Despesas).filter(Despesas.id == id).update({ 'descricao': descricao,
                                                                            'data_pagamento': data_pagamento,
                                                                            'data_vencimento': data_vencimento,
                                                                            'valor': valor,
                                                                            'valor_pago': valor_pago,
                                                                            'observacoes': observacoes })
              db.session.commit()
              return True, None
          except Exception as exception:
                return False, exception
          
            
    def insert(self, descricao, data_pagamento, data_vencimento, valor, valor_pago, observacoes):

        with DBConnectionHandler() as db:
            try:
                query = text("SELECT nextval('contas_pagar_id_seq')")
                result = db.session.execute(query)
                id_seq = result.scalar()
                data_isert = Despesas(id=id_seq, 
                                      descricao=descricao,
                                      data_pagamento=data_pagamento,
                                      data_vencimento=data_vencimento,
                                      valor=valor,
                                      valor_pago=valor_pago,
                                      observacoes=observacoes)
                db.session.add(data_isert)
                db.session.commit()
                return True, id_seq
            except Exception as exception:
                db.session.rollback()
                return False, exception
            
            
    def buscar(self, id, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Despesas).filter(Despesas.id==id).one()
                
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
            
            
    def delete(self, id):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Despesas).filter(Despesas.id == id).delete()
                db.session.commit()
                return True, None
            except Exception as exception:
                db.session.rollback()
                return False, exception


    def monta_dados(self,item, resposta):   
        if resposta == True:
            return {'id': item.id,
                    'id_organizacao':item.id_organizacao,
                    'organizacao': item.organizacao.nome,
                    'descricao': item.descricao,
                    'data_pagamento': item.data_pagamento,
                    'data_vencimento': item.data_vencimento,
                    'valor': item.valor,
                    'valor_pago': item.valor_pago,
                    'observacoes': item.observacoes}
        else:
            return {item.id, 
                    item.id_organizacao,
                    item.organizacao.nome,
                    item.descricao, 
                    item.data_pagamento,
                    item.data_vencimento,
                    item.valor,
                    item.valor_pago,
                    item.observacoes}