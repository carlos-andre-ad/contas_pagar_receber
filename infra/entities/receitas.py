
from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Double, DateTime,ForeignKey,Text
from sqlalchemy.orm import relationship

class Receitas(Base):
    __tablename__ = "contas_receber"
    
    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    data_recebimento = Column(DateTime, nullable=False)
    valor = Column(Double, nullable=False)
    observacoes = Column(Text, nullable=True)
    id_organizacao = Column(String, ForeignKey("pessoa.id"))
    organizacao = relationship("Organizacoes")
    