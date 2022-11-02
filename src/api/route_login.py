from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends,APIRouter,Response
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import status,HTTPException
from jose import JWTError, jwt
from db.database.database import get_db
from core.hashing import Hasher
from db.schemas.schemas import Token
from db.models.models import User
from db.datacreator import QueryModelData,get_user
from core.security import create_access_token
from core.config import settings


router = APIRouter()

def authenticate_user(username: str, password: str,db: Session):
    user =  get_user(username=username,db=db)
    print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user

@router.get('/me3')
async def me():

    return "sdfsadfsd"


@router.post("/token", response_model=Token)
def login_for_access_token(response:Response,form_data: OAuth2PasswordRequestForm = Depends(),db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.staffno)}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )


    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")  #new
print(oauth2_scheme ,"oauth2_scheme")

#new function, It works as a dependency
def get_current_user_from_token(token:Depends(oauth2_scheme),db: Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials ibrahim",
    )

    try:

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        print(payload,"from ibrahim test")
        username: str = payload.get("sub")
        print("username/email extracted is ",username)
        if username is None:
            raise credentials_exception
    except JWTError:
        print("JWTError")
        raise credentials_exception
    user = get_user(username=username,db=db)
    print(user,"from ibrahim" )
    if user is None:
        print(payload,"from ibrahim test")
        raise credentials_exception
    return user


#{
#  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzQ1LCJleHAiOjE2NjQzNDk4MTV9.w94h5xPjTrkZuj5p6A2OmZ6kDgSxs14m4EA-AWy2iXc",
#  "token_type": "bearer"
#}
