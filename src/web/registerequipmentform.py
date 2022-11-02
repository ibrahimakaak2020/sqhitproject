from typing import List
from typing import Optional
from datetime import datetime

from fastapi import Request
from api.route_login import get_current_user_from_token


class RegisterForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.register_desc: Optional[str] = None
        self.register_by: Optional[str] = None
        self.workorderid: Optional[str] = None
        self.sn: Optional[str] = None
       


    async def load_data(self):
        form = await self.request.form()
        self.register_desc = form.get(
            "register_desc"
        ) 
        self.register_by = form.get(
            "register_by"
        )
        self.workorderid = form.get("workorderid")
        self.sn= form.get("sn")
       


    async def is_valid(self):

        if len(self.register_desc) <= 4:
            self.errors.append("Write Your Description  ...")
        return not self.errors
