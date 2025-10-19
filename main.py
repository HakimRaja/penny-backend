from fastapi import FastAPI
from routes import user_route
from db.database import test_connection

app = FastAPI(title="Penny")

@app.on_event("startup")
def startup_event():
    test_connection()
app.include_router(user_route.router)

@app.get("/")
def root():
    return {"Message" : "Hello world!"}
