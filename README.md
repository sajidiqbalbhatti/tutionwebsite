# 📚 Acadexa – Smart Tuition Platform (Home, Academy & Online Tuition)

A professional-level **Acadexa Tuition Management System** built with Django. This platform supports **Online Tuition**, **Home Tuition**, and **Academy-based Tuition** services. It manages multiple user roles—**Admin**, **Tutor**, **Student**, and **Parent**—with separate dashboards, course management, assignment submissions, and real-time notifications.

---

## 🚀 Live Demo

🌐 [Live on PythonAnywhere](https://sajiddev.pythonanywhere.com/)  
💻 [GitHub Repository](https://github.com/sajidiqbalbhatti/tutionwebsite.git)

---

## 📌 Features

### 🔐 Authentication & Roles
- User registration, login, logout  
- Role-based access: **Admin**, **Tutor**, **Student**, **Parent**  
- Custom profile creation for Tutors and Students  

### 🎓 Tutor Module
- Create and manage tuition courses (online, home, academy)  
- Upload assignments and learning material  
- View enrolled students  
- Receive real-time notifications  

### 👨‍🎓 Student Module
- Enroll in courses (online/home/academy)  
- View and submit assignments  
- Get notified about course updates and deadlines  

### 🛠 Admin Module
- View system-wide statistics  
- Monitor course, tutor, and assignment activities  
- Track student enrollments and submissions  

### 🔔 Notification System
- Tutors notified on login and content actions  
- Students notified on course and assignment updates  
- Admin notified on user actions and submissions  

### 📊 Dashboards
- **Admin Dashboard** – User stats, activity logs, system overview  
- **Tutor Dashboard** – Courses, student list, content uploads  
- **Student Dashboard** – Enrollments, assignment submissions, alerts  

### 🖥️ Frontend
- Responsive UI using Bootstrap/Tailwind CSS  
- Role-specific, clean user interfaces  

### ⚙️ Deployment
- Live on PythonAnywhere  
- GitHub Integrated  
- Docker-ready (future support)

---

## 🔧 Tech Stack

- **Backend**: Django (Python 3.12+)  
- **Frontend**: HTML, CSS, Bootstrap / Tailwind  
- **Database**: SQLite (development) / MySQL (production)  
- **Deployment**: PythonAnywhere, Docker  
- **Version Control**: Git + GitHub  

---

## 🧱 Django Apps Overview

- `users/` – Authentication and role-based management  
- `students/` – Student dashboards, course enrollments, submissions  
- `tutors/` – Tutor dashboards, course and assignment management  
- `courses/` – Course listing and enrollment logic  
- `assignments/` – Assignment creation, uploads, and submission  
- `notifications/` – Notification logic for all roles  

---



## ⚙️ Setup Instructions

Follow these steps to run the project locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/sajidiqbalbhatti/tutionwebsite.git
   cd tutionwebsite

2. **Create a virtual environment**

   python -m venv env

3. **Activate the virtual environment**

   On macOS/Linux:

   source env/bin/activate

   On Windows:

   env\Scripts\activate

4. **Install dependencies**
  
   pip install -r requirements.txt

5. **Apply database migrations**

   python manage.py migrate

6. **Create a superuser (for admin access)**
  
   python manage.py createsuperuser



   


