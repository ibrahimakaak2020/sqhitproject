from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr

class ManufactureCreate( BaseModel ):

    company_name : str

    class Config:  # to convert non dict obj to json
        orm_mode = True

# class Manufactureshow( BaseModel ):
#     mid:int
#     company_name : str

#     class Config:  # to convert non dict obj to json
#         orm_mode = True
 


class EquipmentTypeCreate(BaseModel):

           equipment_type : str

           class Config:  # to convert non dict obj to json
             orm_mode = True


class EquipmentModelCreate(BaseModel):

           equipment_model : str
           mid:int
           eid:int

           class Config:  # to convert non dict obj to json
             orm_mode = True
    



class LocationCreate(BaseModel):

    loc_name : str
    building : str
    contact_number : str

    class Config:  # to convert non dict obj to json
        orm_mode = True

class EquipmentCreate(BaseModel):
    sn:str
    emid:int
    locid:int
    class Config:
        orm_mode=True
   
class UserCreate(BaseModel):
    staffno:int
    staffname:str
    password:str
    # admin_role:int

    class Config:
        orm_mode=True

#------------------------------------------
class CompanyUserCreate(BaseModel):
    staffname:str
    company_name_en:str
    company_name_ar:str
    contactnumber:str
    # admin_role:int

    class Config:
        orm_mode=True



#-------------------------------------------
class EquipmentCreate(BaseModel):
    sn:str
    emid:int
    locid:int
    class Config:
        orm_mode=True




class EquipmentRegisterCreate(BaseModel):
    sn:str
    register_by:int
    register_desc:str
    workorderid:str
   

    class Config:
        orm_mode=True



class EquipmentActivityCreate(BaseModel):
    registerid:int
    create_by:int
    company_id:int=None
    activity_desc:str
    next_activity:str=None
    activity_status:str
    place_of_maintaince:str
    maintaince_status:str=None
    billid:Optional[str]=None
    billamount:Optional[int]=0
    date_of_send:Optional[datetime]=None
    date_of_returnback:Optional[datetime]=None
    date_of_recievefrom:Optional[datetime]=None
    date_of_maintaince:Optional[datetime]=None

   

    class Config:
        orm_mode=True
