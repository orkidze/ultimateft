import sqlalchemy
import os
from werkzeug.security import generate_password_hash,check_password_hash
class login_db_adapter:
    user = "jlemszjdrzdpcp"
    password = "5535447b7c379896937f4111f3d37b2bd8f86da4b9d9e0c84d962779652ef455"
    db = "d7d6vdurd0b8vu"
    host = 'ec2-50-19-251-149.compute-1.amazonaws.com'
    port = 5432
    def __init__(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        uri = os.environ.get('DATABASE_URL', 'postgres://username:password@192.168.1.42/FLASK_ENTRY')
        self.con = sqlalchemy.create_engine(uri, client_encoding='utf8')
        return
    def getUser(self,id):

        for i in self.con.execute("select * from website.users where id ="+id):
            return i
    def getUserID(self,username):

        for i in self.con.execute("select * from website.users where username ='"+username+"'"):
            return i

    def login(self,username,password):
        for i in self.con.execute("select password from website.users where username ='"+username+"'"):
            if check_password_hash(i['password'],password):
                return True
            else:
                return False
    def availableUsername(self,username):
        i = self.con.execute("select count(id) from website.users where username = '"+username+"'")
        for item in i:
            if int(item['count']) == 0:
                return True
        return False
    def availableEmail(self,email):
        i = self.con.execute("select count(id) from website.users where email = '"+email+"'")
        for item in i:
            if int(item['count']) == 0:
                return True
        return False
    def signup(self, username, password, email):

        self.con.execute("insert into website.users (username,email,password) values('"+ username +"', '"+email+ "', '"+password+"')")
        return
    def getUpcomingEvents(self):

        i = self.con.execute(
            "select * from website.events")
        return i
    def getFights(self, id):
        i = self.con.execute(
            "select * from website.fight where evid = '"+id+"'")
        return i
    def getEventName(self,id):

        i = self.con.execute(
            "select event_name from website.events where event_id = '" + id + "'")
        return i
    def getTop50(self):

        i = self.con.execute(
            "select * from website.users order by balance desc limit 50 ")
        return i
    def makeBet(self,fightID,userID,outcome,amount):
        i = self.getUser(userID)
        if len(amount) == 0:
            return False
        if int(amount) > int(i[4]):
            return False

        self.con.execute("insert into website.bet(fight,uid,outcome,amount,status) values('"+str(fightID)+"',"+str(userID)+","+str(outcome)+","+str(amount)+",'Waiting')")
        self.con.execute("update website.users set balance = balance - "+str(amount)+"where id = "+str(userID))
        return True
    def getBets(self,userID):

        i = self.con.execute("select e.eventename,f.fighter_1,f.fighter_2, b.outcome, b.amount, f.f1koef, f.f2koef, b.status from website.bet b inner join website.users u on b.uid = u.id inner join website.fight f on b.fight = f.fightid inner join website.events e on f.evid = e.eventid where u.id = "+str(userID))
        return i