import sqlite3
import time

from flask import Flask, request, make_response

app = Flask("google login")
con = sqlite3.connect("fruitshop.sqlite", check_same_thread=False)
cur = con.cursor()
def sleep(seconds):
    time.sleep(seconds)
    return None  # SQLite expects a return value

# Register function in SQLite
con.create_function("sleep", 1, sleep)

def init_db():

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username CHAR(100),
            name CHAR(100),
            password CHAR(100),
            email CHAR(150)
        );  
        
        CREATE TABLE IF NOT EXISTS fruits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            amountleft text,
            discount text
        );
    
        CREATE TABLE IF NOT EXISTS creditcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cardnumber TEXT,
            name TEXT,
            surname TEXT,
            cvr INTEGER
        );
        """)
    con.commit()
    fruits = cur.execute("SELECT * FROM fruits").fetchall()
    if not fruits:
        cur.executemany(
            "INSERT INTO fruits (name, price, amountleft, discount) VALUES (?, ?, ?,?)",
            [
                ("Apple", 1.2, '10', '0'),
                ("Banana", 0.8,  '10', '0'),
                ("Orange", 1.0, '10', '0'),
                ("Strawberry", 2.5,'10', '0'),
                ("Mango", 3.0, '10', '0')
            ],
        )

    con.commit()

    creditcards = cur.execute("SELECT * FROM creditcards").fetchall()
    if not creditcards:
        cur.executemany(
            "INSERT INTO creditcards (cardnumber,name, surname, cvr) VALUES (?, ?, ?,?)",
            [
                ("12345678945613245678", 'alice', 'alisoc', '123'),
                ("12345678945613245679", 'bob', 'bobsen','345')
            ],
        )

    con.commit()

@app.route("/logincheck")
def logincheck():

   user_ = request.args.get('username')
   password_ = request.args.get('password')
   cur.execute("SELECT * FROM users where username = '" + user_ + "' and password = '"+password_+"'")
   rows = cur.fetchall()

   result = "<ul> <li> <b>username &nbsp name &nbsp password &nbsp email &nbsp cprnumber</b></li>"
   for row in rows:
       result += "<li>"+ str(row[0]) + "&nbsp" + str(row[1]) + "&nbsp" + str(row[2]) + "&nbsp" + str(row[3]) + "&nbsp" + "</li>"

  # con.close()
   return result + "</ul>"

@app.route("/insert")
def insert():
   user_ = request.args.get('username')
   pass_ = request.args.get('password')
   name_ = request.args.get('fullname')
   email_ = request.args.get('email')

   cur = con.cursor()
   cur.executescript("INSERT INTO users (username, name, password, email) VALUES ('"+ user_ +"','" + pass_ +"','" + email_ +"','" + name_ +"')")
   con.commit()
   return ("<html><head><title>Registration success</title><body> "+
           "Registration success <a href='/login'>&nbsp; Please Login</a></body></html>")

@app.route("/register")
def register():
    resp_html = ("<html><head><title>Webshop</title></head><body>"+
            "<form action='/insert' method='get'>"+
            "<div id = 'div'>" +
            " <label>Username:</label><br> "+
            " <input type='text' name='username'><br><br>"+
            " <label>E-mail:</label><br> " +
            " <input type='text' name='email' id = 'e'><br><br>" +
            " <label>Full name:</label><br> " +
            " <input type='text' name='fullname' id = 'f'><br><br>" +
            " <label>Password:</label><br>"+
            " <input type='password' name='password' id ='pwd'><br><br>"+
            " <button type='submit'>Register</button></form><body></html>")
    resp = make_response(resp_html)

    return resp

@app.route("/")
def index():
    resp_html = ("<html><head><title>Webshop</title></head><body>"+
            "<h1>Welcome to the fruitshop</h1>"+
            "<h2><a href='/register'>Register</a></h2>" +
            "<h2><a href='/login'>Login</a></h2>" +
            "<body></html>")
    resp = make_response(resp_html)

    return resp

@app.route("/login")
def login():
    resp_html = ("<html><head><title>Webshop</title></head><body>"+
            "<form action='/logincheck' method='get'>"+
            "<div id = 'div'>" +
            " <label>Username:</label><br> "+
            " <input type='text' name='username'><br><br>"+
            " <label>Password:</label><br>"+
            " <input type='password' name='password' id ='pwd'><br><br>"+
            " <button type='submit'>Login</button></form><body>")
    resp = make_response(resp_html)

    return resp

if __name__ == "__main__":
    init_db()
    app.run(host="localhost", port=8080, debug=True)
