from infra.configs.connection import DBConnectionHandler
from infra.entities.organizacoes import Organizacoes
from sqlalchemy.orm.exc import NoResultFound
from tkinter import messagebox
from sqlalchemy import text

class OrganizacoesRepository:
    
    def listar(self, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Organizacoes).all()
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

    def insert_update(self, id, nome):
        org = self.buscar_nome(nome, True)
        if (id == ""):
            if (org != None):
                messagebox.showinfo("Atenção", f"A organização {nome} já está cadastrada")
                return False
            
            return self.insert(nome)
        else:
            
            if org != None and id != org['id']:
                messagebox.showinfo("Atenção", f"A organização {nome} já está cadastrada")
                return False
            
            return self.update(id, nome)
  
    def update(self, id, nome):
      with DBConnectionHandler() as db:
          try:
              db.session.query(Organizacoes).filter(Organizacoes.id == id).update({ "nome": nome })
              db.session.commit()
              return True, None
          except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível alterar a organização: {str(e)}")
                return False, None
          
            
    def insert(self, nome):

        with DBConnectionHandler() as db:
            try:
                query = text("SELECT nextval('pessoa_id_seq')")
                result = db.session.execute(query)
                id_seq = result.scalar()
                data_isert = Organizacoes(id=id_seq, nome=nome)
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
                data = db.session.query(Organizacoes).filter(Organizacoes.id==id).one()
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

  
    def buscar_nome(self, nome, resposta=None):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Organizacoes).filter(Organizacoes.nome==nome).one()

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
                db.session.query(Organizacoes).filter(Organizacoes.id == id).delete()
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                messagebox.showerror("Erro", f"Não foi possível excluir essa organização: {str(e)}")
                return False

    def monta_dados(self,item, resposta):   
        if resposta == True:
            return {'id': item.id,'nome': item.nome}
        else:
            return {item.id, item.nome}
