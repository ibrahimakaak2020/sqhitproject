from tkinter import N
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi import FastAPI, Request, Response,Form
from api.base import api_router
from db.models.models import Company_User, Equipment, Equipment_Model, EquipmentRegister, Location, User
from sqlalchemy.orm import Session
from db.database.database import get_db
from db.datacreator import QueryModelData,QueryModelDataActivity
from db.models.models import EquipmentActivity
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
from api.route_login import login_for_access_token
from db.schemas.schemas import UserShow
from web.loginform import LoginForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from web.login import loginroot
from web.signup.signup import signuproot 
from web.signup.changeuser import changepasswordproot 

from web.registerequipment import registerroot
from  web.createequipment import createequipmentroot
from web.equipmentstatus import equipmentstatusroot
from web.createequipmentmodel import createequipmenmodeltroot
from  web.activity.companyoperation import activityroot
from datetime import datetime
from web.actionstake import actions
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(api_router)
app.include_router(loginroot)
app.include_router(registerroot)
app.include_router(createequipmentroot)
app.include_router(activityroot)
app.include_router(signuproot)
app.include_router(equipmentstatusroot)
app.include_router(changepasswordproot)
app.include_router(createequipmenmodeltroot)


@app.get('/')
async def home(request: Request, db: Session=Depends(get_db),msg:str=None,search:str=None,sn:str=None,error:str=None):
    locations=QueryModelData(modeltable=Location,db=db).all()
    equipmentmodels=QueryModelData(modeltable=Equipment_Model,db=db).all()
    companyuser=QueryModelData(modeltable=Company_User,db=db).all()
   
    if search:
        sn=search or sn


    token = request.cookies.get("access_token")
    form = await request.form()
   
   
    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)

        print(f"Current user  from get:{current_user.staffname},{datetime.now()}")

        equipment=QueryModelData(modeltable=Equipment,db=db,cols={"sn":sn}).first()
        equipmentregister=None
        equipmentactivities=None
        equipmentactivitieshistory=None
        if equipment:
            if equipmentregister:=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":equipment.sn,"register_status":"Y"}).first():
                    
                    # equipmentactivities=QueryModelDataActivity(db=db,search=sn,col).all()
                    equipmentactivities=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"registerid":equipmentregister.registerid,"maintaince_status":None,"next_activity":"T","date_of_returnback":None}).first()
                    equipmentactivitieshistory=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"registerid":equipmentregister.registerid,"next_activity":"F"}).all()
                    print("check ibrahi activity",equipmentactivities)

        
        else:
           equipment=None
        print("check ibrahi activity",equipmentactivities)
        contents = {"request": request, "equipment": equipment, "equipmentregister": equipmentregister,
         "equipmentactivities": equipmentactivities, "search": sn, "locations": locations,
          "equipmnetmodel": equipmentmodels, "user": current_user,"companyuser":companyuser,
           "sn": sn,"activityaction":actions,"equipmentactivitieshistory":equipmentactivitieshistory,"error":error}


  # print(f"Current user :{current_user.staffname},{datetime.now()}")
        return templates.TemplateResponse("index.html", contents)
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e

@app.post('/')
async def home(request: Request, db: Session=Depends(get_db),msg:str=None,sn:str=None,error:str=None):
    locations=QueryModelData(modeltable=Location,db=db).all()
    equipmentmodels=QueryModelData(modeltable=Equipment_Model,db=db).all()
    companyuser=QueryModelData(modeltable=Company_User,db=db).all()
   

    token = request.cookies.get("access_token")
    form = await request.form()
    search=form.get("search")
    print(f"search: {search}")
    if search:
        sn = search or sn
    print("cookies  ibrah:", token)
    try:

        scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)

        print(f"Current user  from post:{current_user.staffname},{datetime.now()}")
        
        equipment=QueryModelData(modeltable=Equipment,db=db,cols={"sn":sn}).first()
        equipmentregister=None
        equipmentactivities=None
        equipmentactivitieshistory=None
        if equipment:
            if equipmentregister:=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":equipment.sn,"register_status":"Y"}).first():
                    # equipmentactivities=QueryModelDataActivity(db=db,search=sn).all()
                    equipmentactivities=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"registerid":equipmentregister.registerid,"maintaince_status":None,"next_activity":"T","date_of_returnback":None}).first()
                    equipmentactivitieshistory=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"registerid":equipmentregister.registerid,"next_activity":"F"}).all()
        else:
            equipment=None
                
        print("check ibrahi activity",equipmentactivities)
        contents={"request": request, "user": current_user,"equipment":equipment
                 ,"equipmentregister":equipmentregister,"companyuser":companyuser,
                "equipmentactivities":equipmentactivities,"search":search,"sn":sn
                ,"locations":locations,"equipmnetmodel":equipmentmodels,"activityaction":actions,"equipmentactivitieshistory":equipmentactivitieshistory ,"error":error}

        return templates.TemplateResponse("index.html",contents )
    except Exception as e:
        print(f'{e}')
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e
