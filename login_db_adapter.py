import sqlalchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash


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
    def insertFighter(self,name):
        self.con.execute("insert into website.fighter(name) values('"+name+"')")

    def searchFighter(self,name):
        bucket = list()
        for i in self.con.execute("select fighter_id, name from website.fighter where name like '%%"+name+"%%' limit 10"):
            bucket.append(i)
        return bucket

    def getUser(self, id):
        for i in self.con.execute("select * from website.users where id =" + id):
            return i

    def getUserID(self, username):

        for i in self.con.execute("select * from website.users where username ='" + username + "'"):
            return i

    def login(self, username, password):
        for i in self.con.execute("select password from website.users where username ='" + username + "'"):
            if check_password_hash(i['password'], password):
                return True
            else:
                return False

    def availableUsername(self, username):
        i = self.con.execute("select count(id) from website.users where username = '" + username + "'")
        for item in i:
            if int(item['count']) == 0:
                return True
        return False

    def availableEmail(self, email):
        i = self.con.execute("select count(id) from website.users where email = '" + email + "'")
        for item in i:
            if int(item['count']) == 0:
                return True
        return False

    def signup(self, username, password, email):

        self.con.execute(
            "insert into website.users (username,email,password) values('" + username + "', '" + email + "', '" + password + "')")
        return

    def getUpcomingEvents(self):

        i = self.con.execute(
            "select * from website.events")
        return i

    def getFights(self, id):
        i = self.con.execute(" select fight.fight_id, fighter1.name, fighter2.name, fight.koef_1, "
                             "fight.koef_2, fight.event_id from website.fight fight left join website.fighter fighter1 "
                             "on fighter1.fighter_id = fight.fighter_1 left join "
                             "website.fighter fighter2 on fighter2.fighter_id = "
                             "fight.fighter_2 where event_id = '" + id + "'")
        return i

    def getEventName(self, id):

        i = self.con.execute(
            "select event_name from website.events where event_id = '" + id + "'")
        return i

    def getTop50(self):

        i = self.con.execute(
            "select * from website.users order by balance desc limit 50 ")
        return i

    def makeBet(self, fightID, userID, outcome, amount):
        i = self.getUser(userID)
        if len(amount) == 0:
            return False
        if int(amount) > int(i[4]):
            return False

        self.con.execute(
            "insert into website.bet(fight_id,u_id,outcome,amount) values('" + str(fightID) + "'," + str(
                userID) + "," + str(outcome) + "," + str(amount) + ")")
        self.con.execute("update website.users set balance = balance - " + str(amount) + "where id = " + str(userID))
        return True

    def getBets(self, userID):

        i = self.con.execute(
            "select e.event_name,fighter1.name,fighter2.name, b.outcome, b.amount, f.koef_1, f.koef_2, b.status "
            "from website.bet b inner join website.users u "
            "on b.u_id = u.id inner join website.fight f "
            "on b.fight_id = f.fight_id inner join website.events e "
            "on f.event_id = e.event_id "
            "left join website.fighter fighter1 on fighter1.fighter_id = f.fighter_1 "
            "left join website.fighter fighter2 on fighter2.fighter_id = f.fighter_2 "
            "where u.id =  " + str(userID))
        return i
    def createFight(self,event_id,fighter1,fighter2,koef1,koef2):
        self.con.execute("insert into fight(event_id,fighter_1,fighter_2,koef_1,koef_2) values("+event_id+","+fighter1+","+fighter2+","+koef1+","+koef2+")")
        return True

    def searchFight(self,eventname):
        i = self.con.execute("select event_id from website.events where event_name like '%%"+eventname+"%%'")
        ret = list()
        for item in i:
            ret.append(self.con.execute("select fight.fight_id, fighter1.name, fighter2.name, fight.koef_1, fight.koef_2, e.event_name from website.fight fight left join website.fighter fighter1 "
                                        "on fighter1.fighter_id = fight.fighter_1 left join "
                                        "website.fighter fighter2 on fighter2.fighter_id = fight.fighter_2 "
                                        "inner join website.events e on e.event_id = fight.event_id"
                                        " where fight.event_id = "+str(item[0]) + " limit 15"))
        return ret

    def createEvent(self,name,date):
        self.con.execute("insert into website.events(event_name,event_date) values('"+name+"','to_date('"+date+"','YYYY-MM-DD'))")