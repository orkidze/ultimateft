import sqlalchemy
class login_db_adapter:
    user = "postgres"
    password = "c4inaz"
    db = "postgres"
    host = 'localhost'
    port = 5432
    def __init__(self):
        return
    def getUser(self,id):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        for i in con.execute("select * from website.users where id ="+id):
            return i
    def getUserID(self,username):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        for i in con.execute("select * from website.users where username ='"+username+"'"):
            return i
    def login(self,username,password):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        for i in con.execute("select password from website.users where username ='"+username+"'"):
            if i['password'] != password:
                return False
            else:
                return True
    def signup(self, username, password, email):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user , self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        con.execute("insert into website.users (username,email,password,balance) values('"+ username +"', '"+email+ "', '"+password+"',1000)")
        return
    def getUpcomingEvents(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        i = con.execute(
            "select * from website.events")
        return i
    def getFights(self, id):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        i = con.execute(
            "select * from website.fight where evid = '"+id+"'")
        return i
    def getEventName(self,id):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        i = con.execute(
            "select eventename from website.events where eventid = '" + id + "'")
        return i
    def getTop50(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        i = con.execute(
            "select * from website.users order by balance limit 50 ")
        return i
    def makeBet(self,fightID,userID,outcome,amount):
        i = self.getUser(userID)
        if int(amount) > int(i[4]):
            return False
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        con.execute("insert into website.bet(fight,uid,outcome,amount,status) values('"+str(fightID)+"',"+str(userID)+","+str(outcome)+","+str(amount)+",'Waiting')")
        con.execute("update website.users set balance = balance - "+str(amount)+"where id = "+str(userID))
        return True
    def getBets(self,userID):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        i = con.execute("select e.eventename,f.fighter_1,f.fighter_2, b.outcome, b.amount, f.f1koef, f.f2koef, b.status from website.bet b inner join website.users u on b.uid = u.id inner join website.fight f on b.fight = f.fightid inner join website.events e on f.evid = e.eventid where u.id = "+str(userID))
        return i