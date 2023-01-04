from tkinter import E
from fastapi import FastAPI, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from db.models.models import Equipment, Equipment_Model, EquipmentRegister, Location, User
from sqlalchemy.orm import Session
from db.database.database import get_db
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
# from api.route_login import login_for_access_token
from db.datacreator import CreateModelData, QueryModelData
from db.schemas.schemas import EquipmentCreate, UserShow, EquipmentRegisterCreate

from web.createequipmentform import CreateEquipmentForm
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
createequipmentroot = APIRouter()
templates = Jinja2Templates(directory="templates")

@createequipmentroot.get("/equipment")
def equipment(request: Request,db: Session=Depends(get_db),msg:str=None,sn:str=None):
   
    # locations=QueryModelData(modeltable=Location,db=db).all()
    # equipmentmodels=QueryModelData(modeltable=Equipment_Model,db=db).all()
    token = request.cookies.get("access_token")

    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        
        return templates.TemplateResponse("equipmentregister.html", {"request": request})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e




@createequipmentroot.post("/equipment")
def createequipment(request: Request,db: Session=Depends(get_db),msg:str=None,sn:str=None):
   
    locations=QueryModelData(modeltable=Location,db=db).all()
    equipmentmodels=QueryModelData(modeltable=Equipment_Model,db=db).all()
    token = request.cookies.get("access_token")

    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        register_by=current_user.staffno
        return templates.TemplateResponse("createequipment.html", {"request": request,"register_by":register_by,"locations":locations,"equipmnetmodel":equipmentmodels})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e



@createequipmentroot.get("/createequipment")
async def createequipment(request: Request,db: Session = Depends(get_db)):
    locations=QueryModelData(modeltable=Location,db=db).all()
    equipmentmodels=QueryModelData(modeltable=Equipment_Model,db=db).all()
    form = CreateEquipmentForm(request)

    await form.load_data()
    if await form.is_valid(db=db):
        try:
            equipmentregct=EquipmentCreate(**form.__dict__)
            CreateModelData(modeltable=Equipment,db=db, modelcreate=equipmentregct)
            # return RedirectResponse('/', status_code=303)
            
            
            # return RedirectResponse('/' + '?msg=' + "Equipment Registered  ", status_code=status.HTTP_302_FOUND)
            return templates.TemplateResponse("createequipment.html",{"request": request,"locations":locations,"equipmnetmodel":equipmentmodels,"msg":"succusd sdfs fs  sdfasfs"})
        except HTTPException:
            form.__dict__.update(msg="Optional[str] = None")
            form.__dict__.get("errors").append("Equipment Already in Registered")
            return templates.TemplateResponse("createequipment.html", form.__dict__,{"request": request,"locations":locations,"equipmnetmodel":equipmentmodels,"errors":form.__dict__['errors']})
    return templates.TemplateResponse("createequipment.html",{"request": request,"locations":locations,"equipmnetmodel":equipmentmodels, "errors":form.__dict__['errors']})


@createequipmentroot.post("/createequipmentmain")
async def createequipmentmain(request: Request,db: Session = Depends(get_db),sn:str=None):
    locations=QueryModelData(modeltable=Location,db=db).all()
    equipmentmodels=QueryModelData(modeltable=Equipment_Model,db=db).all()
    form = CreateEquipmentForm(request)
    
    print("request",request.__dict__)

    await form.load_data()
    sn=form.__dict__['sn']
    print("check ibrahim  sn",sn)

    if await form.is_valid(db=db):
        try:
            equipmentregct=EquipmentCreate(**form.__dict__)
            
            CreateModelData(modeltable=Equipment,db=db, modelcreate=equipmentregct)
            #return RedirectResponse('/', status_code=303)
            
            
            
            return RedirectResponse('/' + '?sn=' +sn, status_code=status.HTTP_302_FOUND)
            # return templates.TemplateResponse("createequipment.html",{"request": request,"locations":locations,"equipmnetmodel":equipmentmodels,"msg":"succusd sdfs fs  sdfasfs"})
        except HTTPException:
            form.__dict__.update(msg="Optional[str] = None")
            form.__dict__.get("errors").append("Equipment Already in Registered")
            return templates.TemplateResponse("index.html", form.__dict__,{"request": request,"locations":locations,"equipmnetmodel":equipmentmodels,"errors":form.__dict__['errors']})
    return templates.TemplateResponse("index.html",{"request": request,"locations":locations,"equipmnetmodel":equipmentmodels, "errors":form.__dict__['errors']})





