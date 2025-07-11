# 🤖 KunlikIsh – Telegram Bot for Daily Job Matching

**KunlikIsh** is a Telegram bot developed in Python using `aiogram`. It connects **daily workers** with **customers** who are looking to get tasks done — such as cleaning, repairs, delivery, and more.

Customers can submit job requests, which are then **reviewed by an admin**. Once approved, the job listings are **shared with workers** through the bot. This helps simplify and automate the local gig job process.

---

## 🧩 Key Features

### 👥 For Customers:
- 📝 Submit job requests through Telegram form
- 📸 Optionally upload job details or photos
- ⏳ Wait for admin approval
- ✅ Get notified when job is approved and shared

### 🛠️ For Workers:
- 📬 Receive approved job postings instantly
- 🔎 View job description, location, and pay
- 📞 Contact customer directly (or through bot if anonymized)

### 🧑‍💼 For Admin:
- 📥 Review and approve/reject job submissions
- 🗂 Maintain job queue
- 📊 Monitor system usage (basic logs/notifications)

---

## 🛠 Tech Stack

- **Language**: Python 3
- **Framework**: [aiogram](https://github.com/aiogram/aiogram) – Fast & async Telegram Bot API
- **Database**: SQLite (easily replaceable with PostgreSQL)
- **Storage**: Files, optional image handling (via Telegram API)
- **Env Management**: `.env` for secrets

---

## 🔧 Project Structure

KunlikIsh/
├── bot.py # Bot entry point
├── handlers/ # Separate logic for users, workers, admin
│ ├── customer.py
│ ├── worker.py
│ └── admin.py
├── database.py # SQLite queries for jobs and users
├── keyboards.py # Inline and reply markup
├── config.py # Token and config loading
├── utils.py # Helper functions (formatting, filtering)
├── .env # Contains BOT_TOKEN and admin IDs
├── requirements.txt
└── README.md

yaml
Always show details

Copy



## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Gulrukh07/KunlikIsh.git
cd KunlikIsh
2. Set Up Environment
bash
Always show details

Copy
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
3. Add Your Telegram Bot Token
Create a .env file in the root directory and include:

ini
Always show details

Copy
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
4. Run the Bot
bash
Always show details

Copy
python bot.py
```
### ⚙️ How It Works
- Customer submits a job request

- Admin receives the form and approves or rejects

- If approved, the job is automatically shared with all registered workers

- Workers can view jobs and respond accordingly

### ✅ Future Improvements
- ⏰ Scheduled job expiration

- 📍 Geolocation filtering (jobs by region or city)

- 💬 In-bot communication bridge (worker ↔ customer)

- 📊 Admin dashboard (Telegram or web-based)


### 🙋‍♀️ Author
Gulrukh Khayrullaeva
Python Backend & Bot Developer
🔗 

