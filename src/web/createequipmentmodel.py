from tkinter import E
from fastapi import FastAPI, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from db.models.models import Equipment, Equipment_Model, Equipment_Type, EquipmentRegister, Location, Manufacture, User
from sqlalchemy.orm import Session
from db.database.database import get_db
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
# from api.route_login import login_for_access_token
from db.datacreator import CreateModelData, QueryModelData
from db.schemas.schemas import EquipmentCreate, EquipmentModelCreate, UserShow, EquipmentRegisterCreate

from web.createequipmentform import CreateEquipmentForm
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from web.createequipmentmodelform import CreateEquipmentModelForm
createequipmenmodeltroot = APIRouter()
templates = Jinja2Templates(directory="templates")

@createequipmenmodeltroot.get("/equipmentmodel")
def createequipmentmodel(request: Request,db: Session=Depends(get_db),msg:str=None,sn:str=None):
    print("from equipment model ......")
   
    manuf=QueryModelData(modeltable=Manufacture,db=db).all()
    equipmenttype=QueryModelData(modeltable=Equipment_Type,db=db).all()
    print(equipmenttype)
    token = request.cookies.get("access_token")

    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        
        return templates.TemplateResponse("registerequipmentmodel.html", {"request": request,"manuf":manuf,"equipmnettype":equipmenttype,"user":current_user})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e




@createequipmenmodeltroot.post("/equipmentmodel")
async def createequipmentmodel(request: Request,db: Session=Depends(get_db),msg:str=None,sn:str=None):
    form=CreateEquipmentModelForm(request)
    print("from equipment model ......")

    
    token = request.cookies.get("access_token")
    await form.load_data()
    manuf=QueryModelData(modeltable=Manufacture,db=db).all()
    equipmenttype=QueryModelData(modeltable=Equipment_Type,db=db).all()
    
    if await form.is_valid():
        try:

            equipmentmodel=EquipmentModelCreate(**form.__dict__)
    
            
            print(equipmenttype)

            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            print(param, "param")
            current_user: User = get_current_user_from_token(token=param, db=db)
            CreateModelData(modeltable=Equipment_Model,db=db, modelcreate=equipmentmodel)
            
            return templates.TemplateResponse("registerequipmentmodel.html", {"request": request,"manuf":manuf,"equipmnettype":equipmenttype,"user":current_user,"msg":"Model Register Succusfull"})
        except Exception as e:
            print(f'{e}')
            raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e
    return templates.TemplateResponse("registerequipmentmodel.html", form.__dict__)

