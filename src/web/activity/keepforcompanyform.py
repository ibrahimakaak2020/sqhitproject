from typing import List
from typing import Optional
from datetime import datetime

from fastapi import Depends, Request
from api.route_login import get_current_user_from_token
from db.datacreator import QueryModelData
from db.database.database import get_db
from db.models.models import  Equipment


class CreateEquipmentForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.msg:Optional[str] = None
        self.emid: Optional[str] = None
        self.locid: Optional[str] = None
        self.standby: Optional[str] = "N"
        self.candm_yn: Optional[str] = "N"
        
       


    async def load_data(self):
        form = await self.request.form()
        self.sn = form.get(
            "sn"
        ) 
        self.emid = form.get(
            "emid"
        )
        self.locid = form.get("locid")
      
    


    async def is_valid(self,db=None):
        if equipment := QueryModelData(modeltable=Equipment, db=db, cols={"sn": self.sn}).all():
            self.errors.append("The Equipment Is Already Registered")
        return not self.errors
