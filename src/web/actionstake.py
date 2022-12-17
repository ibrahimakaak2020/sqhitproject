from db.models.models import EquipmentActivity


def actions(activity:EquipmentActivity=None):
    activity_status=activity.activity_status

    if activity_status=='UPL':
        return {'Repaire Status':'locally', 'candemnational': 'candem'}

    if activity_status=='WFS':
        return {'Send': 'send', 'keep for decision': 'keepfor', 'candemnational': 'candem'}
    if activity_status=='UPS':
        return {'Recieve': 'recievefromcompany'}
    if activity_status=='WFD':
        return {'Send To Company': 'send', 'Repaire On IT Workshop': 'Workshop', 'Return Back To Deparmtment': 'returnbackto','candemnational': 'candem'}
    if activity_status=='WFR':
        return {'Return Back To Deparmtment': 'returnbackto','keep for decision': 'keepfor'}
   
    else:
        return {'Send To Company': 'send','Waiting for Send':'waitingfor', 'Repaire On IT Workshop': 'Workshop', 'candemnational': 'candem'}



          