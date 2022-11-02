from typing import List
from typing import Optional
from datetime import datetime

from fastapi import Depends, Request
from sqlalchemy import null
from api.route_login import get_current_user_from_token
from db.datacreator import QueryModelData
from db.database.database import SessionLocal, get_db
from db.models.models import  Company_User, Equipment, EquipmentActivity, EquipmentRegister


class LocallyForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.sn:str
        self.activity_desc:str
        
       


    async def load_data(self):
        form = await self.request.form()
        
        self.activity_desc = form.get('activity_desc')
         
        self.sn = form.get('sn')
        
        


    async def is_valid(self,registerid,db:SessionLocal):

        if check := QueryModelData(modeltable=EquipmentActivity, db=db, cols={"registerid": registerid, "next_activity": "T","activity_status":"UPL" ,"maintaince_status": None}).first():
            self.errors.append(f"Equipment Under Maintenance Status ? date of Maintenance : {check.activity_date} Take Care by:{check.user.staffname}")

        if not self.activity_desc:
          self.errors.append("Write Your Notes For Your Form Colleges ")
        return not self.errors
       
