# 🎉 Event Management System (Django Project)

A professional, full-stack Event Management Web Application built using Django. It allows users to create, manage, and RSVP to events, with role-based access control, user authentication, profile management, email functionality, and a responsive UI.

---

## 🚀 Features

### 👥 User Management
- Custom user model with email authentication
- Role-based access (Admin / Organizer / General User)
- Profile update and image upload
- Password change & reset with email verification

### 📅 Event System
- Create, update, and delete events (Admin/Organizer)
- Event listing with detailed view
- RSVP system: Accept / Decline invitations
- RSVP statistics & dashboard

### 📧 Email Integration
- Email-based password reset
- RSVP email confirmation system

### 💻 UI & Frontend
- Responsive design using Bootstrap 5
- Image upload for events and profiles
- Organized templates and clean layout

---

## 📂 Project Structure

event_management/
├── accounts/ # Authentication, user profile, roles
├── events/ # Event models, RSVP logic
├── templates/ # All HTML templates
├── static/ # CSS, JS, images
├── media/ # Uploaded images
├── manage.py
├── requirements.txt
└── README.md


---

## 💡 Technologies Used

- **Python** 3.10+
- **Django** 5.x
- **SQLite3** (default DB)
- **Bootstrap** 5 for frontend
- **Django Signals & Messages**
- **Email (SMTP) Integration**

---

## ✅ Installation Guide

Follow these steps to run the project locally:

1. **Clone the repository**
   ```bash
   git clone https://github.com/rajibul-shuvo/event-management-system.git
   cd event-management-system

   👤 User Roles
Role  	    Permissions
Admin	    Manage users, events, view RSVP stats
Organizer	Create/update/delete events, view RSVPs
User	    View events, RSVP to events, manage profile


