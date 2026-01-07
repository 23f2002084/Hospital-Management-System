### *Hospital Management System – IITM*

**MAD 1 Project**

<img width="1280" height="640" alt="Narendran" src="https://github.com/user-attachments/assets/6fb7645f-0339-4bea-b356-e9bb76368546" />

---
Project Overview

Hospitals require efficient systems to manage patients, doctors, appointments, and treatments. Many hospitals still rely on manual registers or disconnected software, leading to difficulties in record management, appointment conflicts, and tracking patient history.

This **Hospital Management System (HMS)** is a web-based application designed to streamline hospital operations by providing role-based access for **Admins, Doctors, and Patients**.

---

**Tech Stack :** 

* **Backend:** Flask
* **Frontend:** Jinja2, HTML, CSS, Bootstrap
* **Database:** SQLite

---

**Roles & Functionalities :**

*Admin Functionalities :*

1. View dashboard with total number of doctors, patients, and appointments
2. Admin account is created programmatically (no admin registration allowed)
3. Add and update doctor profiles
4. View all upcoming and past appointments
5. Search for doctors and patients and view their details
6. Edit doctor details (name, specialization, etc.) and patient information
7. Remove or blacklist doctors and patients from the system

---

*Doctor Functionalities :*

1. View upcoming appointments (daily / weekly)
2. View list of patients assigned to the doctor
3. Mark appointments as **Completed** or **Cancelled**
4. Set availability for the next 7 days
5. Update patient treatment history including diagnosis, treatment, and prescriptions

---

*Patient Functionalities :*

1. Register and log in to the application
2. View available specializations/departments
3. View doctor availability for the next 7 days and read doctor profiles
4. View upcoming appointments and their status
5. View past appointment history with diagnosis and prescriptions
6. Edit personal profile details
7. Book and cancel appointments with doctors

---

*Other Core Features :*

1. Prevent multiple appointments for the same doctor at the same date and time
2. Dynamic appointment status updates (**Booked → Completed → Cancelled**)
3. Search doctors by specialization or name (Admin & Patient)
4. Search patients by name, ID, or contact information (Admin)
5. Store all completed appointment records per patient
6. Maintain diagnosis, prescriptions, and doctor notes for every visit
7. Allow patients to view their treatment history
8. Allow doctors to access full patient history for better consultation

---

**Screenshots :**

*Admin Dashboard :*

<img width="1366" height="768" src="https://github.com/user-attachments/assets/375edf73-d3a8-4295-a13a-1d17fedb2019" />
<img width="1366" height="768" src="https://github.com/user-attachments/assets/ce1a9338-08b4-49ea-a2bc-9f5bca579299" />
<img width="1366" height="768" src="https://github.com/user-attachments/assets/c46cc497-544d-40cb-b526-93ee938cbaba" />
<img width="1366" height="768" src="https://github.com/user-attachments/assets/cea21f17-eb3e-4804-8bfa-e92796359d45" />

---

*Doctor Dashboard :*

<img width="1366" height="768" src="https://github.com/user-attachments/assets/824d9a0e-5732-4384-93dd-0aa988560df8" />

---

*Patient Dashboard :*

<img width="1366" height="768" src="https://github.com/user-attachments/assets/e9db05e1-d2c7-405e-894d-1864244063f3" />
<img width="1366" height="768" src="https://github.com/user-attachments/assets/44c964af-70f7-470d-a23e-f831db75db6b" />
<img width="1366" height="768" src="https://github.com/user-attachments/assets/9bd90444-f5c8-45ef-b4bb-968daf731bba" />


