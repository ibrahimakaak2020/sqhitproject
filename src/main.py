from fastapi import Depends, FastAPI, HTTPException, status,Request

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db.schemas.schemas import UserCreate
from core.hashing import Hasher

from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def fake_decode_token():
    return UserCreate(
        staffno=11111,staffname="fakedecoded",password=Hasher.get_password_hash("ibrahim")
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token()
    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_decode_token() if str(fake_decode_token().staffno)==form_data.username else None
    print(form_data.username)
    print(user_dict)
    print(fake_decode_token().staffno)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_dict.staffname, "token_type": "bearer"}
@app.get("/login")
async def login(request :Request):

    return templates.TemplateResponse("login.html", {"request": request})




@app.get("/users/me")
async def read_users_me(current_user: UserCreate = Depends(get_current_user)):
    return current_user


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}



