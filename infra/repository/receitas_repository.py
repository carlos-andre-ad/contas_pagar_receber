from infra.configs.connection import DBConnectionHandler
from infra.entities.receitas import Receitas
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text

class ReceitasRepository:
    def listar(self, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Receitas).all()
                if data == None:
                    return True, []
                if (resposta == None):
                    return True, data
                else:
                   return True, [ self.monta_dados(item,resposta) for item in data]

            except Exception as exception:
                db.session.rollback()
                return False, exception
    

    def insert_update(self, id, descricao, data_recebimento, valor, observacoes):
        if (id == ""):
            return self.insert(descricao, data_recebimento, valor, observacoes)
        else:
            return self.update(id, descricao, data_recebimento, valor, observacoes)
        
  
    def update(self, id, descricao, data_recebimento, valor, observacoes):
      with DBConnectionHandler() as db:
          try:
              db.session.query(Receitas).filter(Receitas.id == id).update({ 'descricao': descricao,
                                                                            'data_recebimento': data_recebimento,
                                                                            'valor': valor,
                                                                            'observacoes': observacoes })
              db.session.commit()
              return True, None
          except Exception as exception:
                return False, exception
          
            
    def insert(self, descricao, data_recebimento, valor, observacoes):

        with DBConnectionHandler() as db:
            try:
                query = text("SELECT nextval('contas_receber_id_seq')")
                result = db.session.execute(query)
                id_seq = result.scalar()
                data_isert = Receitas(id=id_seq, 
                                      descricao=descricao,
                                      data_recebimento=data_recebimento,
                                      valor=valor,
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
                data = db.session.query(Receitas).filter(Receitas.id==id).one()
                
                if data == None:
                    return False, None
                
                if (resposta == None):
                    return True, data
                else:
                    return True, self.monta_dados(data,resposta)
                                        
            except NoResultFound:
                return False, None
            except Exception as e:
                db.session.rollback()
                return False, None
            
            
    def delete(self, id):
        with DBConnectionHandler() as db:
            try:
                db.session.query(Receitas).filter(Receitas.id == id).delete()
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
                    'data_recebimento': item.data_recebimento,
                    'valor': item.valor,
                    'observacoes': item.observacoes}
        else:
            return {item.id, 
                    item.id_organizacao,
                    item.organizacao.nome,
                    item.descricao, 
                    item.data_recebimento,
                    item.valor,
                    item.observacoes}