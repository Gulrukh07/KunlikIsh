
---

# 🤖 KunlikIsh – Telegram Bot for Daily Job Matching

**KunlikIsh** is a Telegram bot developed with `Python` and `Aiogram`, designed to connect **daily workers** with **customers** looking for short-term services like cleaning, construction, repair, and more. The platform allows job posting, admin approval, and streamlined worker-customer interaction — all within Telegram.

![KunlikIsh Banner](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Relational%20DB-blue?logo=postgresql)


---

## 🚀 Features

* 🔐 Admin-based job approval system
* 🧰 Custom roles: Customers, Workers, Admins
* 📥 Job request form for customers
* 📤 Daily job listings sent to workers
* 📂 Job history and tracking
* 🛠 Built using Python + Aiogram (Telegram Bot Framework)
* 🧾 Local database support using PostgreSql


---

## 🛠 Tech Stack

| Technology   | Purpose |
|--------------| - |
| Python 3.12+ | Backend Logic |
| Aiogram 3.x  | Telegram Bot Framework |
| PostgreSQl   | Robust relational database|
| `.env`       | Secrets management |

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Gulrukh07/KunlikIsh.git
cd KunlikIsh
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the following:

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_IDS=123456789  # comma-separated if multiple
```

### 5. Run the Bot

```bash
python main.py
```

---

## 📁 Project Structure

```
KunlikIsh/
│
├── bot/                # Core bot logic
│   ├── handlers/       # Command and message handlers
│   ├── keyboards/      # Inline and reply markup keyboards
│   ├── filters/        # Custom filters (e.g., is_admin)
│   ├── services/       # Business logic (e.g., job approval)
│   ├── middlewares/    # Middleware for logging, etc.
│   ├── models/         # Database models
│   └── utils/          # Utility functions
│
├── main.py             # Entrypoint
├── config.py           # Bot configuration loader
├── requirements.txt    # Python dependencies
└── .env.example        # Example .env file
```

---

## 👤 User Roles

* **Admin**: Approves job posts and manages the bot
* **Customer**: Submits job listings
* **Worker**: Receives daily job notifications and can apply for jobs

---

## ✅ To-Do / Improvements

* [ ] Add payment system for job listings
* [ ] Admin dashboard (web-based)
* [ ] Statistics and reporting for admins

---


## 🙋‍♀️ Author

**Gulrukh Khayrullaeva**
🔗 GitHub: [@Gulrukh07](https://github.com/Gulrukh07)

