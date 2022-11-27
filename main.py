import json
import pathlib
from typing import List, Union

from fastapi import FastAPI, Response, Depends, HTTPException
from sqlmodel import Session, select


from models import Fila
from database import FilaModel, engine

app = FastAPI()

data = []

@app.on_event("startup")
async def startup_event():
    DATAFILE = pathlib.Path() / 'data' / 'fila.json'

    session = Session(engine)

    stmt = select(FilaModel)
    result = session.exec(stmt).first()

    if result is None:
        with open(DATAFILE, 'r') as f:
            filas = json.load(f)
            for fila in filas:
                session.add(FilaModel(**fila))
        session.commit()

    session.close()

def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
async def home():
    return {"message": "API fila de atendimento"}



@app.get('/fila/', response_model=List[Fila])
def filas(session: Session = Depends(get_session)):
    stmt = select(FilaModel)
    result = session.exec(stmt).all()
    if len(result) == 0:
        raise HTTPException(status_code=200, detail="Fila Vazia")
    return result

@app.get('/fila/{fila_id}', response_model=Union[Fila, str])
def filas(fila_id: int, response: Response, session: Session = Depends(get_session)):
    fila = session.get(FilaModel, fila_id)  
    if fila is None:
        response.status_code = 404
        return {"ID não encontrada na fila"}
    return fila


@app.post('/fila/', response_model=Fila, status_code=201)
def create_fila(fila: FilaModel, session: Session = Depends(get_session)):
    session.add(fila)
    session.commit()
    session.refresh(fila)
    return fila



@app.put('/fila/{fila_id}', response_model=Union[Fila, str])
def filas(fila_id: int, updated_fila: Fila, response: Response, session: Session = Depends(get_session)):
   
    fila = session.get(FilaModel, fila_id)

    if fila is None:
        response.status_code = 404
        return "ID não encontrada na fila"

    fila_dict = updated_fila.dict(exclude_unset=True)
    for key, val in fila_dict.items():
        setattr(fila, key, val)

    session.add(fila)
    session.commit()
    session.refresh(fila)
    return fila

@app.delete('/fila/{fila_id}')
def filas(fila_id: int, response: Response, session: Session = Depends(get_session)):
 
    fila = session.get(FilaModel, fila_id)

    if fila is None:
        response.status_code = 404
        return "ID não encontrada na fila"

    session.delete(fila)
    session.commit()
    return Response(status_code=200)