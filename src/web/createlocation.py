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
from db.schemas.schemas import EquipmentCreate, EquipmentModelCreate, LocationCreate, UserShow, EquipmentRegisterCreate
from web.CreateLocationForm import CreateLocationForm

from web.createequipmentform import CreateEquipmentForm
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from web.createequipmentmodelform import CreateEquipmentModelForm
createlocationroot = APIRouter()
templates = Jinja2Templates(directory="templates")

@createlocationroot.get("/location")
def createlocation(request: Request,db: Session=Depends(get_db),msg:str=None,sn:str=None):
  
    token = request.cookies.get("access_token")

    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        
        return templates.TemplateResponse("registerlocation.html", {"request": request,"user":current_user})
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e




@createlocationroot.post("/location")
async def createlocation(request: Request,db: Session=Depends(get_db),msg:str=None,sn:str=None):
    form=CreateLocationForm(request)
   
    
    token = request.cookies.get("access_token")
    await form.load_data()

    scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            
    current_user: User = get_current_user_from_token(token=param, db=db)
    
    if await form.is_valid(db=db):
        try:

            locationr=LocationCreate(**form.__dict__)        
        
            CreateModelData(modeltable=Location,db=db, modelcreate=locationr)
            
            return templates.TemplateResponse("registerlocation.html", {"request": request,"user":current_user,"msg":"localtion Register Succusfull"})
        except Exception as e:
            print(f'{e}')
            raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e
    return templates.TemplateResponse("registerlocation.html",{"request":request,"errors": form.__dict__['errors'],"user":current_user})

