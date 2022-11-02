import datetime
from fastapi import FastAPI, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from db.models.models import Equipment, EquipmentRegister, User
from sqlalchemy.orm import Session
from db.database.database import get_db
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
# from api.route_login import login_for_access_token
from db.datacreator import CreateModelData, QueryModelData
from db.schemas.schemas import UserShow, EquipmentRegisterCreate

from web.registerequipmentform import RegisterForm
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
registerroot = APIRouter()
templates = Jinja2Templates(directory="templates")


@registerroot.get("/registerequipment")
def registerequipment(request: Request,db: Session=Depends(get_db),sn:str=None):
    if sn:
        equipment=QueryModelData(modeltable=Equipment,db=db ,cols={"sn":sn}).all()[0]
    else:
         equipment=None    
    
    token = request.cookies.get("access_token")
   


    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        register_by=current_user.staffno
        return templates.TemplateResponse("registerequipment.html", {"request": request,"register_by":register_by,"equipment":equipment})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e



@registerroot.post("/registerequipment")
async def registerequipment(request: Request,db: Session = Depends(get_db),sn:str=None):
    form = RegisterForm(request)
    

    await form.load_data()
    sn=form.__dict__['sn']
    if await form.is_valid():
        try:
            equipmentregct=EquipmentRegisterCreate(**form.__dict__)
            equipmentregct.date_of_register =datetime.datetime.now()


            CreateModelData(modeltable=EquipmentRegister,db=db, modelcreate=equipmentregct)
            # return RedirectResponse('/', status_code=303)

            return RedirectResponse('/' + '?msg=' + "Equipment Registered"+'&sn='+sn, status_code=status.HTTP_302_FOUND)

        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("registerequipment.html", form.__dict__)
    return templates.TemplateResponse("registerequipment.html", form.__dict__)

