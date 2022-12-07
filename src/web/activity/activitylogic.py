import datetime
from multiprocessing.connection import wait
from tkinter import E
from fastapi import FastAPI, Form, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from db.models.models import Company_User, Equipment, Equipment_Model, EquipmentActivity, EquipmentRegister, Location, User
from sqlalchemy.orm import Session
from db.database.database import get_db
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
# from api.route_login import login_for_access_token
from db.datacreator import CreateModelData, QueryModelData, UpdateModelData, update_table
from db.schemas.schemas import EquipmentActivityCreate, EquipmentCreate, UserShow, EquipmentRegisterCreate, updateactivity, updateactivitycompany
from web.activity.activityform import UpdateActivityForm
from web.activity.locallyform import LocallyForm

from db.models import models
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from web.activity.repairedcompanyform import CreateRepairedCompanyUpdateForm
from web.activity.repaireupdate import CreateRepairedUpdateForm
from web.activity.senttocompanyform import SendToCompanyForm
from web.activity.waitingform import WaitingForm


activityroot = APIRouter()
templates = Jinja2Templates(directory="templates")



# local maintenance

@activityroot.post("/activitycrud")
async def activitycrud(request: Request,db: Session = Depends(get_db),sn:str=None,activity:EquipmentActivity=None):

    if activity:
        token = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(token) 
        print(param, "param")
        current_user: User = get_current_user_from_token(token=param, db=db)
        userid=current_user.staffno
        updateactivity=None
        createactivity=None

        if activity.activity_status=="UPL":
            updateactivity=
        
        elif activity.activity_status=="UPS":
            pass
        elif activity.activity_status=="WFD":
            pass
        elif activity.activity_status=="WFR":
            pass
        elif activity.activity_status=="WFS":
            pass
   
           