from flask import Flask, request, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired, length, Email
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from login_db_adapter import login_db_adapter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'verysecretsecretkey'
Bootstrap(app)
database = login_db_adapter()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    id =""
    username = ""
    password = ""
    email = ""
    balance = ""
    def __init__(self, id,username,email,password,balance):
        self.id = id
        self.username = username
        self.password = password
        self. email = email
        self.balance = balance


@login_manager.user_loader
def load_user(user_id):
    i = database.getUser(user_id)
    return User(user_id,i[1],i[2],i[3],i[4])


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),length(min=4,max=15)])
    password = PasswordField('password', validators=[InputRequired(), length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(),Email(message ='Invalid email'),length(min=5,max=50)])
    username = StringField('username', validators=[InputRequired(), length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), length(min=8, max=80)])


@app.route("/login", methods=['GET','POST'])

def login():
    if current_user.is_authenticated:

        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        if database.login(form.username.data,form.password.data):
            i = database.getUserID(form.username.data)
            user = User(i[0],i[1],i[2],i[3],i[4])
            login_user(user, remember = form.remember.data)
            return redirect(url_for('index'))
        return "Invalid username or password"

    return render_template('login.html', form=form)


@app.route("/signup",methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()

    if form.validate_on_submit():
        database.signup(form.username.data,form.password.data,form.email.data,)
        return "<h1> You have register! <h1>"

    return render_template('signup.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/top50")
@login_required
def top50():
    arr = list()
    for i in database.getTop50():
        arr.append(i)
    return render_template('top50.html', list=arr, username = current_user.username, balance=current_user.balance)


@app.route("/upcomingEvents")
@login_required
def upcomingEvents():
    arr = list()
    for i in database.getUpcomingEvents():
        arr.append(i)
    return render_template('upcomingEvents.html', list=arr, username = current_user.username, balance=current_user.balance)


@app.route("/")
def index():
    isOnline = False
    if current_user.is_authenticated:
        isOnline = True
        return render_template('index.html', isOnline=isOnline, username=current_user.username,
                               balance=current_user.balance)
    return render_template('index.html', isOnline = isOnline)


@app.route('/event/<id>',methods=['GET'])
@login_required
def event(id):
    arr = list()
    arr1 = list()
    for i in database.getEventName(id):
        arr1.append(i)
    for i in database.getFights(id):
        arr.append(i)
    return render_template('event.html', fights=arr, name=arr1, username = current_user.username, balance=current_user.balance)


@app.route('/event/<id>',methods=['POST'])
@login_required
def event_p(id):
    try:
        text = request.form['amount']
        radio = request.form['radio']
        value = 2
        if radio == 'option1':
            value = 1
        fight = request.form['fight']
    except:
        return "Bad data"
    if not database.makeBet(fight,current_user.id,value,text):
        return "Not enought balance"
    arr = list()
    arr1 = list()
    for i in database.getEventName(id):
        arr1.append(i)
    for i in database.getFights(id):
        arr.append(i)
    return redirect(url_for('event', id=id,fights=arr, name=arr1, username = current_user.username, balance=current_user.balance))


@app.route('/dash')
@login_required
def dash():
    return render_template('dash.html', username = current_user.username, balance=current_user.balance)


@app.route('/bets')
@login_required
def bets():
    return render_template('bets.html', username=current_user.username, balance=current_user.balance, list=database.getBets(current_user.id))
if __name__ == '__main__':
    app.run()