from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.routers import tasks
from fastapi import FastAPI
from app.routers import users
from .security import create_access_token
from app.security import get_current_user






# ابتدا نمونه app را بساز
app = FastAPI(title="NexusTask API", version="1.0.0")

# سپس روتورها را اضافه کن
app.include_router(users.router)


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="NexusTask API", version="1.0.0", lifespan=lifespan)

# ثبت روتر تسک‌ها
app.include_router(tasks.router)


@app.get("/")
def read_root():
    return {"message": "خوش آمدید به پروژه نکسوس‌تسک!"}
from fastapi import FastAPI
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexusTask API")


@app.get("/")
def root():
  return {"message": "خوش آمدید به پروژه NexusTask"}
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.security import create_access_token

app = FastAPI()


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
  if form_data.username != "shahab" or form_data.password != "TOKEN_PLACEHOLDER":
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="نام کاربری یا رمز عبور اشتباه است",
        headers={"WWW-Authenticate": "Bearer"},
    )

  access_token = create_access_token(data={"sub": form_data.username})
  return {"access_token": access_token, "token_type": "bearer"}
@app.get("/users/me")
async def read_users_me(current_user: str = Depends(get_current_user)):
  return {"username": current_user}
