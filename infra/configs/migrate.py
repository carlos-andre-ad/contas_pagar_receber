from infra.configs.connection import DBConnectionHandler
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Date
from sqlalchemy.sql import text
from contextlib import contextmanager
import datetime

class Migrate:
    
    
    def create_table(self):
        self.create_migration_table()
    
    def create_migration_table(self):
        with DBConnectionHandler() as db:
            migration_table = Table(
                'migration',
                db.metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('arquivo', String(200), nullable=False),
                Column('conteudo', Text, nullable=False),
                Column('data', Date, nullable=False)
            )
            if not migration_table.exists():
                migration_table.create()