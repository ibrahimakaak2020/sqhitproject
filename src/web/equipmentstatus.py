import datetime
from fastapi import FastAPI, Form, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from db.models.models import Equipment, EquipmentActivity, EquipmentRegister, User
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
from web.actionstake import actions
equipmentstatusroot = APIRouter()
templates = Jinja2Templates(directory="templates")


@equipmentstatusroot.get("/equipmentincompany")
def equipmentincompany(request: Request,db: Session=Depends(get_db),sn:str=None):
    eqincompany=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"next_activity":"T","date_of_recievefrom":None,"place_of_maintaince":"S"}).all()
 
    
    token = request.cookies.get("access_token")
   


    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        register_by=current_user.staffno


        return templates.TemplateResponse("activityequipmentshownew.html", {"request": request,"register_by":register_by ,"equipmentactivities":eqincompany,"activityaction":actions,"user":current_user})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e

@equipmentstatusroot.get("/equipmentwaitingforsend")
def equipmentwaitingforsend(request: Request,db: Session=Depends(get_db),sn:str=None):
    eqincompany=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"next_activity":"T","activity_status":"WFS","place_of_maintaince":"L"}).all()
 
    
        
    
    
    
    token = request.cookies.get("access_token")
   


    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        return templates.TemplateResponse("activityequipmentshownew.html", {"request": request ,"equipmentactivities":eqincompany,"activityaction":actions,"user":current_user})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e


@equipmentstatusroot.get("/equipmentinlocal")
def equipmentinlocal(request: Request,db: Session=Depends(get_db),sn:str=None):
    eqincompany=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"next_activity":"T","activity_status":"UPL","place_of_maintaince":"L"}).all()
 
    
        
    
    token = request.cookies.get("access_token")
   


    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        register_by=current_user.staffno
        return templates.TemplateResponse("equipmentinlocal.html", {"request": request,"register_by":register_by ,"equipmentactivities":eqincompany,"activityaction":actions,"user":current_user})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e



@equipmentstatusroot.get("/equipmentwaitingforreturn")
def equipmentwaitingforreturn(request: Request,db: Session=Depends(get_db),sn:str=None):
    eqincompany=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"next_activity":"T","activity_status":"WFR","place_of_maintaince":"L"}).all()
 
    
      
    token = request.cookies.get("access_token")
   


    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        register_by=current_user.staffno
        return templates.TemplateResponse("activityequipmentshownew.html", {"request": request,"register_by":register_by ,"equipmentactivities":eqincompany,"activityaction":actions,"user":current_user})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e


@equipmentstatusroot.get("/equipmentwaitingfordecision")
async def equipmentwaitingfordecision(request: Request,db: Session = Depends(get_db),sn:str=None):
    eqincompany=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"next_activity":"T","activity_status":"WFD","place_of_maintaince":"L"}).all()
 
    
    token = request.cookies.get("access_token")
   


    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        register_by=current_user.staffno


        return templates.TemplateResponse("activityequipmentshownew.html", {"request": request,"register_by":register_by ,"equipmentactivities":eqincompany,"activityaction":actions,"user":current_user})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e













@equipmentstatusroot.post("/takeactionone")
def takeactionone(request: Request,sn: str = Form()):
 
    sn=sn
    print(sn)

    return RedirectResponse('/?msg=' + "Equipment Registered"+'&sn='+sn, status_code=status.HTTP_302_FOUND)
            
