from typing import List
from typing import Optional

from fastapi import Request
from db.database.database import SessionLocal
from db.datacreator import QueryModelData
from db.models.models import User
from core.hashing import Hasher

class SignupForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.staffno: Optional[str] = None
        self.password: Optional[str] = None
        self.staffname: Optional[str] = None
        self.admin_role:Optional[int]=0


    async def load_data(self):
        form = await self.request.form()
        self.staffno = form.get(
            "username"
        )  # since outh works on username field we are considering email as username
        print(form.get("password"))
        # self.password = Hasher.get_password_hash(form.get("password"))
        self.password = form.get("password")
        self.staffname = form.get(
            "staffname"
        )
        self.admin_role = form.get(
            "admin_role"
        )

    async def is_valid(self,db:SessionLocal,username:str):
        user=QueryModelData(modeltable=User,db=db,cols={"staffno":username}).first()

        if user:
            self.errors.append("User Is exist ..."+user.staffname)

        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required more then 4 characters")
        
        if not self.errors:
            return True
        return False
