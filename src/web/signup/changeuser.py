from fastapi import FastAPI, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse
from core.hashing import Hasher
from db.models.models import User
from sqlalchemy.orm import Session
from db.database.database import get_db
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
from api.route_login import login_for_access_token
from db.schemas.schemas import UserShow,UserCreate
from web.loginform import LoginForm
from fastapi.templating import Jinja2Templates

from db.datacreator import CreateModelData, update_table

from web.signup.changeuserform import ChangeUserForm
changepasswordproot = APIRouter()
templates = Jinja2Templates(directory="templates")


@changepasswordproot.get("/changepassword")
def changepassword(request: Request,errors:None,db: Session = Depends(get_db),staffno=None):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            
    current_user: User = get_current_user_from_token(token=param, db=db)

    return RedirectResponse("http://localhost:8000/#changepassword", {"request":request,"user":current_user,"errors":form.__dict__['errors']})


@changepasswordproot.post("/changepassword")
async def changepassword(request: Request,db: Session = Depends(get_db),staffno=None,error:str=None):
    form = ChangeUserForm(request)
    staffno=staffno
    print('-------------current staffno:',staffno)
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
       
   
    error="Please Enter Your Correct Current Password"
    headers = {'Location': '/#changepassword','error':error}
    

    await form.load_data()
    current_user: User = get_current_user_from_token(token=param, db=db)
    if await form.is_valid(db=db,staffno=staffno):
        try:
           
            
            user=update_table(modeltable=User,db=db, col_id={"staffno":staffno}, updatecols={"password":Hasher.get_password_hash(form.__dict__['newpassword'])})
            return RedirectResponse('/', status_code=status.HTTP_302_FOUND)
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Please Enter Your Correct Current Password")
            return  Response(data=error, headers=headers, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

    return  Response(content=error, headers=headers, status_code=status.HTTP_307_TEMPORARY_REDIRECT)



