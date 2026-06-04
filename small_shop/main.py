from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from session import get_db
from model import User, Product
import bcrypt
from sqlalchemy import text

app = FastAPI()

# Helper functions
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )



@app.post("/signup")
def sign_up(
    name: str, 
    age: int, 
    password: str, 
    db: Session = Depends(get_db)
):
    hashed = hash_password(password)

    # Check if user exists
    name_user = db.execute(
        text("SELECT name FROM client WHERE name = :name"),
        {"name": name}
    ).first()

    if name_user:
        raise HTTPException(status_code=400, detail="USER ALREADY EXISTS")

    # Insert new user
    db.execute(
        text("INSERT INTO client (name, age, motdepass) VALUES (:name, :age, :password)"),
        {"name": name, "age": age, "password": hashed}
    )
    db.commit()

    return {"message": "USER ADDED SUCCESSFULLY !"}




@app.get("/signin")
def sign_in(
    name: str, 
    password: str, 
    db: Session = Depends(get_db)
):
    # Get user from database
    user = db.execute(
        text("SELECT name, motdepass FROM client WHERE name = :name"),
        {"name": name}
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="WRONG NAME OR PASSWORD")

    # Verify password using verify_password function
    if verify_password(password, user.motdepass):
        return {"message": f"SUCCESSFUL LOG IN WELCOME {name}"}
    else:
        raise HTTPException(status_code=401, detail="WRONG NAME OR PASSWORD")



# FIXED #1: Get user info from dashboard
@app.get("/dashboard")
def get_user_info(name: str, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT age FROM client WHERE name = :name"),
        {"name": name}
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")
    
    return {"age": result.age}  




@app.get("/displayproduct")
def display_product(db: Session = Depends(get_db)):
    products = db.execute(
        text("SELECT name, quentity FROM product WHERE quentity > 0")
    ).all()  
    
    return [
        {
            "name": p.name,
            "quentity": p.quentity
        }
        for p in products
    ]



#we already know that the product exists (the user selects one from its shown list)
@app.put("/buyproduct")
def buy_product(name: str, qt: int, db: Session = Depends(get_db)):
    if qt <= 0:
        raise HTTPException(status_code=400, detail="ENTER A VALID QUANTITY")
    
   
    qtt = db.execute(
        text("SELECT quentity FROM product WHERE name = :name"),
        {"name": name}
    ).first()
    
   
    qt1 = qtt.quentity
    
    if qt1 < qt:
        raise HTTPException(status_code=400, detail="ENTER LESS QUANTITY")
    
    qt1 = qt1 - qt
    
    db.execute(
        text("UPDATE product SET quentity = :new_qt WHERE name = :name"),
        {"new_qt": qt1, "name": name}
    )
    db.commit()
    
    return {"message": "buying done successfully"}
#do the front end girl , the we pass to the  JWT and lkhorti lakhor.