import datetime
def isBeforeNow(date):
    now = datetime.datetime.now().date()
    if(date<now):
        return True
    else:
        return False
