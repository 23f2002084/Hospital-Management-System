from flask import Flask, render_template, request, redirect, url_for
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
    cur.execute('SELECT COUNT(*)FROM PATIENTS')
    patcount=cur.fetchone()[0]
    cur.execute("SELECT COUNT(*)FROM APPOINTMENTS WHERE STATUS='Booked'")
    appcount=cur.fetchone()[0]
    con.close()
    return doccount, usercount, deptcount, patcount,appcount

def tabledata():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("SELECT APPOINTMENT_ID,PATIENT_NAME,DOC_NAME,APPOINTMENT_DATE,APPOINTMENT_TIME FROM APPOINTMENTS WHERE STATUS='Booked'")
    tab=cur.fetchall()
    con.close()
    return tab

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/register', methods=['POST'])
def register():
    uname=request.form['uname']
    email=request.form['email']
    pwd=request.form['pwd']
    pnum=request.form['pnum']
    dob=request.form['dob']
    gender=request.form['Gender']
    role=request.form['Role']
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute(
        '''INSERT INTO USERS(NAME,EMAIL,PASSWORD,GENDER,PHONE_NUMBER,DOB,ROLE)
           VALUES(?,?,?,?,?,?,?);''',
           (uname,email,pwd,gender,pnum,dob,role)
    )
    con.commit()
    con.close()
    return redirect(url_for('index'))

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        pwd=request.form['pwd']
        role=request.form['Role']
        con=sqlite3.connect(database)
        cur=con.cursor()
        cur.execute(
            'SELECT * FROM USERS WHERE EMAIL=? AND PASSWORD=?',(email,pwd)
        )
        res=cur.fetchone()
        con.close()
        if res:
            if role=="Doctor":
                return redirect(url_for('doctor_dashboard'))
            elif role=="Patient":
                return redirect(url_for('patient_dashboard'))
            elif role.lower()=="admin":
                return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Login Credentials"
    return render_template('login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    doctor,user,dept,pat,app=count()
    tab=tabledata()
    return render_template("admin/dashboard.html",doctor=doctor,user=user,dept=dept,pat=pat,app=app,tab=tab)


if __name__ == "__main__":
    app.run(debug=True)
