import os

# Define directory and file structure
structure = {
    "models": ["__init__.py", "models.py"],
    "schemas": ["__init__.py", "schemas.py"],
    "services": ["__init__.py", "views.py"],
    "routers": ["__init__.py", "urls.py"],
    "deps": ["__init__.py", "deps.py"],
    "__files__": ["main.py", "database.py", "requirements.txt"]
}

# Content for files
file_contents = {
    "main.py": """from fastapi import FastAPI
from routers import urls

app = FastAPI()

app.include_router(urls.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8082, reload=True)
""",
    "database.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

URL_DATABASE = ""

engine = create_engine(URL_DATABASE)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
""",
    "services/views.py": """from models import models
from database import engine
from database import db_dependency

models.Base.metadata.create_all(bind=engine)
""",
    "schemas/schemas.py": """from pydantic import BaseModel
""",
    "routers/urls.py": """from fastapi import APIRouter
from database import db_dependency

router = APIRouter()
""",
    "models/models.py": """from sqlalchemy import Boolean, Column, Integer, String
from database import Base
"""
}

def create_structure(base_path, struct):
    for key, value in struct.items():
        if key == "__files__":
            for filename in value:
                filepath = os.path.join(base_path, filename)
                content = file_contents.get(filename, "")
                with open(filepath, "w") as f:
                    f.write(content)
        else:
            dir_path = os.path.join(base_path, key)
            os.makedirs(dir_path, exist_ok=True)
            for filename in value:
                file_path = os.path.join(dir_path, filename)
                rel_path = f"{key}/{filename}"
                content = file_contents.get(rel_path, "")
                with open(file_path, "w") as f:
                    f.write(content)

# Run the structure creation
create_structure(".", structure)
