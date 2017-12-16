import datetime
def isBeforeNow(date):
    now = datetime.datetime.now()
    if(date<now):
        return True
    else:
        return False
