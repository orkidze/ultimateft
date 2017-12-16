import datetime
def isBeforeNow(date):
    now = datetime.date.now()
    if(date<now):
        return True
    else:
        return False
