from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import user_auth, inventry, buyer
from routers import inventry, user_router, buyer


user_auth.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)


app.include_router(user_router.router)
app.include_router(inventry.router)
app.include_router(buyer.router)

@app.get("/api")
def base_root():
    return {"message": "hello world"}

# @app.post("/api")
# def base_root():
#     return {"message": "hello world"}

# @app.put("/api")
# def base_root():
#     return {"message": "hello world"}

# @app.delete("/api")
# def base_root():
#     return {"message": "hello world"}