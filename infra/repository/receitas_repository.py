from infra.configs.connection import DBConnectionHandler
from infra.entities.receitas import Receitas
from infra.entities.organizacoes import Organizacoes
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text
from datetime import datetime

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
    

    def insert_update(self, id, descricao, data_recebimento, valor, observacoes, nome_org):
        
        data_recebimento = datetime.strptime(data_recebimento, "%d/%m/%Y").strftime("%Y-%m-%d")
        
        with DBConnectionHandler() as db:
            data = db.session.query(Organizacoes).filter(Organizacoes.nome==nome_org).one_or_none()   
            if (data == None):
                return False, f"Não foi possivel encontrar a organização {nome_org}"
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
              return True, None
          except Exception as exception:
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
                return True, id_seq
            except Exception as exception:
                db.session.rollback()
                return False, exception
            
            
    def buscar(self, id, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Receitas).filter(Receitas.id==id).one_or_none()
                
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