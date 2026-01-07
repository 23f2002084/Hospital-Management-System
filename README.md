# Hospital-Management-System - IITM
MAD 1 PROJECT

Hospitals need efficient systems to manage patients, doctors, appointments, and treatments. Currently, many hospitals use manual registers or disconnected software, which makes it difficult to manage records, avoid scheduling conflicts, and track patient history.

Frameworks Used :

Flask for application back-end
Jinja2 templating, HTML, CSS and Bootstraps for application front-end
SQLite for database

Roles & Functionalities :

  Admin functionalities:
      1. Admin dashboard must display total number of doctors, patients, and appointments.
      2. Admin should pre-exist in the app i.e. it must be created programmatically after the creation of the database. [No admin registration allowed]
      3. Admin can add/update doctor profiles.
      4. Admin can view all upcoming and past appointments.
      5. Admin can search for patients or doctors and view their details.
      6. Admin can edit doctor details such as name, specialization etc., and also patient info if needed.
      7. Admin can remove/blacklist doctors and patients from the system.
      
  Doctor functionalities:
      1. Doctor’s dashboard must display upcoming appointments for the day/week.
      2. Doctor’s dashboard must show list of patients assigned to the doctor.
      3. Doctor's dashboard must have the option to mark appointments as Completed or Cancelled.
      4. Doctors can provide their availability for the next 7 days.
      5. Doctors can update patient treatment history like provide diagnosis, treatment and prescriptions.
      
  Patient functionalities:
      1. Patients can register and login themselves on the app.
      2. Patients’ Dashboard must display all available specialization/departments
      3. Patients’ Dashboard must display availability of doctors for the coming 7 days (1 week) and patients can read doctors profiles.
      4. It must display upcoming appointments and their status.
      5. It must show past appointment history with diagnosis and prescriptions.
      6. Patients can edit their profile.
      7. Patients can book as well as cancel appointments with doctors.
  
  Other core functionalities:
      1. Prevent multiple appointments at the same date and time for the same doctor.
      2. Update appointment status dynamically (Booked → Completed → Cancelled).
      3. Admin and Patient should be able to search for a specialization or by a doctor’s name
      4. Admin should be able to search patients by name, ID, or contact information.
      5. Store all completed appointment records for each patient.
      6. Include diagnosis, prescriptions, and doctor notes for each visit.
      7. Allow patients to view their own treatment history.
      8. Allow doctors to view the full history of their patients for informed consultation.

Screenshots:

  Admin's Dashboard:
  <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/375edf73-d3a8-4295-a13a-1d17fedb2019" />
  <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/ce1a9338-08b4-49ea-a2bc-9f5bca579299" />
  <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/c46cc497-544d-40cb-b526-93ee938cbaba" />
  <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/cea21f17-eb3e-4804-8bfa-e92796359d45" />

  Doctor's Dashboard:
  <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/824d9a0e-5732-4384-93dd-0aa988560df8" />

  Patient's Dashboard:
  <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/e9db05e1-d2c7-405e-894d-1864244063f3" />
  <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/44c964af-70f7-470d-a23e-f831db75db6b" />
  <img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/9bd90444-f5c8-45ef-b4bb-968daf731bba" />








