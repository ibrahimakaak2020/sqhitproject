from typing import List
from typing import Optional
from datetime import datetime

from fastapi import Depends, Request
from api.route_login import get_current_user_from_token
from db.datacreator import QueryModelData
from db.database.database import get_db
from db.models.models import  Equipment,Equipment_Model


class CreateEquipmentModelForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.equipment_model:Optional[str] = None
        self.mid: Optional[str] = None
        self.eid: Optional[str] = None
       
        
       


    async def load_data(self):
        form = await self.request.form()
        self.equipment_model = form.get(
            "equipment_model"
        ) 
        self.mid = form.get(
            "mid"
        )
        self.eid = form.get("eid")
      
    


    async def is_valid(self,db=None):
        if equipment := QueryModelData(modeltable=Equipment_Model, db=db, cols={"equipment_model": self.equipment_model}).all():
            self.errors.append("The Equipment Model Is Already Registered")
        return not self.errors
