from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, DateTime,DECIMAL
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from db.database.database import *
import datetime
from sqlalchemy.orm import relationship


#Base = declarative_base()
class Manufacture(Base):
    __tablename__ = "manufacture"

    mid = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(30),nullable=False)
    equipment_model = relationship("Equipment_Model", back_populates="manufacture")
    def __repr__(self):
       return f"Manufacture(id={self.mid!r}, name={self.company_name})"


class Equipment_Model(Base):
     __tablename__ = "equipment_model" 


     emid=Column(Integer, primary_key=True, index=True)
     equipment_model=Column(String(30),nullable=False) 
     mid=Column(Integer, ForeignKey('manufacture.mid'))
     manufacture = relationship("Manufacture", back_populates="equipment_model")

     eid=Column(Integer, ForeignKey('equipment_type.eid'))
     equipment_type = relationship("Equipment_Type", back_populates="equipment_model")
    
     equipments = relationship("Equipment", back_populates="equipment_model")
     def __repr__(self):
        return f"Equipment Model (id={self.emid!r}, Equipment Model={self.equipment_model!r})"

class Equipment(Base):
    __tablename__ = "equipment"

    sn = Column(String(30), primary_key=True, index=True)
    emid=Column(Integer, ForeignKey('equipment_model.emid') )
    standby=Column(String(1),default='N')
    own_location=Column(String(30))
    equipment_model = relationship("Equipment_Model", back_populates="equipments")
    locid = Column(Integer,ForeignKey('location.locid'))
    locations = relationship("Location", back_populates="equipments")
    equipment_register=relationship("EquipmentRegister", back_populates="equipments")
    candm_yn = Column(String(1), default='N')
    def __repr__(self):
        return f"Equipment(sn={self.sn!r}, equipment type={self.equipment_model  !r})"

class Equipment_Type(Base):
    __tablename__ = "equipment_type"

    eid = Column(Integer, primary_key=True, index=True)
    equipment_type = Column(String(30),nullable=False) 
    equipment_model = relationship("Equipment_Model", back_populates="equipment_type")

    def __repr__(self):
        return f"Equipment type (id={self.eid!r}, equipment type={self.equipment_type!r})"



class Location(Base):
    __tablename__ = "location"

    locid = Column(Integer, primary_key=True, index=True)
    loc_name = Column(String(30),nullable=False) 
    building = Column(String(100),nullable=False) 
    contact_number = Column(String(30),nullable=False) 
    equipments= relationship("Equipment", back_populates="locations")
    def __repr__(self):
        return f"Location (id={self.locid!r}, location={self.building!r})"


    
class EquipmentRegister(Base):
    __tablename__ = "equipmentregister"

    registerid = Column(Integer, primary_key=True, index=True)
    date_of_register = Column(DateTime, default=datetime.datetime.now ,nullable=False) 
    register_by =  Column(Integer, ForeignKey('user.staffno'))
    user = relationship("User", back_populates="equipment_register") 
    register_desc = Column(String(300) , nullable=False)
    workorderid=Column(Integer)
    register_status=Column(String(1) ,default='Y')# active y or not active n
    sn = Column(String(30), ForeignKey('equipment.sn'))
    equipments = relationship("Equipment", back_populates="equipment_register")
    equipmentactivity=relationship("EquipmentActivity", back_populates="equipmen_register")
    order_by=" date_of_register"
        
    def __repr__(self):
        return f" Equipment Register (SN ={self.sn}, descriptions ={self.register_desc},register status ={self.register_status})"

class EquipmentActivity(Base):
    __tablename__ = "equipmentactivity"
    activityid = Column(Integer, primary_key=True, index=True)
    registerid= Column(Integer, ForeignKey('equipmentregister.registerid'))

    equipmen_register=relationship("EquipmentRegister", back_populates="equipmentactivity")
    activity_date = Column(DateTime,default=datetime.datetime.now) 
    create_by =  Column(Integer, ForeignKey('user.staffno'))
    user=relationship("User", back_populates="activities")
    recieve_by =  Column(Integer)
   
    next_activity=Column(String(3))# Yes(have another activity or NO  Finall activity or Conadmnations
    activity_desc = Column(String(300))
    recieve_note = Column(String(300))
    activity_status = Column(String(3) ) # RR Repaired RO Not Repaired CC Condamnation
    maintaince_status=Column(String(3))
    date_of_maintaince = Column(DateTime)   
    place_of_maintaince=Column(String(1) ) # local L or Send to Company S
    billid=Column(String(30))
    billamount=Column(DECIMAL)
    company_id= Column(Integer, ForeignKey('company_user.cid'))
    company_user=relationship("Company_User", back_populates="equipmentactivity")
    date_of_send = Column(DateTime)
    date_of_returnback = Column(DateTime)   
    date_of_recievefrom = Column(DateTime) 
    order_by=" activity_date"
    def __repr__(self):
        return f" Equipment Activity (user={self.create_by}, status ={self.activity_date})"



class User(Base):
    __tablename__ = "user"

    staffno = Column(Integer, primary_key=True, index=True)
    staffname = Column(String(100),nullable=False) 
    password = Column(String(30),nullable=False) 
    admin_role=Column(Integer,nullable=False)
    equipment_register = relationship("EquipmentRegister", back_populates="user")
    activities = relationship("EquipmentActivity", back_populates="user")

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
     
    def __repr__(self):
        return f"User (staff No ={self.staffno  !r}, staff Name={self.staffname !r})"


class Company_User(Base):
    __tablename__ = "company_user"

    cid = Column(Integer, primary_key=True, index=True)
    staffname = Column(String(50),nullable=False) 
    company_name_en = Column(String(50),nullable=False) 
    company_name_ar = Column(String(50),nullable=False) 
    contactnumber = Column(String(30),nullable=False) 
    equipmentactivity = relationship("EquipmentActivity", back_populates="company_user")
    def __repr__(self):
        return f"User (staff No ={self.cid  !r}, staff Name={self.staffname !r})"
#for test test
