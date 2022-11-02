from abc import ABC, abstractmethod
from db.database.database import get_db,Base
from db.models.models import User , Location
from fastapi import Depends
from sqlalchemy.orm import Session
from core.hashing import Hasher
class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f'Expected {value!r} to be one of {self.options!r}')

class Number(Validator):

    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f'Expected {value!r} to be an int or float')
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(
                f'Expected {value!r} to be at least {self.minvalue!r}'
            )
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(
                f'Expected {value!r} to be no more than {self.maxvalue!r}'
            )

class String(Validator):

    def __init__(self, minsize=None, maxsize=None, predicate=None):
        self.minsize = minsize
        self.maxsize = maxsize
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Expected {value!r} to be an str')
        if self.minsize is not None and len(value) < self.minsize:
            raise ValueError(
                f'Expected {value!r} to be no smaller than {self.minsize!r}'
            )
        if self.maxsize is not None and len(value) > self.maxsize:
            raise ValueError(
                f'Expected {value!r} to be no bigger than {self.maxsize!r}'
            )
        if self.predicate is not None and not self.predicate(value):
            raise ValueError(
                f'Expected {self.predicate} to be true for {value!r}'
            )



class Component:

    name = String(minsize=3, maxsize=10, predicate=str.isupper)
    kind = OneOf('wood', 'metal', 'plastic')
    quantity = Number(minvalue=0)

    def __init__(self, name, kind, quantity):
        self.name = name
        self.kind = kind
        self.quantity = quantity


class StaticMethod:
    "Emulate PyStaticMethod_Type() in Objects/funcobject.c"

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        return self.f

    def __call__(self, *args, **kwds):

        return self.f(*args, **kwds)

def ModelData(model=None,modelcreate=None):
    columns = [m.key for m in model.__table__.columns]
    print(columns)
    createcols=modelcreate.__fields__.keys()
    print(createcols)
    data={}
    for col in columns:
        if col in createcols:
            data[col]=col
        else:
            data[col]=0
    return data


def CreateModelData(model:None,db:Session,modelcreate:None):
    #keys=list(modelcreate.__fields__.keys())
    data={ "staffno":"123445","staffname":"ibrahim ali","password":Hasher.get_password_hash("ibrahim" ),"admin_role":1}
    modeldata1 = model(
        **data
    )
    db.add(modeldata1)
    db.commit()
    db.refresh(modeldata1)
    return modeldata1


def testquery(model:Base,db:Session,opt:str):
    operation={"query":"query","add":"add","update":"update","delete":"delete"}
    if opt in operation:
        if opt=="query":
            return db.query(model).all()
        else:
            return "others"
    else:
        return "this type of operation Not supported"

from db.schemas.schemas import UserCreate, LocationCreate
def queryall(db:Session):

    return db.query(User).all()

if __name__ == "__main__":
    user =UserCreate(staffno=1223,staffname="ibrahim ",password="sfs")
    loc=LocationCreate(loc_name="administration",building="hospital", contact_number= "9933323")
    print(ModelData(model=Location,modelcreate=loc))




