from typing import Annotated, Union
from fastapi import FastAPI, Query, HTTPException
from sqlmodel import select
from .models import Hero, SessionDep, create_db_and_tables
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run at startup
    create_db_and_tables()
    yield
    

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/environment")
def get_environment():
    import os
    return {"environment": os.environ.get("ENVIRONMENT", "development")}

@app.post("/heroes")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return JSONResponse(status_code=201, content={"ok": True, "data": hero.model_dump()})

@app.get("/heroes")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit).order_by('name')).all()
    return JSONResponse(status_code=200, content={"ok": True, "data": list(map(lambda h: h.model_dump(), heroes))})

@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return JSONResponse(status_code=200, content={"ok": True, "data": hero.model_dump()})


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return JSONResponse(status_code=200, content={"ok": True, "message": "Hero deleted successfully"})

@app.put("/heroes/{hero_id}")
def update_hero(hero_id: int, hero: Hero, session: SessionDep):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    # Merge the existing data with the new data
    hero_data = hero.model_dump(exclude_unset=True)  # Only include fields provided in the request
    for key, value in hero_data.items():
        setattr(db_hero, key, value)  # Update the existing record with new values

    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    
    return JSONResponse(status_code=200, content={"ok": True, "data": db_hero.model_dump()})

# define cors middleware
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["web", "localhost"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)