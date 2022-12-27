from db.models.models import EquipmentActivity


def Status(activity:EquipmentActivity=None):
    activity_status=activity.activity_status

    if activity_status=='UPL':
        return 'Maintenence Under IT'

    if activity_status=='WFS':
        return 'Waiting For Send'
    if activity_status=='UPS':
        return 'Maintenence Under company'
    if activity_status=='WFD':
        return 'Waiting For Decision'
    if activity_status=='WFR':
        return 'Waiting  To Return Deparmtment'
   
    else:
        return 'No in Register'



          