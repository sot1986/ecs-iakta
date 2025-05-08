import json
from os import environ
from typing import Annotated, Optional
from sqlmodel import Field, Session, SQLModel, create_engine
from fastapi import Depends

class Hero(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: Optional[int] = Field(default=None, nullable=True, index=True)
    secret_name: str

db_connection_data= json.loads(environ.get("FASTAPICLUSTER_SECRET"))
DB_HOST = db_connection_data.get("host")
DB_PORT = db_connection_data.get("port")
DB_USERNAME = db_connection_data.get("username")
DB_PASSWORD = db_connection_data.get("password")
DB_DATABASE = db_connection_data.get("dbname")
# DB_PORT = environ.get("DB_PORT", 5432)
# DB_DATABASE = environ.get("DB_DATABASE", "mydatabase")
# DB_USERNAME = environ.get("DB_USERNAME", "myuser")
# DB_PASSWORD = environ.get("DB_PASSWORD", "mypassword")

pg_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
print(f"PostgreSQL URL: {pg_url}")

connection_args = {}
engine = create_engine(pg_url, echo=True, connect_args=connection_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Database and tables created successfully.")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
