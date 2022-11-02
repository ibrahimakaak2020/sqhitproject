from typing import List
from typing import Optional
from datetime import datetime

from fastapi import Depends, Request
from api.route_login import get_current_user_from_token
from db.datacreator import QueryModelData
from db.database.database import get_db
from db.models.models import  Equipment


class CreateRepairedUpdateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.maintaince_status: Optional[str] = None
        self.recieve_note: Optional[str] = "N"
        
       


    async def load_data(self):
        form = await self.request.form()
        self.maintaince_status = form.get(
            "maintaince_status"
        ) 
        self.recieve_note = form.get(
            "recieve_note"
        )
        
    


    # async def is_valid(self,db=None):
    #     if equipment := QueryModelData(modeltable=Equipment, db=db, cols={"sn": self.sn}).all():
    #         self.errors.append("The Equipment Is Already Registered")
    #     return not self.errors
