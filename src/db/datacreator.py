from tkinter import N
from sqlalchemy.orm.exc import NoResultFound
from db.models.models import *
from db.database.database import Base , get_db
from db.schemas.schemas import UserCreate
from db.models import models
from sqlalchemy.orm import Session
from core.hashing import Hasher
from sqlalchemy import func, null
from sqlalchemy import inspect
from sqlalchemy import text,and_ ,not_
def get_pkey(modeltable,db , pkey):
    modelkey=getattr(modeltable, pkey)
    return db.query(func.max(modelkey)).scalar()

def ModelData(modeltable=None,modelcreate=None):
    Mapper=inspect(modeltable)
    mapper_pkey=[c for c in Mapper.columns if c.primary_key][0]
    columns = [m.key for m in modeltable.__table__.columns]
    createcols=modelcreate.__fields__.keys()
    data={}
    for col in columns:
        if col in createcols:
            data[col] = Hasher.get_password_hash(dict(modelcreate)[col]) if col == "password" else dict(modelcreate)[col]

        elif mapper_pkey.name==col:
            if primarykey := get_pkey(modeltable=modeltable, db=next(get_db()), pkey=str(col)):
                data[col]=primarykey+1
            else:
                data[col]=1
        else:
            data[col]=0
    return data


def CreateModelData(modeltable:None,db:Session,modelcreate:None):
    #keys=list(modelcreate.__fields__.keys())
    try:
        data=ModelData(modeltable=modeltable,modelcreate=modelcreate)
        modeldata1 = modeltable(
            **data
        )
        db.add(modeldata1)
        db.commit()
        db.refresh(modeldata1)
        return modeldata1
    except Exception as e:
        raise False from e


def get_user(username:str,db: Session):
    return db.query(User).filter(User.staffno == username).first()

def get_recieveuser(staffno):
    return next(get_db()).query(User).filter(User.staffno == staffno).first()
    
def QueryModelData(modeltable, db:Session, cols: dict = None):
   
    if cols is None:
        cols = {}
    return db.query(modeltable).filter_by(**cols) if cols else db.query(modeltable)

def Queryactivityhistory(registerid:int):
    session=next(get_db())
   
    return session.query(EquipmentActivity).filter(EquipmentActivity.registerid==registerid).all()


def QueryModelDataActivity(db:Session,search:str=None,active:bool=True):
    if search:
        return db.query(EquipmentActivity).join(EquipmentRegister).filter(and_(EquipmentRegister.sn == search, EquipmentActivity.date_of_maintaince.is_(None)))
    else:
        return db.query(EquipmentActivity).join(EquipmentRegister).filter(EquipmentActivity.date_of_maintaince.is_(None))



  
  
# start of update model function
def update_table(modeltable, col_id, updatecols,db):
  db.query(modeltable).filter_by(**col_id).update(dict(updatecols))
  db.commit()


def UpdateModelData(modeltable, col_id, updatecols,db):
    """
    dynamic_table: name of the table, "User" for example
    col_id: id of which column you want to update
    dynamic_cols: key value pairs {name: "diana"}
    """
    print("from update dynamic ",models)
    if hasattr(models, modeltable.__table__.name):
        table = getattr(models, modeltable.__table__.name)
        print(modeltable.__table__.name)


        if hasattr(table, *col_id):
                col_info = db.query(table).filter_by(**col_id).first()
                print(col_info)
                for (key, value) in updatecols.items():
                    if hasattr(table, key):
                        setattr(col_info, key, value)

                    else:
                        return "not has attr"
                db.commit()
                return True



        else:
            return 'table not has activityid'


    return "model not found"


#end of update model function
# start if delete Model data Function
def DeleteModelData(modeltable:None, db:Session, cols: dict = None):


    if cols is None:
        cols = {}
    try:
        if data := QueryModelData(modeltable=modeltable, db=db, cols=cols):
            db.delete(*data)
            db.commit()

            return True
        else:
            return False
    except NoResultFound:

            return False

# end of delete Model data Function
def QueryAll(tablename,db:Session):
    return db.query(tablename).all() if hasattr(models,tablename) else False



def authenticate_user(username,password):
    if user := QueryModelData(modeltable=User, db=next(get_db()), cols={"staffno": username}).all()[0]:
        return user if Hasher.verify_password(password,user.password) else False
    else:
        return False

def createactivityupl(db:Session,activityid:int=None,localactivity=None,maintaince_status=None):
    if activityid:
        activity=QueryModelData(modeltable=EquipmentActivity,db=db,cols={"activityid":activityid,"next_activity":"T"}).first()
        if activity:
            
             update_table(modeltable=EquipmentActivity,col_id={"activityid":activity.activityid},updatecols={},db=db)

    
    else:
        CreateModelData(modeltable=EquipmentActivity,db=db, modelcreate=localactivity)

                

def select(table, session, **criteria):
    query = session.query(table)
    for key, value in criteria.items():
        query = query.filter(getattr(table, key) == value)
    return query.all()




# Create a dictionary that maps table names to classes
tables = {
    "users": User,
    "equipment_model":Equipment_Model,
    "equipment_type":Equipment_Type,
    "equipment":Equipment,
    "company_user":Company_User,
    "manufacture":Manufacture,
    "location":Location,
    "equipmentactivity":EquipmentActivity,
}

def update(table_name, session, filter, data):
    # Get the class for the specified table
    table_class = tables[table_name]

    try:
        # Update the specified record in the database
        session.query(table_class).filter(filter).update(data)

        # Commit the transaction
        session.commit()

    except Exception as e:
        # Handle the exception
        print(e)

class CRUD:
    def __init__(self, table_class, pk_name):
        # engine = create_engine('postgresql://user:password@host:port/database')
        Session = next(get_db())
        self.session = Session
        self.table_class = table_class
        self.pk_name = pk_name

    def create(self, **kwargs):
        entry = self.table_class(**kwargs)
        self.session.add(entry)
        self.session.commit()

    def read(self, **kwargs):
        entries = self.session.query(self.table_class).filter_by(**kwargs).all()
        return entries

    def update(self, pk_value, **kwargs):
        entry = self.session.query(self.table_class).filter(getattr(self.table_class, self.pk_name)==pk_value).first()
        for key, value in kwargs.items():
            setattr(entry, key, value)
        self.session.commit()

    def delete(self, pk_value):
        entry = self.session.query(self.table_class).filter(getattr(self.table_class, self.pk_name)==pk_value).first()
        self.session.delete(entry)
        self.session.commit()



def myfirstname():
    return "ibrahim ali"



def AdminUser():
    user=User(staffno=9999,staffname="ibrahim ali amor akaak",password=Hasher.get_password_hash("1234"),admin_role=1)

    next(get_db()).add(user)
    next(get_db()).commit()
    next(get_db()).refresh(user)

    return user
    

    