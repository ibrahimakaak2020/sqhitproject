from db.datacreator import CreateModelData , QueryModelData,UpdateModelData ,DeleteModelData, QueryAll
from db.database.database import get_db
import json
from core.hashing import Hasher
from db.schemas.schemas import UserCreate, LocationCreate,ManufactureCreate  , EquipmentModelCreate

from db.models.models import User , Location , Manufacture , Equipment_Model,Equipment , Company_User , EquipmentRegister , EquipmentActivity,Equipment_Type

from db.datacreator import authenticate_user

if __name__ == "__main__":
    user=UserCreate(staffno="12345",staffname="ibrahim ali alsadouni ",password="12345")

    #CreateModelData(modeltable=User,db=next(get_db()),modelcreate=user)
    print( authenticate_user(username="12345",password="12345"))
