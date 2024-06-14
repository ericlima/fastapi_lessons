from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
import models
import schemas
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException, status

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
    try:
        db_cliente = models.Cliente()
        for key, value in cliente.model_dump().items():
            setattr(db_cliente, key, value)
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O cliente com este email já existe."
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor ao tentar criar o cliente."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro inesperado."
        )


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

def update_cliente(db: Session, id: int, cliente_update: schemas.ClienteUpdate):
    try:
        db_cliente = db.query(models.Cliente).filter(models.Cliente.id == id).first()
        if db_cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado."
            )
        for key, value in cliente_update.dict().items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O cliente com este email já existe."
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor ao tentar atualizar o cliente."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro inesperado."
        )

