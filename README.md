# 🚀 Instagram Non-Followers Finder Bot

A Telegram bot that analyzes your Instagram data and finds users who **don’t follow you back**, then sends the result as a CSV file.

---

## ✨ Features

* 📥 Accepts Instagram data files directly via Telegram
* ⚡ Automatically processes uploads (no commands needed)
* 📊 Generates a clean CSV of non-followers
* 🔒 Secure token handling using environment variables
* ☁️ Deployable on serverless platforms like Vercel

---

## 🧠 How It Works

1. User downloads Instagram data (**Followers & Following only**)
2. Uploads:

   * `following.json`
   * `followers_*.json`
3. Bot:

   * Parses data
   * Compares followers vs following
   * Generates `result.csv`
4. Sends CSV back to user 📄

---

## 📥 How to Get Instagram Data

1. Go to Instagram → **Settings**
2. Open **Accounts Center**
3. Click **Download your information**
4. Select:

   * ✅ Followers & Following ONLY
   * ✅ JSON format
5. Download and extract the ZIP

---

## 📤 Usage

1. Open your Telegram bot
2. Send any message or `/start`
3. Upload:

   * `following.json`
   * `followers_*.json` (one or more)
4. Wait for processing
5. Receive CSV with non-followers

---

## 🛠️ Tech Stack

* Python
* Telegram Bot API (via HTTP requests)
* Serverless deployment (Vercel)

---

## 📁 Project Structure

```
project/
│
├── api/
│   └── index.py       # Telegram webhook handler
│
├── gg.py              # Core processing script
├── requirements.txt
```

---

## ⚙️ Setup & Deployment

### 1. Clone Repo

```
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Set Environment Variable

Add your Telegram bot token:

```
BOT_TOKEN=your_telegram_bot_token
```

---

### 4. Deploy on Vercel

* Push project to GitHub
* Import into Vercel
* Add environment variable (`BOT_TOKEN`)
* Deploy

---

### 5. Webhook Setup (Auto)

Webhook is automatically configured on first request.

---

## 🔒 Security Notes

* Never expose your bot token publicly
* Only JSON files are processed
* Temporary files are deleted after execution

---

## ⚠️ Limitations

* Vercel has execution time limits (~10s)
* Not suitable for very large Instagram exports
* Sessions are temporary (serverless environment)

---

## 🚀 Future Improvements

* ZIP upload support (better UX)
* Persistent storage (Redis / DB)
* Deployment on Railway for scalability
* UI enhancements (buttons, progress tracking)

---

## 👨‍💻 Author

**Edwin** ✨
Smart • Fast • Clean

---

## ⭐ Support

If you found this useful, consider starring the repo ⭐
