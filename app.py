from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3

app = Flask(__name__, instance_relative_config = True)
app.secret_key="Narendran20$"
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

def patientlist():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("SELECT PATIENT_ID,PATIENT_NAME FROM PATIENTS")
    patienttab=cur.fetchall()
    con.close()
    return patienttab

def doctorlist():
    con=sqlite3.connect(database)
    cur=con.cursor()
    cur.execute("SELECT DOC_ID,DEPT_ID,DOC_NAME,SPECIALIZATION FROM DOCTORS")
    doctab=cur.fetchall()
    con.close()
    return doctab

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
        cur.execute("SELECT PATIENT_ID,PATIENT_NAME FROM PATIENTS WHERE PATIENT_NAME LIKE ?", ('%'+name+'%',))
    else:
        cur.execute("SELECT PATIENT_ID,PATIENT_NAME FROM PATIENTS")
    patienttab = cur.fetchall()
    con.close()
    return render_template("admin/patient.html",patienttab=patienttab, search=name)

@app.route('/doctor_list')
def doctor_list():
    name = request.args.get('name', '').strip()
    con=sqlite3.connect(database)
    cur=con.cursor()
    if name:
        cur.execute("SELECT DOC_ID,DEPT_ID,DOC_NAME,SPECIALIZATION FROM DOCTORS WHERE DOC_NAME LIKE ?", ('%'+name+'%',))
    else:
        cur.execute("SELECT DOC_ID,DEPT_ID,DOC_NAME,SPECIALIZATION FROM DOCTORS")
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
        dept_id = request.form.get('dept_id')
        name = request.form.get('name')
        specialization = request.form.get('specialization')
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("INSERT INTO DOCTORS (DEPT_ID, DOC_NAME, SPECIALIZATION) VALUES (?, ?, ?)", (dept_id, name, specialization))
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

if __name__ == "__main__":
    app.run(debug=True)
