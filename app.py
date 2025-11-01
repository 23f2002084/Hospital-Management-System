from flask import Flask, render_template
import os
import sqlite3

app = Flask(__name__, instance_relative_config = True)
database=os.path.join(app.instance_path, "hospitalmanagement.db")

def count():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute('SELECT COUNT(*)FROM DOCTORS')
    doccount=cur.fetchone()[0]
    cur.execute('SELECT COUNT(*)FROM USERS')
    usercount=cur.fetchone()[0]
    cur.execute('SELECT COUNT(*)FROM DEPARTMENT')
    deptcount=cur.fetchone()[0]
    con.close()
    return doccount, usercount, deptcount

@app.route('/')

def home():
    doctor,user,dept=count()
    return render_template("admin/dashboard.html",doctor=doctor,user=user,dept=dept)


if __name__ == "__main__":
    app.run(debug=True)
