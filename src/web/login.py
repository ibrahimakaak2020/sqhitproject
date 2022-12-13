from fastapi import FastAPI, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from db.models.models import User
from sqlalchemy.orm import Session
from db.database.database import get_db
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
from api.route_login import login_for_access_token
from db.schemas.schemas import UserShow
from web.loginform import LoginForm
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
loginroot = APIRouter()
templates = Jinja2Templates(directory="templates")


@loginroot.get("/login")
def login(request: Request):

    return templates.TemplateResponse("login.html", {"request": request,"user":None})


@loginroot.post("/login")
async def login(request: Request,db: Session = Depends(get_db)):
    form = LoginForm(request)

    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            # response = templates.TemplateResponse("index.html", {"request": request})
            response = RedirectResponse('/', status_code=status.HTTP_302_FOUND)

            login_for_access_token(response=response, form_data=form, db=db)

            # return RedirectResponse('/', status_code=303)
            
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__,{"user":None})


@loginroot.get("/logout")
async def logout(request: Request):
    try:
        response =  response = RedirectResponse('/', status_code=status.HTTP_302_FOUND)
        response.delete_cookie("access_token")
        return response
    except Exception:
        return templates.TemplateResponse("login.html", {"request": request})
