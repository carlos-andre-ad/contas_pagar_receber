from sqlalchemy import Table, Column, Integer, String, Text, Date, Double, Boolean,ForeignKey,ForeignKeyConstraint
from sqlalchemy.sql import text
from sqlalchemy.engine.reflection import Inspector
import os

# DROP TABLE usuario; DROP TABLE contas_pagar; DROP TABLE contas_receber; DROP TABLE pessoa; DROP TABLE migration;
class Migrate():
    
    def __init__(self,db):
        self.db = db
        self.table_despesas   = 'contas_pagar'
        self.table_receitas   = 'contas_receber'
        self.table_pessoa     = 'pessoa'
        self.table_migration  = 'migration'
        self.table_usuario    = 'usuario'
    
    def create_table(self):
        
            try:
                self.create_migration_table()
                self.create_usuario_table()
                self.create_pessoa_table()
                self.create_despesa_table()
                self.create_receita_table()
                
                #self.migration()
                
                return True, None  
            except Exception as e:
                self.db.session.rollback()
                return False, e
       
    def check_exist_table(self, table):
        inspector = Inspector.from_engine(self.db.get_engine())
        if table not in inspector.get_table_names():     
            return True
        else:
            return False                       
        
    def create_pessoa_table(self):
            table = Table(
                self.table_pessoa,
                self.db.metadata,
                Column(name='id', type_= Integer, primary_key=True, autoincrement=True,  server_default=(f"nextval('{self.table_pessoa}_id_seq'::regclass)")),
                Column(name='nome', type_= String(100), nullable=False, unique=True),
                Column(name='id_organizacao', type_= Integer, nullable=True),
                Column(name='tipo_fornecedor', type_= Boolean, default=False),
                Column(name='tipo_prestador', type_= Boolean, default=False),
                Column(name='tipo_cliente', type_= Boolean, default=False),
                Column(name='tipo_instit_financ', type_= Boolean, default=False),
            )
            table.create(self.db.get_engine(), checkfirst=True)

    def create_migration_table(self):
            table = Table(
                self.table_migration,
                self.db.metadata,
                Column(name='id',type_= Integer, primary_key=True, autoincrement=True),
                Column(name='arquivo',type_= String(200), nullable=False),
                Column(name='conteudo',type_= Text, nullable=False),
                Column(name='data',type_= Date, nullable=False)
            )
            table.create(self.db.get_engine(), checkfirst=True)

    def create_usuario_table(self):
            table = Table(
                self.table_usuario,
                self.db.metadata,
                Column(name='id',type_= Integer, primary_key=True, autoincrement=True,  server_default=(f"nextval('{self.table_usuario}_id_seq'::regclass)")),
                Column(name='email',type_= String(100), nullable=False),
                Column(name='senha',type_= String(200), nullable=False)
            )
            table.create(self.db.get_engine(), checkfirst=True)

    def create_despesa_table(self):
            table = Table(
                self.table_despesas,
                self.db.metadata,
                Column(name='id',type_= Integer, primary_key=True, autoincrement=True, server_default=(f"nextval('{self.table_despesas}_id_seq'::regclass)")),
                Column(name='id_organizacao',type_= Integer, nullable=False),
                Column(name='descricao',type_= String(100), nullable=False),
                Column(name='data_pagamento',type_= Date, nullable=False),
                Column(name='data_vencimento',type_= Date, nullable=False),
                Column(name='valor',type_= Double, nullable=False),
                Column(name='valor_pago',type_= Double, nullable=False),
                Column(name='observacoes',type_= Text, nullable=True),
                ForeignKeyConstraint(columns=['id_organizacao'], refcolumns=[f'{self.table_pessoa}.id'], name=f"fk_{self.table_despesas}_parent_{self.table_pessoa}"),     
            )
            table.create(self.db.get_engine(), checkfirst=True)
                
    def create_receita_table(self):
            table = Table(
                self.table_receitas,
                self.db.metadata,
                Column(name='id',type_= Integer, primary_key=True, autoincrement=True,  server_default=(f"nextval('{self.table_receitas}_id_seq'::regclass)")),
                Column(name='id_organizacao',type_= Integer, nullable=False),
                Column(name='descricao',type_= String(100), nullable=False),
                Column(name='data_recebimento',type_= Date, nullable=False),
                Column(name='valor',type_= Double, nullable=False),
                Column(name='observacoes',type_= Text, nullable=True),
                ForeignKeyConstraint(['id_organizacao'], [f'{self.table_pessoa}.id'], name=f"fk_{self.table_receitas}_parent_{self.table_pessoa}"),
            )
            table.create(self.db.get_engine(), checkfirst=True)
                
#    def migration(self):
#            dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "migration")
#            for sql in os.listdir(dir):
#                if sql.endswith('.sql'):
#                    query = text("SELECT id FROM migration WHERE arquivo = '" + sql + "'")
#                    result = self.db.session.execute(query)
#                    qr = result.scalar()
#                    if qr == None:
#                        sql_path = os.path.join(dir, sql)               
#                        with open(sql_path, 'r') as f:
#                            conteudo = f.read()    
#                            self.db.session.execute(text(conteudo))               
#                            query = text("INSERT INTO migration(arquivo, conteudo, data) VALUES('"+ sql + "','" + conteudo +"', CURRENT_DATE )")
#                            self.db.session.execute(query)                            