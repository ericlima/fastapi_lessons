from sqlalchemy import Column, Integer, String
from database import Base  # Importação relativa do Base

class Item(Base):  # Herda de Base
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    fone = Column(String(255), index=True)
    
    