from functools import wraps
from flask import Flask, render_template, request,redirect,url_for , session,flash, jsonify
from datetime import timedelta
import sqlite3
app = Flask(__name__)


app.config["SECRET_KEY"] = "abcd"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)

@app.route('/')
def index():
    return render_template('index.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None or session.get("id") == "":
            flash("로그인 필요!")
            return redirect(url_for("index"))
        return f(*args, **kwargs)

    return decorated_function
@app.route('/feed')
@login_required
def feed():
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    sql = "SELECT * FROM Post ORDER BY post_id DESC"
    cur.execute(sql)
    posts = cur.fetchall()
    keyword=[]
    user =[]
    userId = []

    for row in posts:
        cur.execute("SELECT keyword FROM KEYWORDS WHERE post_id = ?", (row[0],))
        temp = []
        for word in cur.fetchall():
            temp.append(word[0])
        keyword.append(temp)
    for row in posts:
        cur.execute("SELECT user_id FROM POST WHERE post_id = ?", (row[0],))
        user_id = cur.fetchone()[0]
        userId.append(user_id)
        cur.execute("SELECT name FROM USER WHERE user_id = ?", (user_id,))
        user.append(cur.fetchone()[0])


    print(user)
    return render_template('feed.html',feeds=posts,keyword=keyword,user=user,userId=userId)

@app.route('/photo',methods=['POST','PATCH','DELETE'])
@login_required
def post_Photo():
    print("Photo")
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    print(request.method)
    if request.method == 'POST':
        data = request.form
        f = request.files['file']
        f.save('static/uploads/'+f.filename)

        print("수정",data['postId'])
        if data['postId']:
            print("!!!")
            cur.execute("DELETE FROM keywords WHERE post_id = ?",
                        (data['postId'],)
                        )
            sql.commit()
            cur.execute(
                "DELETE FROM POST WHERE post_id = ?",
                (data['postId'],)
            )
            sql.commit()
        try:
            cur.execute(
                "INSERT INTO Post(user_id,content,img)VALUES (?,?,?)"
                , (session.get("id"), data['content'], 'static/uploads/'+f.filename,))
            sql.commit()
            postId = cur.lastrowid
            print(postId)
            keywords = data['keyword']
            keywords = list(keywords.lower().split(','))

            for word in keywords:
                cur.execute("INSERT INTO keywords(post_id,keyword)VALUES (?,?)",(postId, word,))
                sql.commit()


            sql.commit()
            return redirect(url_for('profile_page'))
        except Exception as e:
            sql.rollback()
            return redirect(url_for('profile_page'))
    if request.method == 'PATCH':
        data = request.json
        f = request.files['img']
        f.save('static/uploads/' + f.filename)
        cur.execute(
            "UPDATE Post SET content = ?, keyword = ?, img = ? WHERE userId = ? AND postId=?",
            (data['content'], data['keyword'], 'static/uploads/' + f.filename, session['id'],data['postId'])
        )
        cur.execute(
            "DELETE keyword FROM post WHERE postId = ?", (data['postId'])
        )
        keywords = data['keyword']
        keywords = list(keywords.lower().split(' '))
        for word in keywords:
            cur.execute("INSERT INTO keyword(postId,keyword)VALUES (?,?),", data['postId'], word)

        data = cur.fetchall()
        if data:
            sql.commit()
            flash("Successfully updated")
            return 'uploadSuccess'
        else:
            sql.rollback()
            flash("Error")
            return 'Error'

    if request.method == 'DELETE':
        data = request.json
        print(data['postId'])
        try:
            cur.execute("SELECT user_id FROM Post WHERE post_id = ?", (data['postId'],))
            user_id = cur.fetchall()[0][0]
            print(user_id)
            sql.commit()
            if user_id == session.get('id'):
                cur.execute("DELETE FROM keywords WHERE post_id = ?",
                            (data['postId'],)
                            )
                sql.commit()
                cur.execute(
                    "DELETE FROM POST WHERE post_id = ?",
                    (data['postId'],)
                )
                sql.commit()
                return render_template('myprofile.html'), 200
            else:
                return 'Error'
        except Exception as e:
                print(e)
                sql.rollback()
                return 'Error'


@app.route('/search')
def search_posts():
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    data = request.json
    if " " in data['word']:
        flash("Error")
        return 'Error'
    if data is not None:
        cur.execute("SELECT p.* FROM posts p INNER JOIN hashtags h ON p.id = h.post_id WHERE h.tag = ?", data['word'])
    data = cur.fetchall()
    if data:
        sql.commit()
        flash("successfully searched")
        return 'SearchSuccess'
    else:
        sql.rollback()
        flash("Error")
        return 'Error'


@app.route('/messages',methods=['GET','POST','DELETE'])
@login_required
def message():
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    if request.method == 'GET':
        user=[]
        cur.execute("SELECT sender_id,message,message_id FROM Message WHERE receiver_id = ?",
                    (session.get('id'),))
        messages = cur.fetchall()
        print(messages)
        for message in messages:
            cur.execute("SELECT name FROM User WHERE user_id = ?",(message[0],))
            user.append(cur.fetchone()[0])
        print(user)
        return render_template('messages.html', messages=messages,user=user)

    if request.method == 'POST':
        data = request.json
        try:
            print("!")
            cur.execute(
                "INSERT INTO Message(sender_id,receiver_id,message) VALUES (?,?,?)",
                (session.get('id'),data['receiverId'], data['message'],)
            )
            sql.commit()
            print("@")
            return "Success"
        except Exception as e:
            print(e)
            sql.rollback()
            return 'Error'

    if request.method == 'DELETE':
        data = request.get_json()
        try:
            cur.execute(
                'DELETE FROM Message WHERE message_id = ?'
                , (data['messageId'],)
            )
            sql.commit()
            print("delete")
            return 'DeleteSuccess'
        except Exception as e:
            print(e)
            sql.rollback()
            return 'Error'




@app.route('/userlist')
def user_list():
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    cur.execute('SELECT * FROM User')
    users = cur.fetchall()
    print(users)
    return render_template("userlist.html",users=users)
@app.route('/checksession')
def checksession():
    print("come")
    print(session.get('id'))
    if session.get("id") is None or session.get("id") == "":
        return "LogIn"
    else:
        return "LogOut"
@app.route('/signin',methods=['GET','POST'])
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
                    return jsonify({'error': "Incorrect Password"}), 400
        except Exception as e:
            print("Email doesn't exist")
            return jsonify({'error': "Email doesn't exist"}), 400

    if request.method == 'GET':
        return render_template("signin.html")


@app.route("/logout")
@login_required
def member_logout():
    session.clear()
    print("로그아웃")
    return redirect(url_for("index"))

@app.route('/signup',methods=['GET','POST'])
def register_page():
    sql = sqlite3.connect("PhotoDiary.db")
    cur = sql.cursor()
    if request.method == 'POST':
        try:
            data = request.json
            print(data)
            if data['name'] == "" or data['email'] == "" or data['password1'] == "" or data['password2'] == "":
                flash("입력되지 않는 값이 존재합니다.")
                return redirect(url_for("register_page"))
            if data['password1'] != data['password2']:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("register_page"))
            cur.execute("INSERT INTO User(name,email,password)VALUES (?,?,?)", (data['name'], data['email'], data['password1'],))
            sql.commit()
            return redirect(url_for('login_page'))
        except Exception as e:
            print("중복!!")
            print(e)
            sql.rollback()
            return jsonify({'error': 'Email already exists'}), 400

    elif request.method == 'GET':
        return render_template("signup.html")

@app.route("/myprofile")
@login_required
def profile_page():
    if request.method == 'GET':
        sql = sqlite3.connect("PhotoDiary.db")
        cur = sql.cursor()
        keywords = []
        try:
            id = session.get('id')
            cur.execute("SELECT * FROM POST WHERE user_id = ? ORDER BY post_id DESC", (id,))
            posts = cur.fetchall()
            print(posts)
            for post in posts:
                cur.execute("SELECT keyword FROM KEYWORDS WHERE post_id = ?", (post[0],))
                key = cur.fetchall()

                temp =[]
                for k in key:
                    temp.append(k[0])
                keywords.append(temp)

        except Exception as e:
            print(e)
            posts = []

        print(keywords)
        return render_template("myprofile.html",posts=posts,keywords=keywords,name=session.get('username'))




if __name__ == '__main__':
    app.run(debug=True)