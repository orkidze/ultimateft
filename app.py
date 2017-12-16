from flask import Flask, request, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired, length, Email
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from login_db_adapter import login_db_adapter
import tools
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
    admin = False;
    def __init__(self, id,username,email,password,balance,admin):
        self.id = id
        self.username = username
        self.password = password
        self. email = email
        self.balance = balance
        self.admin = admin;


@login_manager.user_loader
def load_user(user_id):
    i = database.getUser(user_id)
    return User(user_id,i[1],i[2],i[3],i[4],i[7])


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
            user = User(i[0],i[1],i[2],i[3],i[4],i[7])
            login_user(user, remember = form.remember.data)
            flash("You logged in")
            return redirect(url_for('dash'))
        flash("Invalid username or password")
        return redirect(url_for("login"))

    return render_template('login.html', form=form)


@app.route("/signup",methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if not database.availableUsername(form.username.data):
            flash("Username already taken")
            return redirect(url_for('signup'))
        if not database.availableEmail(form.email.data):
            flash("Email already taken")
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        database.signup(form.username.data,hashed_password,form.email.data)
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)


@app.route("/adminpanel",methods=['GET','POST'])
@login_required
def adminpanel():
    if not current_user.admin:
        return redirect(url_for('index'))
    if request.method == 'POST':
        action = request.form['todo']
        if action == 'insert fighter':
            name = request.form['name']
            database.insertFighter(name)
            flash(name +' inserted')
            return redirect(url_for('adminpanel'))
        if action == "search fighter":
            name = request.form['name']
            arr = list()
            for i in database.searchFighter(name):
                arr.append(i)
            for item in arr:
                flash("ID: " + str(item['fighter_id']) + " Name: " + item['name'])

            return redirect(url_for('adminpanel'))
        if action == "create event":
            name = request.form['name']
            date = request.form['date']
            database.createEvent(name,date)
            flash("Event created")
            return redirect(url_for('adminpanel'))
        if action == "get upcoming":
            arr = list()
            for i in database.getUpcomingEvents():
                arr.append(i)
            for item in arr:
                flash("ID: " + str(item['event_id']) + " Name: " + item['event_name'])
            return redirect(url_for('adminpanel'))
        if action == "create fight":
            fighter1 = request.form['fighter_1']
            fighter2 = request.form['fighter_2']
            koef1 = request.form['koef_1']
            koef2 = request.form['koef_2']
            id = request.form['event_id']
            database.createFight(id,fighter1,fighter2,koef1,koef2)
            flash("Fight created")
            return redirect(url_for('adminpanel'))
        if action == "search fight":
            name = request.form['name']
            for i in database.searchFight(name):
                for item in i:
                    flash("Fight ID: " + str(item[0]) + " " +str(item[1]) +" ("+str(item[3])+") VS " + str(item[2])+" ("+str(item[4])+") EVENT: "+str(item[5]))
            return redirect(url_for('adminpanel'))
        if action == "fight results":
            fightID = request.form['fight_id']
            fighter = request.form['fighter']
            database.fightResults(fightID,int(fighter))
            flash(fightID + " " + fighter)
            return redirect(url_for('adminpanel'))
        if action == "cancel fight":
            fightID = request.form['fight_id']
            database.cancelFight(fightID)
            flash("Canceled")
            return redirect(url_for('adminpanel'))
    return render_template('adminpanel.html')


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


@app.route("/profile")
@login_required
def profile():
    arr = list()
    for i in database.getUserID(current_user.username):
        arr.append(i)
    return render_template('profile.html', list=arr, username = current_user.username, balance=current_user.balance)


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


@app.route('/past_event/<id>',methods=['GET'])
def past_event(id):
    arr = list()
    arr1 = list()
    for i in database.getEventName(id):
        arr1.append(i)
    for i in database.getFights(id):
        arr.append(i)
    return render_template('event_past.html', fights=arr, name=arr1, username=current_user.username,
                           balance=current_user.balance)

@app.route('/event/<id>',methods=['GET'])
@login_required
def event(id):
    arr = list()
    arr1 = list()
    for i in database.getEventName(id):
        arr1.append(i)
    if tools.isBeforeNow(arr1[0][1]):
        return redirect(url_for('event.html', fights=arr, name=arr1, username=current_user.username,
                               balance=current_user.balance))
    for i in database.getFights(id):
        arr.append(i)

    return render_template('event.html', fights=arr, name=arr1, username = current_user.username, balance=current_user.balance)


@app.route('/event/<id>',methods=['POST'])
@login_required
def event_p(id):
    arr = list()
    arr1 = list()
    for i in database.getEventName(id):
        arr1.append(i)
    for i in database.getFights(id):
        arr.append(i)
    try:
        text = request.form['amount']
        radio = request.form['radio']
        value = 2
        if radio == 'option1':
            value = 1
        fight = request.form['fight']
    except:
        flash("You need to make a selection")
        return redirect(url_for('event', id=id, fights=arr, name=arr1, username=current_user.username,
                                balance=current_user.balance))
    if not database.makeBet(fight,current_user.id,value,text):
        flash("Not enough balance or invalid value")
    else:
        flash("You made bet of: " + text+ " units ")
    return render_template('event.html',id=id, fights=arr, name=arr1, username=current_user.username,
                               balance=current_user.balance)
    #return redirect(url_for('event', id=id,fights=arr, name=arr1, username = current_user.username, balance=current_user.balance))


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
