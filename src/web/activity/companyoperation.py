import datetime
from multiprocessing.connection import wait
from tkinter import E
from fastapi import FastAPI, status, HTTPException, Depends
# from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, Response
from db.models.models import Company_User, Equipment, Equipment_Model, EquipmentActivity, EquipmentRegister, Location, User
from sqlalchemy.orm import Session
from db.database.database import get_db
from fastapi.security.utils import get_authorization_scheme_param
from api.route_login import get_current_user_from_token
# from api.route_login import login_for_access_token
from db.datacreator import CreateModelData, QueryModelData, UpdateModelData
from db.schemas.schemas import EquipmentActivityCreate, EquipmentCreate, UserShow, EquipmentRegisterCreate,repairedcompanyupdate,repairedupdate
from web.activity.locallyform import LocallyForm


from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from web.activity.repairedcompanyform import CreateRepairedCompanyUpdateForm
from web.activity.repaireupdate import CreateRepairedUpdateForm
from web.activity.senttocompanyform import SendToCompanyForm
from web.activity.waitingform import WaitingForm


activityroot = APIRouter()
templates = Jinja2Templates(directory="templates")



@activityroot.get("/finalaction")
async def register(request: Request,db: Session=Depends(get_db),msg:str=None,sn:str=None,status:str=None):
     if status =="RR" :
        return templates.TemplateResponse("activity/repaired.html",{"request": request,"msg":"Equipment Sent to Comapny Sucussfully"})
    


@activityroot.post("/finalaction")
async def register(request: Request,db: Session=Depends(get_db),msg:str=None,sn:str=None,status:str=None):
        if status =="RR":
            form=CreateRepairedUpdateForm(request)
        else:
            form=CreateRepairedCompanyUpdateForm(request)


        await form.load_data()
        
        sn=sn
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
            token)  # scheme will hold "Bearer" and param will hold actual token value
            print(param, "param")
            current_user: User = get_current_user_from_token(token=param, db=db)
            userid=current_user.staffno
            registerid=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":sn,"register_status":"Y"}).first()
            activityid=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"registerid":registerid.registerid,"maintaince_status":None,"next_activity":"T"}).first()
            returnbacke=returnbackrepairedcreate(**form.__dict__,recieve_by=userid,recieve_date=datetime.datetime.now(),next_activity="F",maintaince_status="RR")
            UpdateModelData(modeltable=EquipmentActivity,col_id=activityid.activityid,db=db, updatecols=returnbacke)
            return RedirectResponse('/'+'?sn='+sn, status_code=303)
            
            
            # return RedirectResponse('/' + '?msg=' + "Equipment Registered  ", status_code=status.HTTP_302_FOUND)
            # return templates.TemplateResponse("sendtocompany.html",{"request": request,"company_user":company_user,"msg":"Equipment Sent to Comapny Sucussfully"})
        except HTTPException:
            form.__dict__.update(msg="Optional[str] = None")
            form.__dict__.get("errors").append("Equipment Already Sended to Comapany")
            return templates.TemplateResponse("sendtocompany.html", form.__dict__,{"request": request,"company_user":company_user,"errors":form.__dict__['errors'],"sn":form.__dict__['sn']})
    # return templates.TemplateResponse("sendtocompany.html",{"request": request,"company_user":company_user, "errors":form.__dict__['errors'],"sn":form.__dict__['sn']})



@activityroot.post("/sendtocompany")
async def register(request: Request,db: Session = Depends(get_db)):
  
    company_user=QueryModelData(modeltable=Company_User,db=db).all()
       
    form = SendToCompanyForm(request)
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
    print(param, "param")
    current_user: User = get_current_user_from_token(token=param, db=db)
    userid=current_user.staffno
    await form.load_data()
    registerid=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":sn,"register_status":"Y"}).first()
           
    
    if await form.is_valid(registerid=registerid,db=db):
        try:
            
           

            # CreateModelData(modeltable=EquipmentRegister,db=db, modelcreate=equipmentregister)
            equipmentregister=EquipmentActivityCreate(**form.__dict__,create_by=userid,registerid=registerid.registerid,activity_status="UPS",activity_date=datetime.datetime.now(),date_of_send=datetime.datetime.now(),place_of_maintaince="S",next_activity="T")
            
            print("check ibrahim",equipmentregister)
            CreateModelData(modeltable=EquipmentActivity,db=db, modelcreate=equipmentregister)
            return RedirectResponse('/'+'?sn='+form.sn, status_code=303)
            
            
            # return RedirectResponse('/' + '?msg=' + "Equipment Registered  ", status_code=status.HTTP_302_FOUND)
            # return templates.TemplateResponse("sendtocompany.html",{"request": request,"company_user":company_user,"msg":"Equipment Sent to Comapny Sucussfully"})
        except HTTPException:
            form.__dict__.update(msg="Optional[str] = None")
            form.__dict__.get("errors").append("Equipment Already Sended to Comapany")
            return templates.TemplateResponse("sendtocompany.html", form.__dict__,{"request": request,"company_user":company_user,"errors":form.__dict__['errors'],"sn":form.__dict__['sn']})
    return templates.TemplateResponse("sendtocompany.html",{"request": request,"company_user":company_user, "errors":form.__dict__['errors'],"sn":form.__dict__['sn']})


# local maintenance

@activityroot.post("/locally")
async def locally(request: Request,db: Session = Depends(get_db),sn:str=None):
   
    form = LocallyForm(request)
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
    print(param, "param")
    current_user: User = get_current_user_from_token(token=param, db=db)
    userid=current_user.staffno
    
    await form.load_data()
    sn=form.__dict__['sn']
    
    registerid=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":sn,"register_status":"Y"}).first()
           
    
    if await form.is_valid(registerid=registerid.registerid ,db=db):
        try:
                 

            # CreateModelData(modeltable=EquipmentRegister,db=db, modelcreate=equipmentregister)
            equipmentregister=EquipmentActivityCreate(**form.__dict__,create_by=userid,registerid=registerid.registerid,activity_status="UPL",activity_date=datetime.datetime.now(),place_of_maintaince="L",next_activity='T')
            
            print("check ibrahim",equipmentregister)
            CreateModelData(modeltable=EquipmentActivity,db=db, modelcreate=equipmentregister)
            return RedirectResponse('/'+'?sn='+sn, status_code=303)
            
            
            # # return RedirectResponse('/' + '?msg=' + "Equipment Registered  ", status_code=status.HTTP_302_FOUND)
            # return templates.TemplateResponse("sendtocompany.html",{"request": request,"sn":sn,"msg":"Equipment Under Process Locally "})
        except HTTPException:
            form.__dict__.update(msg="Optional[str] = None")
            form.__dict__.get("errors").append("Equipment Already Sended to Comapany")
            return templates.TemplateResponse("sendtocompany.html", form.__dict__,{"request": request,"errors":form.__dict__['errors'],"sn":form.__dict__['sn']})
    return templates.TemplateResponse("sendtocompany.html",{"request": request, "errors":form.__dict__['errors'],"sn":form.__dict__['sn']})


# send equipment to company

@activityroot.post("/sentequipmenttoecompany")
async def sendequipmenttoecompany(request: Request,db: Session = Depends(get_db),sn:str=None):
   
    form = SendToCompanyForm(request)
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
    print(param, "param")
    current_user: User = get_current_user_from_token(token=param, db=db)
    userid=current_user.staffno
    
    await form.load_data()
    sn=form.__dict__['sn']
    
    registerid=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":sn,"register_status":"Y"}).first()
           
    
    if await form.is_valid(registerid=registerid.registerid ,db=db):
        try:
                 

            # CreateModelData(modeltable=EquipmentRegister,db=db, modelcreate=equipmentregister)
            equipmentregister=EquipmentActivityCreate(**form.__dict__,create_by=userid,registerid=registerid.registerid,activity_status="UPS",activity_date=datetime.datetime.now(),place_of_maintaince="S",next_activity='T')
            
            print("check ibrahim",equipmentregister)
            CreateModelData(modeltable=EquipmentActivity,db=db, modelcreate=equipmentregister)
            return RedirectResponse('/'+'?sn='+sn, status_code=303)
            
            
            # # return RedirectResponse('/' + '?msg=' + "Equipment Registered  ", status_code=status.HTTP_302_FOUND)
            # return templates.TemplateResponse("sendtocompany.html",{"request": request,"sn":sn,"msg":"Equipment Under Process Locally "})
        except HTTPException:
            form.__dict__.update(msg="Optional[str] = None")
            form.__dict__.get("errors").append("Equipment Already Sended to Comapany")
            return templates.TemplateResponse("sendtocompany.html", form.__dict__,{"request": request,"errors":form.__dict__['errors'],"sn":form.__dict__['sn']})
    return templates.TemplateResponse("sendtocompany.html",{"request": request, "errors":form.__dict__['errors'],"sn":form.__dict__['sn']})

# keep in waiting list

@activityroot.post("/waiting")
async def waiting(request: Request,db: Session = Depends(get_db),sn:str=None):
   
    form = WaitingForm(request)
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
    print(param, "param")
    current_user: User = get_current_user_from_token(token=param, db=db)
    userid=current_user.staffno
    
    await form.load_data()
    sn=form.__dict__['sn']
    
    registerid=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":sn,"register_status":"Y"}).first()
           
    
    if await form.is_valid(registerid=registerid.registerid ,db=db):
        try:
                 

            # CreateModelData(modeltable=EquipmentRegister,db=db, modelcreate=equipmentregister)
            equipmentregister=EquipmentActivityCreate(**form.__dict__,create_by=userid,registerid=registerid.registerid,activity_status="WFS",activity_date=datetime.datetime.now(),place_of_maintaince="L",next_activity='T')
            
            print("check ibrahim",equipmentregister)
            CreateModelData(modeltable=EquipmentActivity,db=db, modelcreate=equipmentregister)
            return RedirectResponse('/'+'?sn='+sn, status_code=303)
            
            
            # # return RedirectResponse('/' + '?msg=' + "Equipment Registered  ", status_code=status.HTTP_302_FOUND)
            # return templates.TemplateResponse("sendtocompany.html",{"request": request,"sn":sn,"msg":"Equipment Under Process Locally "})
        except HTTPException:
            form.__dict__.update(msg="Optional[str] = None")
            form.__dict__.get("errors").append("Equipment Already Sended to Comapany")
            return templates.TemplateResponse("sendtocompany.html", form.__dict__,{"request": request,"errors":form.__dict__['errors'],"sn":form.__dict__['sn']})
    return templates.TemplateResponse("sendtocompany.html",{"request": request, "errors":form.__dict__['errors'],"sn":form.__dict__['sn']})

