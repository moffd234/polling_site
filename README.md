# 🗳️ Flask Polling Site

This is a Flask-based polling web application created for my significant other when she needed a simple, accessible site for collecting votes across multiple categories. The application supports dynamic polls, stores results in a SQLite database, and displays aggregated results after each vote.

> ⚠️ The names used in this project have been changed for privacy purposes.

---

## 📋 Features

- ✅ Multiple dynamic poll questions and options  
- ✅ Responsive UI using Bootstrap 5  
- ✅ Vote tracking per session (prevents duplicate votes per poll)  
- ✅ Vote results display with percentage breakdowns  
- ✅ AJAX form submission (no page reload on vote)  
- ✅ SQLite database integration via SQLAlchemy  
- ✅ Easily extensible to add more questions or voters  
- ✅ Deployable to platforms like Render or Heroku  

---

## 🏗️ Technologies

- **Python 3.11+**
- **Flask**
- **Flask-SQLAlchemy**
- **Bootstrap 5 (manual integration)**
- **Gunicorn** (for production WSGI server)
- **Render** (used for deployment)
