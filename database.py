from typing import Optional
from datetime import datetime



from sqlmodel import Field, SQLModel, create_engine, DateTime, Column

DB_FILE = 'db.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)


class FilaModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posicao: Optional[int] = Field(default=None)
    nome: str = Field(max_length=20)
    data_chegada: datetime
    prioridade: str = Field(max_length=1)
    atendido: bool = Field(default=True, nullable=False)

def create_table():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_table()