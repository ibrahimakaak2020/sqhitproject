from fastapi import FastAPI, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from db.models.models import User
from sqlalchemy.orm import Session
from db.database.database import get_db
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
from api.route_login import login_for_access_token
from db.schemas.schemas import UserShow,UserCreate
from web.loginform import LoginForm
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from db.datacreator import CreateModelData

from web.signup.signupform import SignupForm
signuproot = APIRouter()
templates = Jinja2Templates(directory="templates")


@signuproot.get("/signup")
def signup(request: Request):

    return templates.TemplateResponse("signup.html", {"request": request,"user":None})


@signuproot.post("/signup")
async def signup(request: Request,db: Session = Depends(get_db)):
    form = SignupForm(request)

    await form.load_data()
    if await form.is_valid(db=db,username=form.staffno):
        try:
            userdata=UserCreate(**form.__dict__)
            print(form.password)
           
           
            # response = templates.TemplateResponse("index.html", {"request": request})
            user=CreateModelData(modeltable=User,db=db,modelcreate=userdata)
            response = RedirectResponse('/', status_code=status.HTTP_302_FOUND)
            
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect username or Password")
            return templates.TemplateResponse("signup.html", form.__dict__)
    return templates.TemplateResponse("signup.html", form.__dict__)


