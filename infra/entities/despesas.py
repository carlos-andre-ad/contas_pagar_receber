
from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Double, DateTime,ForeignKey, Text
from sqlalchemy.orm import relationship

class Despesas(Base):
    __tablename__ = "contas_pagar"
    
    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    data_pagamento = Column(DateTime, nullable=False)
    data_vencimento = Column(DateTime, nullable=False)
    valor = Column(Double, nullable=False)
    valor_pago = Column(Double, nullable=False)
    observacoes = Column(Text, nullable=True)
    id_organizacao = Column(String, ForeignKey("pessoa.id"))
    organizacao = relationship("Organizacoes")
    