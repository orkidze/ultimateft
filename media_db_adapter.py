import sqlalchemy
import os

class media_db_adapter:
    user = "jlemszjdrzdpcp"
    password = "5535447b7c379896937f4111f3d37b2bd8f86da4b9d9e0c84d962779652ef455"
    db = "d7d6vdurd0b8vu"
    host = 'ec2-50-19-251-149.compute-1.amazonaws.com'
    port = 5432

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