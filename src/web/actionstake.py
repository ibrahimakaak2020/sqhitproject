def actions(activity_status:str=None):

    if activity_status=='UPL':
        return {'Repaired': '/repaired', 'Notreaired': '/notreaired', 'candemnational': '/candem'}

    if activity_status=='WFS':
        return {'Send': '/send', 'keep for decision': '/keepfor', 'candemnational': '/candem'}
    if activity_status=='UPS':
        return {'Recieve Repaired': '/repaired', 'Recieve Not Repaired': '/notrepaired'}
    if activity_status=='WFD':
        return {'Send To Company': '/send', 'Repaire On IT Workshop': '/locally', 'candemnational': '/candem'}
    if activity_status=='WFR':
        return {'Return Back': '/return','keep for decision': '/keepfor'}
   
    else:
        return {'Send To Company': '/send','Waiting for Send':'/waitingfor', 'Repaire On IT Workshop': '/locally', 'candemnational': '/candem'}