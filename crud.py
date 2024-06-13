from sqlalchemy.orm import Session
import models
import schemas

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_cliente(db: Session, id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == id).first()

def get_all_cliente(db: Session):
    return db.query(models.Cliente).all()

def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(nome=cliente.nome, email=cliente.email, fone=cliente.fone)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, id: int):
    # Busca o cliente pelo ID
    cliente = db.query(models.Cliente).filter(models.Cliente.id == id).first()
    # Verifica se o cliente existe
    if cliente:
        # Deleta o cliente
        db.delete(cliente)
        # Confirma as mudanças no banco de dados
        db.commit()
        return True
    return False

def update_cliente(db: Session, cliente_id: int, cliente_update: schemas.ClienteUpdate):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if db_cliente is None:
        return None
    for key, value in cliente_update.dict().items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente
