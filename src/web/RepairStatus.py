from db.models.models import EquipmentActivity


def RStatus(activity:EquipmentActivity=None):
    maintaince_status=activity.maintaince_status

    if maintaince_status=='RR':
        return 'REPAIRED'

    else:
        return 'NOT REPAIRED'
   

