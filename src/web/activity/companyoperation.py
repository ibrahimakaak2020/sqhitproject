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
from db.schemas.schemas import EquipmentActivityCreate, EquipmentCreate, UserShow, EquipmentRegisterCreate, updateactivity, updateactivitycompany,updateactivitywaiting
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
    activityexist=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"registerid":registerid.registerid,"next_activity":"T"}).first()
    print("-------------------------------------activityexist",activityexist)
    
           
    
    if await form.is_valid(registerid=registerid.registerid ,db=db):
        try:
                 
            if activityexist:
                # CreateModelData(modeltable=EquipmentRegister,db=db, modelcreate=equipmentregister)
                equipmentregister=EquipmentActivityCreate(**form.__dict__,create_by=userid,registerid=registerid.registerid,activity_status="UPL",activity_date=datetime.datetime.now(),place_of_maintaince="L",next_activity='T')
                updatewaiting=updateactivitywaiting()
                print("check ibrahim",equipmentregister)

                update_table(modeltable=EquipmentActivity,col_id={"activityid":activityexist.activityid},updatecols=updatewaiting,db=db)
                print("done-----------------------")
                CreateModelData(modeltable=EquipmentActivity,db=db, modelcreate=equipmentregister)
                return RedirectResponse('/'+'?sn='+sn, status_code=303)
            else:

                # CreateModelData(modeltable=EquipmentRegister,db=db, modelcreate=equipmentregister)
                equipmentregister=EquipmentActivityCreate(**form.__dict__,create_by=userid,registerid=registerid.registerid,activity_status="UPL",activity_date=datetime.datetime.now(),place_of_maintaince="L",next_activity='T')
                
                print("check ibrahim",equipmentregister)
                CreateModelData(modeltable=EquipmentActivity,db=db, modelcreate=equipmentregister)
                print("----------------------------------------------------creaete",equipmentregister)
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
async def sendequipmenttoecompany(request: Request,db: Session = Depends(get_db),sn:str=None,activityid:int=None,registerid:int=None):
   
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
    registerid=None
    if registerid:
        registerid=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"registerid":registerid,"register_status":"Y"}).first()
    else:
        registerid=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":sn,"register_status":"Y"}).first()

    activityT=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"activityid":activityid,"next_activity":"T"}).first()
    if activityT:       
    
        if await form.is_valid(registerid=registerid.registerid ,db=db):
            try:
                    

                # CreateModelData(modeltable=EquipmentRegister,db=db, modelcreate=equipmentregister)
                equipmentregister=EquipmentActivityCreate(**form.__dict__,create_by=userid,registerid=registerid.registerid,activity_status="UPS",activity_date=datetime.datetime.now(),place_of_maintaince="S",next_activity='T')
                
                print("check ibrahim",equipmentregister)
    
                updatewaiting=updateactivitywaiting(date_of_maintaince=datetime.datetime.now())
               
                update_table(modeltable=EquipmentActivity,col_id={"activityid":activityT.activityid},updatecols=updatewaiting,db=db)

                CreateModelData(modeltable=EquipmentActivity,db=db, modelcreate=equipmentregister)
                return RedirectResponse('/'+'?sn='+sn, status_code=303)
                
                
                # # return RedirectResponse('/' + '?msg=' + "Equipment Registered  ", status_code=status.HTTP_302_FOUND)
                # return templates.TemplateResponse("sendtocompany.html",{"request": request,"sn":sn,"msg":"Equipment Under Process Locally "})
            except HTTPException:
                form.__dict__.update(msg="Optional[str] = None")
                form.__dict__.get("errors").append("Equipment Already Sended to Comapany")
                return templates.TemplateResponse("sendtocompany.html", form.__dict__,{"request": request,"errors":form.__dict__['errors'],"sn":form.__dict__['sn'],"user":current_user})
        return templates.TemplateResponse("sendtocompany.html",{"request": request, "errors":form.__dict__['errors'],"sn":form.__dict__['sn'],"user":current_user})
    else:
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
                return templates.TemplateResponse("sendtocompany.html", form.__dict__,{"request": request,"errors":form.__dict__['errors'],"sn":form.__dict__['sn'],"user":current_user})
        return templates.TemplateResponse("sendtocompany.html",{"request": request, "errors":form.__dict__['errors'],"sn":form.__dict__['sn'],"user":current_user})

# keep in waiting list

@activityroot.post("/returntodepartment")
async def waiting(request: Request,db: Session = Depends(get_db),activityid:int=None):
    
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
    print(param, "param")
    current_user: User = get_current_user_from_token(token=param, db=db)
    activity=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"activityid":activityid,"maintaince_status":None,"next_activity":"T","activity_status":"WFR","date_of_returnback":None}).first()
    
    try:
       
          
                # print(UpdateModelData(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols=sentactivity,db=db))
                update_table(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols={"next_activity":"F","date_of_returnback":datetime.datetime.now(),"recieve_by":current_user.staffno},db=db)
                print("-----------activity --------",activity.equipmen_register.sn)
                activityregister=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":activity.equipmen_register.sn,"register_status":"Y"}).first()
                print("-----------activityregister --------",activityregister)
                update_table(modeltable=EquipmentRegister,col_id={"sn":activityregister.sn},updatecols={"register_status":"N"},db=db)
                
                return RedirectResponse('/'+'?sn='+activity.equipmen_register.sn, status_code=303)
       
    
    except HTTPException:
            return templates.TemplateResponse("index.html",{"request": request})
    return templates.TemplateResponse("index.html",{"request": request})



@activityroot.post("/actionstatusnew")
async def actionstatusnew(request: Request,db: Session=Depends(get_db),activityid:int=None):
    form=UpdateActivityForm(request)
    activity=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"activityid":activityid,"maintaince_status":None,"next_activity":"T","date_of_returnback":None}).first()
    activitycreate=None
    print("----------------from actionstatusnew ------{}-----------------".format(activity.activityid))
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
    print(param, "param")
    current_user: User = get_current_user_from_token(token=param, db=db)
    await form.load_data(activity=activity)
    print('recieve_note ----------------',form.__dict__['recieve_note'])
    try:
       
          
        if activity.place_of_maintaince=="L":
            localactivity= updateactivity(recieve_by=current_user.staffno,**form.__dict__)
            print(dict(localactivity))
            # print(UpdateModelData(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols=localactivity,db=db))
            update_table(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols=localactivity,db=db)
            if localactivity.maintaince_status=="RR":
                activitycreate=EquipmentActivityCreate(registerid=activity.equipmen_register.registerid,activity_date=datetime.datetime.now(),create_by=current_user.staffno,activity_desc="Waiting for return back to Department",next_activity="T",place_of_maintaince="L",activity_status="WFR")
            else:
                activitycreate=EquipmentActivityCreate(registerid=activity.equipmen_register.registerid,activity_date=datetime.datetime.now(),create_by=current_user.staffno,activity_desc="Waiting for Taking Decision ",next_activity="T",place_of_maintaince="L",activity_status="WFD")
        else:
            sentactivity= updateactivitycompany(date_of_maintaince=datetime.datetime.now(),recieve_by=current_user.staffno,**form.__dict__)
            print(dict(sentactivity))
            # print(UpdateModelData(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols=sentactivity,db=db))
            update_table(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols=sentactivity,db=db)
                # activitycreate=EquipmentActivityCreate(registerid=activity.equipmen_register.registerid,create_by=current_user.staffno,activity_desc="Waiting for return back to Department",next_activity="T",place_of_maintaince="L",activity_status="WFR")
                # CreateModelData(modeltable=EquipmentActivity,db=db,modelcreate=activitycreate)
            if sentactivity.maintaince_status=="RR":
                activitycreate=EquipmentActivityCreate(activity_date=datetime.datetime.now(),registerid=activity.equipmen_register.registerid,create_by=current_user.staffno,activity_desc="Waiting for return back to Department",next_activity="T",place_of_maintaince="L",activity_status="WFR")
            else:
                activitycreate=EquipmentActivityCreate(activity_date=datetime.datetime.now(),registerid=activity.equipmen_register.registerid,create_by=current_user.staffno,activity_desc="Waiting for Taking Decision ",next_activity="T",place_of_maintaince="L",activity_status="WFD")
        CreateModelData(modeltable=EquipmentActivity,db=db,modelcreate=activitycreate)
        print("----------------------------------------------------creaete",activitycreate)
        return RedirectResponse('/'+'?sn='+activity.equipmen_register.sn, status_code=303)
    except HTTPException:
            return templates.TemplateResponse("index.html",{"request": request})
    return templates.TemplateResponse("index.html",{"request": request})





                            
@activityroot.get("/activityhistory")
async def activityhistory(request: Request,db: Session=Depends(get_db),sn:str=None):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
       
    
    Equipmentregisteryh=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":sn}).all()
    activityhistory=[]
    for register in Equipmentregisteryh:
     activity=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"registerid":register.registerid,"next_activity":"F"}).all()
     activityhistory.append(activity)
  
    try:

        current_user: User = get_current_user_from_token(token=param, db=db)
        return templates.TemplateResponse("/htmlmodels/activityhistory.html",{"request": request,"equipmentactivitieshistory":activityhistory,"Equipmentregisteryh":Equipmentregisteryh,"user":current_user})
       
    
    except Exception as e:
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e
    


        
@activityroot.post("/activityhistory")

async def activityhistory(request: Request,db: Session=Depends(get_db),sn:str=None):
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
       
    
    sn=sn
    Equipmentregisteryh=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":sn,"register_status":"N"}).all()
    print("--------------------------ibrahim--------------------",Equipmentregisteryh)
    activityhistory=[]
    for register in Equipmentregisteryh:
     activity=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"registerid":register.registerid,"next_activity":"F"}).all()
     if activity:
         activityhistory.append(activity)
     print(activity)
     print(register)
  
    try:
        current_user: User = get_current_user_from_token(token=param, db=db)
       
        return templates.TemplateResponse("/htmlmodels/activityhistory.html",{"request": request,"equipmentactivitieshistory":activityhistory,"Equipmentregisteryh":Equipmentregisteryh,"sn":sn,"user": current_user})
       
    
    except Exception as e:
       
        raise HTTPException(status_code=302, detail="Not authorized", headers={"Location": "/login"}) from e
    





@activityroot.post("/waitingfordecision")
async def waitingfordecision(request: Request,db: Session = Depends(get_db),activityid:int=None):
    
    token = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(
            token
        )  # scheme will hold "Bearer" and param will hold actual token value
    print(param, "param")
    
    activity=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"activityid":activityid,"maintaince_status":None,"next_activity":"T","activity_status":"WFR","date_of_returnback":None}).first()
    
    try:
       
                current_user: User = get_current_user_from_token(token=param, db=db)
                # print(UpdateModelData(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols=sentactivity,db=db))
                update_table(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols={"next_activity":"F","date_of_returnback":datetime.datetime.now(),"recieve_by":current_user.staffno},db=db)
                print("-----------activity --------",activity.equipmen_register.sn)
                activityregister=QueryModelData(modeltable=EquipmentRegister,db=db,cols={"sn":activity.equipmen_register.sn,"register_status":"Y"}).first()
                print("-----------activityregister --------",activityregister)
                update_table(modeltable=EquipmentRegister,col_id={"sn":activityregister.sn},updatecols={"register_status":"N"},db=db)
                
                return RedirectResponse('/'+'?sn='+activity.equipmen_register.sn, status_code=303)
       
    
    except HTTPException:
            return templates.TemplateResponse("index.html",{"request": request})
    return templates.TemplateResponse("index.html",{"request": request})



@activityroot.post("/waiting")
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


     
