from flask import Flask, render_template, request,redirect,url_for , session,flash
from datetime import timedelta
import sqlite3
app = Flask(__name__)


app.config["SECRET_KEY"] = "abcd"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/post',methods=['GET','POST'])


@app.route('/userList')
def user_list():
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    cur.execute('SELECT * FROM User')
    users = cur.fetchall()
    return render_template("UserList.html",users=users)

@app.route('/login',methods=['GET','POST'])
def login_page():
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    if request.method == 'POST':
        try:
            data = request.json

            cur.execute("SELECT * FROM User WHERE email = ?", (data['email'],))
            user = cur.fetchone()

            if user[2] == data['email']:
                if user[3] == data['password'] :
                    session['email'] = data['email']
                    session['id'] = user[0]
                    session['username'] = user[1]
                    session.permanent = True
                    return render_template('index.html')
                else:
                    return redirect(url_for("login_page"))
        except Exception as e:
            print("Email doesn't exist")
            return redirect(url_for("login_page"))
    if request.method == 'GET':
        return render_template("login.html")

@app.route('/signup',methods=['GET','POST'])
def register_page():
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    if request.method == 'POST':
        try:
            data = request.json
            if data['name'] == "" or data['email'] == "" or data['password1'] == "" or data['password2'] == "":
                flash("입력되지 않는 값이 존재합니다.")
                return redirect(url_for("register_page"))
            if data['password1'] != data['password2']:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("register_page"))

            cur.execute("INSERT INTO User(name,email,password)VALUES (?,?,?)", (data['name'], data['email'], data['password1']))

            sql.commit()

        except Exception as e:
            flash("이메일 아이디가 중복됩니다.")
            sql.rollback()
            return redirect(url_for("register_page"))

        return render_template("login.html")


    elif request.method == 'GET':
        return render_template("signUp.html")





if __name__ == '__main__':
    app.run(debug=True)