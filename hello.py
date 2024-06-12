import sqlite3
sql = sqlite3.connect('PhotoDiary.db')
print("Opened database successfully")
sql.execute('CREATE TABLE User (user_id INTEGER PRIMARY KEY,name VARCHAR(30) NOT NULL,email VARCHAR(30) NOT NULL UNIQUE, password VARCHAR(30) NOT NULL)')
sql.execute('CREATE TABLE Post (post_id INTEGER PRIMARY KEY,user_id INTEGER,content TEXT,img BLOB,FOREIGN KEY (user_id) REFERENCES User(user_id))')
sql.execute('CREATE TABLE Message (message_id INTEGER PRIMARY KEY,sender_id INTEGER,receiver_id INTEGER,message TEXT,FOREIGN KEY (sender_id) REFERENCES User(user_id),FOREIGN KEY (receiver_id) REFERENCES User(user_id))')
sql.execute('CREATE TABLE keywords (keyword_id INTEGER PRIMARY KEY,post_id INTEGER,keyword VARCHAR(30) NOT NULL,FOREIGN KEY (post_id) REFERENCES Post(post_id))')
print("Table created successfully")
sql.close()


"""
로그인이 필요한 작업 하기 전에 권한 확인
키워드 작업
메세지 선택해서 응답및 삭제 작업
"""

