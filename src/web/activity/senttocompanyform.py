from typing import List
from typing import Optional
from datetime import datetime

from fastapi import Depends, Request
from sqlalchemy import null
from api.route_login import get_current_user_from_token
from db.datacreator import QueryModelData
from db.database.database import get_db
from db.models.models import  Company_User, Equipment, EquipmentActivity, EquipmentRegister


class SendToCompanyForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.sn:str
        self.company_id:int=None
        self.activity_desc:str
        self.desc:str
        
       


    async def load_data(self):
        form = await self.request.form()
        self.sn = form.get('sn')
      
        self.company_id = form.get('cid')
        
         
        self.activity_desc = form.get('activity_desc')
         
        
        print("user ----------------",self.company_id)
        
        


    async def is_valid(self,registerid=None,db=None):
        
        company_id = QueryModelData(modeltable=Company_User, db=db, cols={"cid": self.company_id}).all()
        equipment = QueryModelData(modeltable=Equipment, db=db, cols={"sn": self.sn}).all()
        
        if equipment:
            register = QueryModelData(modeltable=EquipmentRegister,db=db , cols={"registerid": registerid.registerid,"register_status":"Y"} ).first()
            if not register:
                self.errors.append("Register Equipment For Maintenance")
            if register:
                if activityfound := QueryModelData(modeltable=EquipmentActivity, db=db, cols={"registerid": registerid.registerid, "next_activity":"T","activity_status":"UPS"}).first():
                    self.errors.append("The Equipment Already in  Maintenance Mode")
        else:
            self.errors.append(" The Equipment  Not added Do Want To add ")
        return not self.errors
       
