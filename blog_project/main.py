from fastapi import FastAPI
from app.database import engine, Base
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Blog API ishlamoqda!"}
