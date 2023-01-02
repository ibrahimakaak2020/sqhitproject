from typing import List
from typing import Optional
from datetime import datetime

from fastapi import Depends, Request
from api.route_login import get_current_user_from_token
from db.datacreator import QueryModelData
from db.database.database import get_db
from db.models.models import  Equipment,Equipment_Model, Location


class CreateLocationForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.loc_name:Optional[str] = None
        self.building:Optional[str] = None
        self.contact_number:Optional[str] = None
      
       
        
       


    async def load_data(self):
        form = await self.request.form()
        self.loc_name = form.get(
            "loc_name"
        ) 
        self.building = form.get(
            "building"
        )
        self.contact_number = form.get("contact_number")
      
    


    async def is_valid(self,db=None):
        if location := QueryModelData(modeltable=Location, db=db, cols={"loc_name": self.loc_name,"building":self.building}).all():
            self.errors.append("The Location  Already Registered")
        return not self.errors
