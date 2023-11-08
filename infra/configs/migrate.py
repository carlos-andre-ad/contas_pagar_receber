from sqlalchemy import create_engine, Table, Column, Integer, String, Text, Date, Double, Boolean
from sqlalchemy.sql import text
from contextlib import contextmanager

class Migrate():
    
    def __init__(self, db):
        self.db = db
    
    def create_table(self):
       try:
            self.create_migration_table()
            self.create_despesa_table()
            self.create_pessoa_table()
            self.create_receita_table()
            self.create_usuario_table()
            return True, None   
       except Exception as e:
           return False, e
        
    
    def create_migration_table(self):
            table = Table(
                'migration',
                self.db.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('arquivo', String(200), nullable=False),
                Column('conteudo', Text, nullable=False),
                Column('data', Date, nullable=False)
            )
            if not table.exists():
                table.create()
                
    def create_usuario_table(self):
            table = Table(
                'usuario',
                self.db.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('email', String(100), nullable=False),
                Column('senha', String(200), nullable=False)
            )
            if not table.exists():
                table.create()
                
    def create_despesa_table(self):
            table = Table(
                'contas_pagar',
                self.db.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('descricao', String(100), nullable=False),
                Column('data_pagamento', Date, nullable=False),
                Column('data_vencimento', Date, nullable=False),
                Column('valor', Double, nullable=False),
                Column('valor_pago', Double, nullable=False),
                Column('observacoes', Text, nullable=True)
            )
            if not table.exists():
                table.create()
                
    def create_receita_table(self):
            table = Table(
                'contas_pagar',
                self.db.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('descricao', String(100), nullable=False),
                Column('data_recebimento', Date, nullable=False),
                Column('valor', Double, nullable=False),
                Column('observacoes', Text, nullable=True)
            )
            if not table.exists():
                table.create()
                
    def create_pessoa_table(self):
            table = Table(
                'pessoa',
                self.db.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('nome', String(100), nullable=False),
                Column('id_organizacao', Integer, nullable=False),
                Column('tipo_fornecedor', Boolean, nullable=False, default=False),
                Column('tipo_prestador', Boolean, nullable=False, default=False),
                Column('tipo_cliente', Boolean, nullable=False, default=False),
                Column('tipo_instit_financ', Boolean, nullable=False, default=False),
            )
            if not table.exists():
                table.create()