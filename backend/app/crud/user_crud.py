from datetime import datetime
from http.cookiejar import user_domain_match

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from ..auth import hash_password, verify_password
from ..config import SECRET_KEY, ALGORITHM
from ..db.session import get_db
from ..models.user import User
from ..schemas.token_schemas import TokenData
from ..schemas.user_schemas import UserCreate, UserUpdate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_user(db: Session, user_data: UserCreate):
    hashed_password = hash_password(user_data.password)
    db_user = User(
        username=user_data.username,
        email=str(user_data.email),
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, user_username: str):
    return db.query(User).filter(User.username == user_username).first()


def get_user_by_email(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()


def get_all_users(db: Session, skip: int = 0, limit=10):
    return db.query(User).offset(skip).limit(limit).all()


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db=db, user_username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False

    for key, value in user_data.model_dump(exclude_unset=True).items():
        if key == "password":
            setattr(db_user, "password_hash", hash_password(value))
        else:
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def user_streak_management(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    today = datetime.today().date()

    if db_user.current_streak is None or db_user.last_activity_date is None or db_user.longest_streak is None:
        db_user.current_streak = 1
        db_user.longest_streak = 1
        db_user.last_activity_date = today
    else:
        if (today - db_user.last_activity_date).days == 1:
            db_user.current_streak += 1
            db_user.longest_streak += 1
            db_user.last_activity_date = today
            if db_user.current_streak > db_user.longest_streak:
                db_user.longest_streak = db_user.current_streak
        elif (today - db_user.last_activity_date).days > 1:
            db_user.current_streak = 1
            db_user.last_activity_date = today
        else:
            return {"message": "Streak already updated for today",
                    "current_streak": db_user.current_streak,
                    "longest_streak": db_user.longest_streak
                    }

    db.commit()
    db.refresh(db_user)
    return {"message": "Streak updated",
            "current_streak": db_user.current_streak,
            "longest_streak": db_user.longest_streak
            }
