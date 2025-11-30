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
                FOREIGN KEY (DOC_NAME) REFERENCES DOCTORS (DOC_NAME))''')
    con.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS DOC_AVAILABILITY(
                AVAILABLE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DOC_ID INTEGER,
                DOC_NAME TEXT,
                DAY TEXT CHECK (DAY IN ('MON','TUE','WED','THU','FRI','SAT','SUN')),
                TIME TEXT,
                AVAILABILITY TEXT,
                FOREIGN KEY (DOC_ID) REFERENCES DOCTORS (DOC_ID),
                FOREIGN KEY (DOC_NAME) REFERENCES DOCTORS (DOC_NAME)
                )''')
    con.commit()
    cur.execute('''CREATE TABLE IF NOT EXISTS TREATMENTS(
                TREATMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                PATIENT_NAME TEXT,
                DOC_NAME TEXT,
                DIAGNOSIS TEXT,
                TREATMENT TEXT,
                PRESCRIPTION TEXT,
                FOREIGN KEY (DOC_NAME) REFERENCES DOCTORS (DOC_NAME)
                FOREIGN KEY (PATIENT_NAME) REFERENCES PATIENTS (PATIENTS_NAME)
                )''')
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
                    ("Dr. "+uname,))
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
            session['userid']=res[0]
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
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT APPOINTMENT_ID, PATIENT_NAME, DOC_NAME, APPOINTMENT_DATE, APPOINTMENT_TIME FROM APPOINTMENTS WHERE STATUS='Booked'")
    appdata=cur.fetchall()
    return render_template("admin/dashboard.html",doctor=doctor,user=user,dept=dept,pat=pat,app=app,appdata=appdata)

@app.route('/patient_dashboard')
def patient_dashboard():
    uname = session.get('username')
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT PATIENT_NAME FROM PATIENTS WHERE PATIENT_NAME LIKE ?", (f"%{uname}%",))
    name=cur.fetchone()
    patname=name[0]
    cur.execute("SELECT DEPT_NAME FROM DEPARTMENTS")
    depttab=cur.fetchall()
    cur.execute("SELECT DISTINCT DOC_NAME FROM DOC_AVAILABILITY")
    doctab=cur.fetchall()
    docdict={}
    cur.execute("SELECT DEPT_NAME, DOC_NAME FROM DOCTORS")
    res = cur.fetchall()
    for dept, doc in res:
        dept = dept.strip().upper()
        if dept not in docdict:
            docdict[dept]=[]
        docdict[dept].append(doc)
    timings={}
    cur.execute("SELECT DOC_NAME, DAY, TIME, AVAILABILITY FROM DOC_AVAILABILITY")
    res = cur.fetchall()
    for doc, day, time, avail in res:
        if doc not in timings:
            timings[doc] = []
        timings[doc].append(f"{day} : {time} → {avail}")
    print("TIMINGS:", repr(timings))
    cur.execute("SELECT APPOINTMENT_ID, DOC_NAME, APPOINTMENT_TIME, APPOINTMENT_DATE FROM APPOINTMENTS WHERE PATIENT_NAME LIKE ? AND STATUS='Booked'",(f"%{uname}%",))
    tab=cur.fetchall()
    return render_template("patient/dashboard.html",patname=patname,depttab=depttab,doctab=doctab,docdict=docdict,timings=timings,tab=tab)

@app.route('/doctor_dashboard')
def doctor_dashboard():
    uname = request.form.get('doc_name') or session.get('username')
    uid = request.form.get('doc_id') or session.get('userid')
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT DOC_ID, DOC_NAME FROM DOCTORS WHERE DOC_NAME LIKE ?', (f"%{uname}%",))
    res = cur.fetchone() 
    docid, drname = res[0], res[1]
    cur.execute("SELECT APPOINTMENT_ID, PATIENT_NAME, APPOINTMENT_DATE, APPOINTMENT_TIME FROM APPOINTMENTS WHERE DOC_NAME=? AND STATUS='Booked'",(drname,))
    tab=cur.fetchall()
    print(tab)
    dist=[]
    for i in range(len(tab)):
        if tab[i][1] not in dist:
            dist.append(tab[i][1])
    print("dist is",dist)
    return render_template("doctor/dashboard.html",drname=drname,tab=tab,dist=dist)

@app.route('/patient_list')
def patient_list():
    name = request.args.get('name', '').strip()
    con=sqlite3.connect(database)
    cur=con.cursor()
    if name:
        cur.execute("SELECT * FROM PATIENTS WHERE PATIENT_NAME LIKE ? OR CONTACT LIKE ? OR PATIENT_ID LIKE ?", ('%'+name+'%','%'+name+'%','%'+name+'%'))
    else:
        cur.execute("SELECT * FROM PATIENTS")
    patienttab = cur.fetchall()
    con.close()
    return render_template("admin/patient.html",patienttab=patienttab, search=name)

@app.route('/doctor_list')
def doctor_list():
    uname = session.get('username')
    print(uname)
    name = request.args.get('name', '').strip()
    con=sqlite3.connect(database)
    cur=con.cursor()
    if name:
        cur.execute("SELECT DOC_ID,DEPT_NAME,DOC_NAME, STATE FROM DOCTORS WHERE DOC_NAME LIKE ? OR DEPT_NAME LIKE ?", ('%'+name+'%', '%'+name+'%'))
    else:
        cur.execute("SELECT DOC_ID,DEPT_NAME,DOC_NAME, STATE FROM DOCTORS")
    doctab = cur.fetchall()
    con.close()
    if uname=='ADMIN':
        return render_template("admin/doctor.html",doctab=doctab, search=name)
    else:
        return render_template("patient/doctor.html",doctab=doctab,search=name)
    

@app.route('/appointment_list')
def appointment_list():
    name = request.args.get('name', '').strip()
    con=sqlite3.connect(database)
    cur=con.cursor()
    if name:
        cur.execute("SELECT APPOINTMENT_ID,PATIENT_NAME,DOC_NAME,APPOINTMENT_DATE,APPOINTMENT_TIME, STATUS FROM APPOINTMENTS WHERE PATIENT_NAME LIKE ? ORDER BY STATUS", ('%'+name+'%',))
    else:
        cur.execute("SELECT APPOINTMENT_ID,PATIENT_NAME,DOC_NAME,APPOINTMENT_DATE,APPOINTMENT_TIME, STATUS FROM APPOINTMENTS ORDER BY STATUS")
    apptab = cur.fetchall()
    con.close()
    return render_template("admin/appointments.html",apptab=apptab, search=name)


@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        dept_name = request.form.get('dept_name')
        name = request.form.get('name')
        gender=request.form.get('gender')
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("INSERT INTO USERS (NAME, EMAIL, PASSWORD, GENDER, ROLE, STATE) VALUES (?, ?, ?, ?, ?, ?)", ("Dr. "+name, name+"@gmail.com",name, gender, "Doctor", "Active"))
        con.commit()
        cur.execute("INSERT INTO DOCTORS (DEPT_NAME, DOC_NAME, STATE) VALUES (?, ?, ?)", (dept_name,"Dr. "+name, "Active"))
        con.commit()
        con.close()
        return redirect(url_for('doctor_list'))
    return render_template('admin/add_doctor.html')


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient_name = request.form.get('patient_name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        address = request.form.get('address')
        contact = request.form.get('contact')
        blood = request.form.get('blood')
        allergies = request.form.get('allergies')
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("INSERT INTO USERS (NAME, EMAIL, PASSWORD, GENDER, PHONE_NUMBER, ROLE, STATE) VALUES (?, ?, ?, ?, ?, ?, ?)", (patient_name, patient_name+"@gmail.com",patient_name, gender, contact, "Patient", "Active"))
        con.commit()
        cur.execute("INSERT INTO PATIENTS (PATIENT_NAME, AGE, GENDER, ADDRESS, CONTACT, BLOOD_GRP, ALLERGIES, STATE) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (patient_name, age, gender, address, contact, blood, allergies, "Active" ))
        con.commit()
        con.close()
        return redirect(url_for('patient_list'))
    return render_template('admin/add_patient.html')


@app.route('/editdoc/<int:doc_id>', methods=['GET', 'POST'])
def editdoc(doc_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if request.method == 'POST':
        dept_name= request.form.get('dept_name')
        doc_name = request.form.get('doc_name')
        cur.execute("UPDATE DOCTORS SET DEPT_NAME=?, DOC_NAME=? WHERE DOC_ID=?", (dept_name, doc_name, doc_id))
        con.commit()
        con.close()
        return redirect(url_for('doctor_list'))
    
    cur.execute("SELECT DOC_ID, DEPT_NAME, DOC_NAME FROM DOCTORS WHERE DOC_ID=?", (doc_id,))
    doc = cur.fetchone()
    con.close()
    
    return render_template('admin/editdoc.html', doc={
        'id': doc[0], 'dept_name': doc[1], 'doc_name': doc[2]
    })

@app.route('/blacklistdoc/<int:doc_id>', methods=['POST'])
def blacklistdoc(doc_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("UPDATE DOCTORS SET STATE ='Blacklist' WHERE DOC_ID = ?",(doc_id,))
    con.commit()
    con.close()
    return redirect(url_for('doctor_list'))

@app.route('/deletedoc/<int:doc_id>', methods=['POST'])
def deletedoc(doc_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("DELETE FROM DOCTORS WHERE DOC_ID=?",(doc_id,))
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
        parameter=[]
        values=[]
        patient_name = request.form.get('patient_name')
        if patient_name:
            parameter.append("PATIENT_NAME=?")
            values.append(patient_name)
        age = request.form.get('age')
        if age:
            parameter.append("AGE=?")
            values.append(age)
        gender = request.form.get('gender')
        if gender:
            parameter.append("GENDER=?")
            values.append(gender)
        address = request.form.get('address')
        if address:
            parameter.append("ADDRESS=?")
            values.append(address)
        contact = request.form.get('contact')
        if contact:
            parameter.append("CONTACT=?")
            values.append(contact)
        blood = request.form.get('blood')
        if blood:
            parameter.append("BLOOD_GRP=?")
            values.append(blood)
        allergies = request.form.get('allergies')
        if allergies:
            parameter.append("ALLERGIES=?")
            values.append(allergies)
        values.append(patient_id)
        if parameter:
            q=f"UPDATE PATIENTS SET {','.join(parameter)} WHERE PATIENT_ID=?"
            cur.execute(q,values)
            con.commit()
        con.close()
        return redirect(url_for('patient_list'))

    cur.execute("SELECT PATIENT_ID, PATIENT_NAME FROM PATIENTS WHERE PATIENT_ID=?", (patient_id,))
    p = cur.fetchone()
    con.close()
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

@app.route('/timeslot', methods=['GET'])
def timeslot():
    uname = request.form.get('doc_name') or session.get('username')
    uid = request.form.get('doc_id') or session.get('userid')
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT DOC_ID, DOC_NAME FROM DOCTORS WHERE DOC_NAME LIKE ?', (f"%{uname}%",))
    res = cur.fetchone() 
    docid, drname = res[0], res[1]
    cur.execute('SELECT DAY, TIME FROM DOC_AVAILABILITY WHERE DOC_ID = ?', (docid,))
    saved_slots = cur.fetchall()
    con.close()
    return render_template('doctor/timeslot.html', drname=drname, docid=docid, saved=saved_slots)

@app.route('/saveslots', methods=['POST'])
def saveslots():
    uname = request.form.get('doc_name') or session.get('username')
    uid = request.form.get('doc_id') or session.get('userid')
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT DOC_ID, DOC_NAME FROM DOCTORS WHERE DOC_NAME LIKE ?', (f"%{uname}%",))
    res = cur.fetchone() 
    docid, drname = res[0], res[1]
    cur.execute('DELETE FROM DOC_AVAILABILITY WHERE DOC_ID = ?', (docid,))

    days = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    for day in days:
        slots = request.form.getlist(f"{day}[]")
        for time in slots:
            cur.execute('''
                INSERT INTO DOC_AVAILABILITY (DOC_ID, DOC_NAME, DAY, TIME, AVAILABILITY)
                VALUES (?, ?, ?, ?, ?)''',
                (docid, drname, day, time, "Available"))

    con.commit()
    con.close()
    return redirect(url_for('timeslot'))

@app.route('/bookappointment', methods=['POST','GET'])
def bookappointment():
    uname = session.get('username')
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT * FROM PATIENTS WHERE PATIENT_NAME LIKE ?', (f"%{uname}%",))
    res = cur.fetchone()
    cur.execute("SELECT DEPT_NAME FROM DEPARTMENTS")
    depttab = cur.fetchall()
    pid=res[0]
    pname=res[1]
    selected_day=""
    selected_time=""
    if request.method=="POST" and request.form.get("dept_name"):
        dept_name = request.form.get("dept_name")
        cur.execute("SELECT DOC_NAME FROM DOCTORS WHERE DEPT_NAME = ? AND STATE='Active'", (dept_name,))
        docnames=cur.fetchall()
        print(docnames)
        return render_template('patient/book.html', profiledet=res, depttab=depttab, docnames=docnames )
    if request.method=="POST" and request.form.get("doc_name"):
        doc_name = request.form.get("doc_name")
        cur.execute("SELECT DAY, TIME FROM DOC_AVAILABILITY WHERE DOC_NAME = ? AND AVAILABILITY='Available'", (doc_name,))
        doctimes=cur.fetchall()
        cur.execute('SELECT DOC_ID FROM DOCTORS WHERE DOC_NAME=?', (doc_name,))
        docid=cur.fetchone()
        session['selected_docid'] = docid[0]
        session['selected_doct'] = doc_name
        return render_template('patient/book.html', profiledet=res, depttab=depttab, doctimes=doctimes )
    if request.method=="POST" and request.form.get("doc_time"):
        doc_time = request.form.get("doc_time")
        day, time = doc_time.split(",")
        selected_day+=day
        selected_time+=time
        selected_docid = session.get('selected_docid')
        selected_doct = session.get('selected_doct')
        cur.execute('''INSERT INTO APPOINTMENTS (PATIENT_ID, PATIENT_NAME, DOC_ID, DOC_NAME, APPOINTMENT_DATE, APPOINTMENT_TIME, STATUS)
                    VALUES(?,?,?,?,?,?,?)''',
                    (pid,pname,selected_docid,selected_doct,selected_day,selected_time,"Booked"))
        con.commit()
        cur.execute("UPDATE DOC_AVAILABILITY SET AVAILABILITY='Not Available' WHERE DOC_ID = ? AND DAY = ? AND TIME = ? ",
                    (selected_docid,selected_day,selected_time))
        con.commit()
    con.close()
    return render_template('patient/book.html', profiledet=res, depttab=depttab)

@app.route('/canceleapp/<int:app_id>', methods=['POST'])
def cancelapp(app_id):
    uname=session.get('username')
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT ROLE FROM USERS WHERE NAME LIKE ?",(f"%{uname}%",))
    role=cur.fetchone()
    cur.execute("UPDATE APPOINTMENTS SET STATUS='Cancelled' WHERE APPOINTMENT_ID=?",(app_id,))
    con.commit()
    cur.execute("SELECT DOC_NAME, APPOINTMENT_DATE, APPOINTMENT_TIME FROM APPOINTMENTS WHERE APPOINTMENT_ID=?",(app_id,))
    res=cur.fetchone()
    doc_name=res[0]
    day=res[1]
    time=res[2]
    cur.execute("UPDATE DOC_AVAILABILITY SET AVAILABILITY='Available' WHERE DOC_NAME=? AND DAY=? AND TIME=?",
                (doc_name,day,time))
    con.commit()
    con.close()
    if role[0]=='Admin':
        return redirect(url_for('admin_dashboard'))
    if role[0]=='Doctor':
        return redirect(url_for('doctor_dashboard'))
    if role[0]=='Patient':
        return redirect(url_for('patient_dashboard'))

@app.route('/updatepatprofile', methods=['POST','GET'])
def updatepatprofile():
    uname = session.get('username')
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT * FROM PATIENTS WHERE PATIENT_NAME LIKE ?', (f"%{uname}%",))
    res = cur.fetchone()
    con.close()
    return render_template('patient/profile.html', profiledet=res)


@app.route('/editpatprofile/<int:patient_id>', methods=['POST','GET'])
def editpatprofile(patient_id):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM PATIENTS WHERE PATIENT_ID=?", (patient_id,))
    patient = cur.fetchone()
    if request.method == 'POST':
        parameter = []
        values = []

        patient_name = request.form.get('patient_name')
        if patient_name:
            parameter.append("PATIENT_NAME=?")
            values.append(patient_name)

        age = request.form.get('age')
        if age:
            parameter.append("AGE=?")
            values.append(age)

        gender = request.form.get('gender')
        if gender:
            parameter.append("GENDER=?")
            values.append(gender)

        address = request.form.get('address')
        if address:
            parameter.append("ADDRESS=?")
            values.append(address)

        contact = request.form.get('contact')
        if contact:
            parameter.append("CONTACT=?")
            values.append(contact)

        blood = request.form.get('blood')
        if blood:
            parameter.append("BLOOD_GRP=?")
            values.append(blood)

        allergies = request.form.get('allergies')
        if allergies:
            parameter.append("ALLERGIES=?")
            values.append(allergies)

        values.append(patient_id)

        if parameter:
            q = f"UPDATE PATIENTS SET {','.join(parameter)} WHERE PATIENT_ID=?"
            cur.execute(q, values)
            con.commit()

        con.close()
        return redirect(url_for('updatepatprofile'))
    con.close()
    return render_template('patient/editprofile.html', patient=patient)

@app.route('/treatment', methods=['GET', 'POST'])
def treatment():
    if request.method == 'POST':
        appointment_id= request.form.get('appointment_id')
        patient_name = request.form.get('patient_name')
        uname = session.get('username')
        con = sqlite3.connect(database)
        cur = con.cursor()
        cur.execute("SELECT DOC_NAME FROM DOCTORS WHERE DOC_NAME LIKE ?",(f"%{uname}%",))
        docname=cur.fetchone()
        print("Doc name is", docname[0])
        diagnosis = request.form.get('diagnosis')
        treatment = request.form.get('treatment')
        presc = request.form.get('presc')

        if not diagnosis:
            return render_template('doctor/treatment.html', patient_name=patient_name, appointment_id=appointment_id)

        cur.execute('''INSERT INTO TREATMENTS (PATIENT_NAME, DOC_NAME, DIAGNOSIS, TREATMENT, PRESCRIPTION)
                    VALUES(?,?,?,?,?)''',
                    (patient_name,docname[0],diagnosis,treatment,presc))
        con.commit()
        cur.execute("UPDATE APPOINTMENTS SET STATUS='Completed' WHERE APPOINTMENT_ID=?",(appointment_id,))
        con.commit()
        con.close()
        return redirect(url_for('doctor_dashboard'))

@app.route('/history', methods=['GET'])
def history():
    uname = session.get('username')
    print("UNAME IS",uname)
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('SELECT TREATMENT_ID, DOC_NAME, DIAGNOSIS, TREATMENT, PRESCRIPTION FROM TREATMENTS WHERE PATIENT_NAME LIKE ?',(f"%{uname}%",))
    his=cur.fetchall()
    print("HIS VALUE IS",his)
    return render_template('patient/history.html', his=his)

@app.route('/patient_history')
def patient_history():
    pname=request.args.get('pname')
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('''SELECT TREATMENT_ID, DOC_NAME, DIAGNOSIS, TREATMENT, PRESCRIPTION FROM TREATMENTS WHERE PATIENT_NAME=?''',
                (pname,))
    his=cur.fetchall()
    return render_template('doctor/history.html', his=his)

@app.route('/reschedule/<int:app_id>', methods=['GET', 'POST'])
def reschedule(app_id):
    con = sqlite3.connect(database)
    cur = con.cursor()

    if request.method == "POST" and "new_day_time" in request.form:
        doc_name = request.form.get("docname")
        print("first print",doc_name)

        old_date = request.form.get("old_day")
        old_time = request.form.get("old_time")

        print("OLD DATE:", old_date)
        print("OLD TIME:", old_time)

        new_day, new_time = request.form.get("new_day_time").split(",")
        print("NEW DATE:", new_day, "| NEW TIME:", new_time)

        cur.execute("""
            UPDATE APPOINTMENTS
            SET APPOINTMENT_DATE = ?, APPOINTMENT_TIME = ?
            WHERE APPOINTMENT_ID = ?
        """, (new_day, new_time, app_id))
        con.commit()

        cur.execute("""
            UPDATE DOC_AVAILABILITY
            SET AVAILABILITY = 'Available'
            WHERE DOC_NAME = ? AND DAY = ? AND TIME = ?
        """, (doc_name, old_date, old_time))
        con.commit()

        cur.execute("""
            UPDATE DOC_AVAILABILITY
            SET AVAILABILITY = 'Not Available'
            WHERE DOC_NAME = ? AND DAY = ? AND TIME = ?
        """, (doc_name, new_day, new_time))

        con.commit()
        con.close()
        return redirect(url_for('patient_dashboard'))

    elif request.method == "POST":
        doc_name = request.form.get('docname')
        old_date = request.form.get('day')
        old_time = request.form.get('time')

        print("➡ FIRST POST:", doc_name, old_date, old_time)

    else:
        return redirect(url_for('patient_dashboard'))

    cur.execute("""
        SELECT DAY, TIME
        FROM DOC_AVAILABILITY
        WHERE DOC_NAME = ? AND AVAILABILITY='Available'
    """, (doc_name,))
    available = cur.fetchall()
    con.close()
    return render_template("patient/reschedule.html", app_id=app_id, doc_name=doc_name, old_date=old_date, old_time=old_time, available=available)




if __name__ == "__main__":
    app.run(debug=True)
