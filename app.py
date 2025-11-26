from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3

app = Flask(__name__, instance_relative_config = True)
app.secret_key="Narendran20$"
database=os.path.join(app.instance_path, "hospitalmanagement.db")

def dbinit():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS(
                USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT,
                EMAIL TEXT UNIQUE,
                PASSWORD TEXT,
                GENDER TEXT,
                PHONE_NUMBER TEXT,
                ROLE TEXT,
                STATE TEXT,
                DOB TEXT)''')
    con.commit()
    cur.execute('INSERT OR IGNORE INTO USERS (NAME,EMAIL,PASSWORD,GENDER,PHONE_NUMBER,ROLE,STATE) VALUES("ADMIN","admin@123","admin123","NA","9962286705","Admin","Active")')
    con.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS PATIENTS(
                PATIENT_ID INTEGER PRIMARY KEY,
                PATIENT_NAME TEXT,
                AGE INTEGER,
                GENDER TEXT,
                ADDRESS TEXT,
                CONTACT TEXT,
                BLOOD_GRP TEXT,
                ALLERGIES TEXT,
                STATE TEXT,
                FOREIGN KEY (PATIENT_ID) REFERENCES USERS (USER_ID) ON DELETE CASCADE)''')
    con.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS DEPARTMENTS(
                DEPT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DEPT_NAME TEXT)''')
    con.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS DOCTORS(
                DOC_ID INTEGER PRIMARY KEY,
                DOC_NAME TEXT,
                DEPT_NAME TEXT,
                STATE TEXT,
                FOREIGN KEY (DOC_ID) REFERENCES USERS (USER_ID) ON DELETE CASCADE,
                FOREIGN KEY (DEPT_NAME) REFERENCES DEPARTMENTS (DEPT_NAME))''')
    con.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS APPOINTMENTS(
                APPOINTMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                PATIENT_ID INTEGER,
                PATIENT_NAME TEXT,
                DOC_ID INTEGER,
                DOC_NAME TEXT,
                APPOINTMENT_DATE DATE,
                APPOINTMENT_TIME TIME,
                STATUS TEXT,
                FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS (PATIENT_ID),
                FOREIGN KEY (PATIENT_NAME) REFERENCES PATIENTS (PATIENT_NAME),
                FOREIGN KEY (DOC_ID) REFERENCES DOCTORS (DOC_ID),
                FOREIGN KEY (DOC_NAME) REFERENCES DOCTORS (DOC_NAME),
                UNIQUE (DOC_ID, APPOINTMENT_DATE, APPOINTMENT_TIME))''')
    con.commit()
    con.close()


def count():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute('SELECT COUNT(*)FROM DOCTORS')
    doccount=cur.fetchone()[0]
    cur.execute('SELECT COUNT(*)FROM USERS')
    usercount=cur.fetchone()[0]
    cur.execute('SELECT COUNT(*)FROM DEPARTMENTS')
    deptcount=cur.fetchone()[0]
    cur.execute('SELECT COUNT(*)FROM PATIENTS')
    patcount=cur.fetchone()[0]
    cur.execute("SELECT COUNT(*)FROM APPOINTMENTS WHERE STATUS='Booked'")
    appcount=cur.fetchone()[0]
    con.close()
    return doccount, usercount, deptcount, patcount,appcount

def admintabledata():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("SELECT APPOINTMENT_ID,PATIENT_NAME,DOC_NAME,APPOINTMENT_DATE,APPOINTMENT_TIME FROM APPOINTMENTS WHERE STATUS='Booked'")
    tab=cur.fetchall()
    con.close()
    return tab

def tabledata(drname=None):
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("SELECT APPOINTMENT_ID,PATIENT_NAME,DOC_NAME,APPOINTMENT_DATE,APPOINTMENT_TIME FROM APPOINTMENTS WHERE STATUS='Booked' AND DOC_NAME=?",(drname,))
    tab=cur.fetchall()
    con.close()
    return tab

@app.route('/')
def index():
    dbinit()
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
        '''INSERT INTO USERS(NAME,EMAIL,PASSWORD,GENDER,PHONE_NUMBER,DOB,ROLE,STATE)
           VALUES(?,?,?,?,?,?,?,"Active");''',
           (uname,email,pwd,gender,pnum,dob,role)
    )
    con.commit()
    if role=="Patient":
        cur.execute('''INSERT INTO PATIENTS(PATIENT_NAME,GENDER,STATE) VALUES(?,?,"Active")''',
                    (uname,gender))
        con.commit()
    if role=="Doctor":
        cur.execute('''INSERT INTO DOCTORS(DOC_NAME,STATE) VALUES(?,"Active")''',
                    (uname,))
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
            session['username']=res[1]
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
    tab=admintabledata()
    return render_template("admin/dashboard.html",doctor=doctor,user=user,dept=dept,pat=pat,app=app,tab=tab)

@app.route('/patient_dashboard')
def patient_dashboard():
    return render_template("patient/dashboard.html")

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if 'username' in session:
        drname=session['username']
    tab=tabledata(drname)
    return render_template("doctor/dashboard.html",drname=drname,tab=tab)

@app.route('/patient_list')
def patient_list():
    name = request.args.get('name', '').strip()
    con=sqlite3.connect(database)
    cur=con.cursor()
    if name:
        cur.execute("SELECT PATIENT_ID,PATIENT_NAME, STATE FROM PATIENTS WHERE PATIENT_NAME LIKE ?", ('%'+name+'%',))
    else:
        cur.execute("SELECT PATIENT_ID,PATIENT_NAME, STATE FROM PATIENTS")
    patienttab = cur.fetchall()
    con.close()
    return render_template("admin/patient.html",patienttab=patienttab, search=name)

@app.route('/doctor_list')
def doctor_list():
    name = request.args.get('name', '').strip()
    con=sqlite3.connect(database)
    cur=con.cursor()
    if name:
        cur.execute("SELECT DOC_ID,DEPT_NAME,DOC_NAME, STATE FROM DOCTORS WHERE DOC_NAME LIKE ?", ('%'+name+'%',))
    else:
        cur.execute("SELECT DOC_ID,DEPT_NAME,DOC_NAME, STATE FROM DOCTORS")
    doctab = cur.fetchall()
    con.close()
    return render_template("admin/doctor.html",doctab=doctab, search=name)

@app.route('/appointment_list')
def appointment_list():
    name = request.args.get('name', '').strip()
    con=sqlite3.connect(database)
    cur=con.cursor()
    if name:
        cur.execute("SELECT APPOINTMENT_ID,PATIENT_NAME,DOC_NAME,APPOINTMENT_DATE,APPOINTMENT_TIME FROM APPOINTMENTS WHERE PATIENT_NAME LIKE ?", ('%'+name+'%',))
    else:
        cur.execute("SELECT APPOINTMENT_ID,PATIENT_NAME,DOC_NAME,APPOINTMENT_DATE,APPOINTMENT_TIME FROM APPOINTMENTS")
    apptab = cur.fetchall()
    con.close()
    return render_template("admin/appointments.html",apptab=apptab, search=name)


@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        dept_name = request.form.get('dept_name')
        name = request.form.get('name')
        specialization = request.form.get('specialization')
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("INSERT INTO DOCTORS (DEPT_NAME, DOC_NAME, SPECIALIZATION) VALUES (?, ?, ?)", (dept_name, name, specialization))
        con.commit()
        con.close()
        return redirect(url_for('doctor_list'))
    return render_template('admin/add_doctor.html')


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("INSERT INTO PATIENTS (PATIENT_NAME) VALUES (?)", (patient_name,))
        con.commit()
        con.close()
        return redirect(url_for('patient_list'))
    return render_template('admin/add_patient.html')


@app.route('/editdoc/<int:doc_id>', methods=['GET', 'POST'])
def editdoc(doc_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if request.method == 'POST':
        dept_id = request.form.get('dept_id')
        doc_name = request.form.get('doc_name')
        specialization = request.form.get('specialization')
        cur.execute("UPDATE DOCTORS SET DEPT_ID=?, DOC_NAME=?, SPECIALIZATION=? WHERE DOC_ID=?", (dept_id, doc_name, specialization, doc_id))
        con.commit()
        con.close()
        return redirect(url_for('doctor_list'))
    
    cur.execute("SELECT DOC_ID, DEPT_ID, DOC_NAME, SPECIALIZATION FROM DOCTORS WHERE DOC_ID=?", (doc_id,))
    doc = cur.fetchone()
    con.close()
    if not doc:
        return "Doctor not found", 404
    
    return render_template('admin/editdoc.html', doc={
        'id': doc[0], 'dept_id': doc[1], 'doc_name': doc[2], 'specialization': doc[3]
    })

@app.route('/blacklistdoc/<int:doc_id>', methods=['POST'])
def blacklistdoc(doc_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("UPDATE DOCTORS SET STATE ='Blacklist' WHERE DOC_ID = ?",(doc_id,))
    con.commit()
    con.close()
    return redirect(url_for('doctor_list'))

@app.route('/unbandoc/<int:doc_id>', methods=['POST'])
def unbandoc(doc_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("UPDATE DOCTORS SET STATE ='Active' WHERE DOC_ID = ?",(doc_id,))
    con.commit()
    con.close()
    return redirect(url_for('doctor_list'))

@app.route('/editpat/<int:patient_id>', methods=['GET', 'POST'])
def editpat(patient_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        cur.execute("UPDATE PATIENTS SET PATIENT_NAME=? WHERE PATIENT_ID=?", (patient_name, patient_id))
        con.commit()
        con.close()
        return redirect(url_for('patient_list'))

    cur.execute("SELECT PATIENT_ID, PATIENT_NAME FROM PATIENTS WHERE PATIENT_ID=?", (patient_id,))
    p = cur.fetchone()
    con.close()
    if not p:
        return "Patient not found", 404
    return render_template('admin/editpat.html', patient={'id': p[0], 'name': p[1]})

@app.route('/blacklistpat/<int:patient_id>', methods=['POST'])
def blacklistpat(patient_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("UPDATE PATIENTS SET STATE ='Blacklist' WHERE PATIENT_ID = ?",(patient_id,))
    con.commit()
    con.close()
    return redirect(url_for('patient_list'))

@app.route('/unbanpat/<int:patient_id>', methods=['POST'])
def unbanpat(patient_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("UPDATE PATIENTS SET STATE ='Active' WHERE PATIENT_ID = ?",(patient_id,))
    con.commit()
    con.close()
    return redirect(url_for('patient_list'))

if __name__ == "__main__":
    app.run(debug=True)
