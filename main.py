from fastapi import FastAPI
from db.database import test_connection

app = FastAPI(title="Penny")

@app.on_event("startup")
def startup_event():
    test_connection()

@app.get("/")
def root():
    return {"Message" : "Hello world!"}