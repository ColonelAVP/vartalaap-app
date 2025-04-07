
# 🧠 Vartalaap — A Django-Based Q&A Platform

🎥 [Watch Demo](https://drive.google.com/file/d/1ErqMI1MIogddhA7n1nA6zqklh6MNIv2m/view?usp=sharing)

Vartalaap is a simple, functional Q&A web app inspired by Quora. Built using Django, it allows users to register, post questions, answer others, and engage with content in a clean, minimalist interface.

---

## 🚀 Features

### 👤 User Management
- Custom user model with:
  - Username, first/last name, gender, bio
- Login / Logout / Registration
- User profile page with editable personal info

### 📝 Questions
- Ask a question
- View all questions on dashboard
- Like/unlike questions
- Edit/delete own questions
- View timestamps (created & updated)

### 💬 Answers
- Answer any question from the detail page
- Edit/delete own answers
- View others' answers (readonly on dashboard)
- Timestamp on each answer

### 🗨️ Comments
- View comments under each answer
- Comment editing is currently disabled for simplicity
- Timestamp on each comment

### 📋 Dashboard
- List of all questions
- Quick like toggle on questions
- Sorting: recent, most liked, most answered
- Link to question detail page for deep engagement

### 🔍 Question Detail Page
- Full question + all answers + comments
- Submit answer form
- Edit/delete buttons for own content
- Clean, nested display layout

### 🧑‍💼 Profile Page
- View user’s questions & answers
- Edit bio, gender, and name if it’s your own profile

### 🛠 Admin Panel
- View/search questions, answers, comments
- Easily manage user content from backend

---

## 🧱 Tech Stack

- **Backend:** Django 4+
- **Frontend:** HTML5, CSS3 (vanilla, clean, mobile-friendly)
- **Database:** SQLite (can be swapped for Postgres/MySQL easily)
- **Templating:** Django Templates
- **Auth:** Django built-in login + custom user

---

## ⚙️ Setup Instructions

### 🔧 1. Clone & Install

```bash
git clone https://github.com/ColonelAVP/vartalaap-app.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
