from ast import Str
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Fila(BaseModel):
    id: Optional[int] = None
    posicao: int
    nome: str
    data_chegada: datetime
    prioridade: str
    atendido: bool