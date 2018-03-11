import sqlalchemy
import os

class media_db_adapter:
    user = ""
    password = ""
    db = ""
    host = ''
    port = 0

    def __init__(self):
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, self.db)
        uri = os.environ.get('DATABASE_URL', 'postgres://username:password@192.168.1.42/FLASK_ENTRY')
        self.con = sqlalchemy.create_engine(uri, pool_size=5, client_encoding='utf8')
        return

    def getTop5s(self):
        i = self.con.execute('select id,title,picture from website.top5')
        return i

    def getTop5(self,id):
        for i in self.con.execute('select t.id, t.title, t.picture, t.content, t.date, u.username, t.date from website.top5 t inner join website.users u on t.author = u.id where t.id = '+id):
            return i

    def nextTop5(self,id):
        for i in self.con.execute('select id,title,picture from website.top5 where id > ' + id +' order by id ASC limit 1'):
            return i
    def preveusTop5(self,id):
        for i in self.con.execute(
                                'select id,title,picture from website.top5 where id < ' + id + ' order by id DESC limit 1'):
            return i