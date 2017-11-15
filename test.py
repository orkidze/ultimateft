from flask import Flask, render_template
import sqlalchemy
import flask_login


app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def connect(user, password, db, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    for i in con.execute("select * from website.person"):
        print(i['name'])
        print(i['lastname'])
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return con, meta


#con_, meta_ = connect('postgres', 'c4inaz', 'postgres')

def getName(user, password, db, id, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    for i in con.execute("select name from website.person where ID = "+ id ):
        name = i['name']
    meta = sqlalchemy.MetaData(bind=con, reflect=True)
    return name

def getAll(user, password, db, id, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)
    con = sqlalchemy.create_engine(url, client_encoding='utf8')
    for i in con.execute("select * from website.person where ID = "+ id ):
       print(i)
       return i
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

#print(con_)

#print(meta_)




@app.route("/")
def hello():
    return "Hello world"


@app.route("/name/<ID>")
def home(ID):
    return render_template("home.html", name=getName('postgres', 'c4inaz', 'postgres',ID))

@app.route("/profile/<ID>")
def profile(ID):
    all = getAll('postgres', 'c4inaz', 'postgres',ID)
    return render_template("profile.html", all=all)


if __name__ == '__main__':
    app.run()