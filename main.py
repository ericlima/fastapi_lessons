from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import crud
import schemas
import models
from database import SessionLocal, engine

# Create all tables in the database.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a route to serve the favicon.ico
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.ico")

@app.get('/')
def home():
    return {"message": "Welcome to the FastAPI application!"}

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/cliente/", response_model=list[schemas.Cliente])
def get_all(db: Session = Depends(get_db)):
    return crud.get_all_cliente(db)

@app.post("/cliente/", response_model=schemas.Cliente)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.create_cliente(db=db, cliente=cliente)

@app.get("/cliente/{id}", response_model=schemas.Cliente)
def read_cliente(id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, id=id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return db_cliente

@app.delete("/cliente/{id}", response_model=schemas.Message)
def delete_cliente_endpoint(id: int, db: Session = Depends(get_db)):
    sucesso = crud.delete_cliente(db, id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"message": "Cliente deletado com sucesso"}


@app.put("/cliente/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente_update: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    db_cliente = crud.update_cliente(db, cliente_id, cliente_update)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente


