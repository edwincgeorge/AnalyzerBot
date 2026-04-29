import json
import os
import requests
import subprocess
import shutil

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

WEBHOOK_URL = "https://analyzer-bot.vercel.app/api"

user_sessions = {}

def send_welcome(chat_id):
    message = (
        "🚀 *Instagram Non-Following-Back Finder Bot*\n\n"

        "📥 *How to use:*\n"
        "1. Go to Instagram → Settings → Accounts Center\n"
        "2. Download your account data\n"
        "3. Select *Followers & Following* data ONLY\n"
        "4. Extract the ZIP file\n\n"

        "📤 *Upload:*\n"
        "• following.json\n"
        "• followers_*.json\n\n"

        "⚙️ Bot will:\n"
        "• Analyze your data\n"
        "• Find non-followers\n"
        "• Send CSV 📄\n\n"

        "━━━━━━━━━━━━━━━\n"
        "💻 *Developed by Edwin* ✨\n"
        "🔗 https://github.com/edwincgeorge/AnalyzerBot\n"
        "⚡ Smart • Fast • Clean\n"
        "━━━━━━━━━━━━━━━"
    )

    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    })
    
def ensure_webhook():
    try:
        r = requests.get(f"{API}/getWebhookInfo").json()
        current_url = r.get("result", {}).get("url")

        if current_url != WEBHOOK_URL:
            requests.get(f"{API}/setWebhook", params={"url": WEBHOOK_URL})
    except:
        pass


def app(environ, start_response): 

    ensure_webhook()

    try:
        request_method = environ["REQUEST_METHOD"]

        if request_method != "POST":
            start_response("200 OK", [("Content-Type", "text/plain")])
            return [b"OK"]

        try:
            request_body = environ["wsgi.input"].read()
            data = json.loads(request_body)
        except:
            start_response("200 OK", [("Content-Type", "text/plain")])
            return [b"Invalid"]

        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")

        if "document" not in message:
            if chat_id:
                send_welcome(chat_id)

            start_response("200 OK", [("Content-Type", "text/plain")])
            return [b"OK"]

        doc = message["document"]
        filename = doc["file_name"]
        file_id = doc["file_id"]

        if chat_id not in user_sessions:
            user_sessions[chat_id] = {
                "has_following": False,
                "followers": 0
            }

        session = user_sessions[chat_id]

        user_dir = f"/tmp/{chat_id}"
        os.makedirs(user_dir, exist_ok=True)

        # Get file
        file_info = requests.get(f"{API}/getFile", params={"file_id": file_id}).json()
        file_path = file_info["result"]["file_path"]

        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        local_path = os.path.join(user_dir, filename)

        with open(local_path, "wb") as f:
            f.write(requests.get(file_url).content)

        if filename == "following.json":
            session["has_following"] = True

        elif filename.startswith("followers_") and filename.endswith(".json"):
            session["followers"] += 1

        else:
            send_message(chat_id, "Invalid file")
            start_response("200 OK", [])
            return [b"OK"]

        if session["has_following"] and session["followers"] > 0:
            send_message(chat_id, "Processing your data 🚀...")

            output_file = os.path.join(user_dir, "result.csv")

            subprocess.run(
                ["python", "test.py", user_dir, output_file],
                check=True
            )

            send_document(chat_id, output_file)

            shutil.rmtree(user_dir)
            del user_sessions[chat_id]

    except Exception as e:
        send_message(chat_id, f"Error: {str(e)}")

    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"OK"]


def send_message(chat_id, text):
    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })


def send_document(chat_id, file_path):
    with open(file_path, "rb") as f:
        requests.post(
            f"{API}/sendDocument",
            data={"chat_id": chat_id},
            files={"document": f}
        )
