from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

class ClienteBase(BaseModel):
    nome: str
    email: str
    fone: str

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int

    class Config:
        orm_mode = True
        
class Message(BaseModel):
    message: str