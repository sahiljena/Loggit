from flask import Flask,render_template,redirect,request,session,url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'sahiljena'

#conn = sqlite3.connect('users.db')
with sqlite3.connect("users.db") as conn:
    c = conn.cursor()
    l = ("CREATE TABLE IF NOT EXISTS base (username text, email text,pass text)")
    c.execute(l)
    conn.commit()









@app.route('/signup',methods = ['POST','GET'])
def signup():
    err = ""
    data = []
    if not session:
        if request.method == "POST":

            username = request.form['username']
            email = request.form['email']
            password = request.form['password']

            with sqlite3.connect("users.db") as conn:
                c = conn.cursor()
                l = ("SELECT username from base where username = '{}'").format(username)
                c.execute(l)
                data = c.fetchall()
            if data:
                err = "Username already exsist! Please choose another!"
                return render_template('signup.html',err = err)
            else:
                with sqlite3.connect("users.db") as conn:
                    c = conn.cursor()
                    l = ("INSERT INTO base(username,email,pass) VALUES('{}','{}','{}') ").format(username,email,password)
                    c.execute(l)
                    conn.commit()
                    l = ("CREATE TABLE if not exists {}_loggs (heading text,logg text,date text)").format(username)
                    c.execute(l)
                    conn.commit()
                    l = ("INSERT INTO {}_loggs(heading,logg,date) VALUES('Joined Loggit !','',datetime('now', 'localtime'))").format(username)
                    c.execute(l)
                    conn.commit()
                    err = "Account Created! Please login!"
                return render_template('signup.html',err = err)
        return render_template('signup.html')
    else:
        return redirect('/')




@app.route('/login',methods = ['GET','POST'])
def login():
    err = ""
    if not session:
        if request.method == "POST":

            session.pop('user_id',None)
            session.pop('user_name',None)

            username = request.form['username']
            password = request.form['password']
            
            data = []
            with sqlite3.connect("users.db") as conn:
                c = conn.cursor()
                l = ("SELECT * FROM base WHERE username = '{}' AND pass = '{}'").format(username,password)
                c.execute(l)
                data = c.fetchall()
            if data and data[0][2] == password:
                session['user_name'] = data[0][0]
                return redirect('/')
            else:
                return render_template('login.html',err = "Wrong Username Or Password!")
        return render_template('login.html')
    else:
        return redirect('/')
@app.route('/')
def index():
    err = ""
    if  not session:
        return redirect('/login')
    else:
        data = []
        username = session['user_name']
        with sqlite3.connect("users.db") as conn:
            c = conn.cursor()
            l = ("SELECT rowid,heading,logg,date FROM {}_loggs").format(username)
            c.execute(l)
            data = c.fetchall()
        return render_template('index.html',name = username, log_data = data, err = err)

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    session.pop('user_name',None)
    return redirect('/')


@app.route('/post/',methods = ['POST'])
def post():
    err = ""
    if not session:
        return redirect('/')
    else:
        log = request.form['log']
        head = request.form['heading']
        username = session['user_name']
        with sqlite3.connect("users.db") as conn:
            try :
                c = conn.cursor()
                l = ("INSERT INTO {}_loggs (heading,logg,date) VALUES('{}','{}',datetime('now', 'localtime')) ").format(username,head,log)
                c.execute(l)
                conn.commit()
                l =("SELECT rowid FROM {}_loggs ORDER BY rowid DESC LIMIT 1").format(username)
                c.execute(l)
                new = c.fetchall()
                r = ('/#{}').format(new[0][0])
                return redirect(r)
            except:
                err = "Something Went Wrong!"
                return redirect(url_for('.index', err = err))

        
