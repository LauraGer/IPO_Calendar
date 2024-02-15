from sqlalchemy.orm import Session
from dba.models_app import WatchlistUser
from .schemas_app import UserCreate
import bcrypt

def create_user(db: Session, user: WatchlistUser):
    hashed_password = hash_password(user.password)
    db_user = WatchlistUser(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(WatchlistUser).filter(WatchlistUser.email == email).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')