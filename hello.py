import sqlite3
sql = sqlite3.connect('PhotoDiary.db')
print("Opened database successfully")
sql.execute('CREATE TABLE User (user_id INTEGER PRIMARY KEY,name VARCHAR(30) NOT NULL,email VARCHAR(30) NOT NULL UNIQUE, password VARCHAR(30) NOT NULL)')
sql.execute('CREATE TABLE Post (post_id INTEGER PRIMARY KEY,user_id INTEGER,content TEXT,keyword VARCHAR(100),img BLOB,FOREIGN KEY (user_id) REFERENCES User(user_id))')
sql.execute('CREATE TABLE Message (message_id INTEGER PRIMARY KEY,sender_id INTEGER,receiver_id INTEGER,message TEXT,FOREIGN KEY (sender_id) REFERENCES User(user_id),FOREIGN KEY (receiver_id) REFERENCES User(user_id))')
print("Table created successfully")
sql.close()