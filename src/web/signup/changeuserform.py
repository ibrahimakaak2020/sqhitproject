from typing import List
from typing import Optional

from fastapi import Request
from db.database.database import SessionLocal
from db.datacreator import QueryModelData
from db.models.models import User
from core.hashing import Hasher

class ChangeUserForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.currentpassword: Optional[str] = None
        self.newpassword: Optional[str] = None
       


    async def load_data(self):
        form = await self.request.form()
        self.currentpassword = form.get("currentpassword")
        self.newpassword = form.get("newpassword")
      

    async def is_valid(self,db:SessionLocal,staffno=None):
        user = QueryModelData(
            modeltable=User, db=db, cols={"staffno": staffno}
        ).first()
        if not Hasher.verify_password(self.currentpassword, user.password):
            self.errors.append("Current Password Not Corrent Please Enter Your Password")

        if not self.errors:
            return True
        return False
