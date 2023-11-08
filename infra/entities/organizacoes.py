from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

class Organizacoes(Base):
    __tablename__ = "pessoa"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, unique=True)
    id_organizacao = Column(String, nullable=True)
    tipo_fornecedor = Column(Boolean, nullable=True, default=False)
    tipo_prestador = Column(Boolean, nullable=True, default=False)
    tipo_cliente = Column(Boolean, nullable=True, default=False)
    tipo_instit_financ = Column(Boolean, nullable=True, default=False)
    
    despesas = relationship("Despesas", backref="contas_pagar", lazy="subquery")

    # def __repr__(self):
    #    return f"Organizacoes [nome={self.nome}]"
#