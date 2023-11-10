from infra.configs.base import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

class Usuarios(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String, nullable=False)

    # def __repr__(self):
    #    return f"Organizacoes [nome={self.nome}]"
#