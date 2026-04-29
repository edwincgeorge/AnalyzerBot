import json
import os
import requests
import subprocess
import shutil

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

WEBHOOK_URL = "https://your-app.vercel.app/api/webhook"

user_sessions = {}


def ensure_webhook():
    try:
        r = requests.get(f"{API}/getWebhookInfo").json()
        current_url = r.get("result", {}).get("url")

        if current_url != WEBHOOK_URL:
            requests.get(
                f"{API}/setWebhook",
                params={"url": WEBHOOK_URL}
            )
    except:
        pass


# ---------------- MAIN HANDLER ----------------
def handler(request):

    ensure_webhook()

    if request.method != "POST":
        return {"statusCode": 200, "body": "OK"}

    data = json.loads(request.body)

    try:
        message = data.get("message", {})
        chat_id = message.get("chat", {}).get("id")

        if "document" not in message:
            return {"statusCode": 200}

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

        file_info = requests.get(
            f"{API}/getFile",
            params={"file_id": file_id}
        ).json()

        file_path = file_info["result"]["file_path"]

        file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

        local_path = os.path.join(user_dir, filename)

        # Download file
        with open(local_path, "wb") as f:
            f.write(requests.get(file_url).content)

        # Track file type
        if filename == "following.json":
            session["has_following"] = True

        elif filename.startswith("followers_") and filename.endswith(".json"):
            session["followers"] += 1

        else:
            send_message(chat_id, "Invalid file name")
            return {"statusCode": 200}

        if session["has_following"] and session["followers"] > 0:
            send_message(chat_id, "Processing...")

            output_file = os.path.join(user_dir, "result.csv")

            subprocess.run(
                ["python", "gg.py", user_dir, output_file],
                check=True
            )

            send_document(chat_id, output_file)

            shutil.rmtree(user_dir)
            del user_sessions[chat_id]

    except Exception as e:
        send_message(chat_id, f"Error: {str(e)}")

    return {"statusCode": 200}


# ---------------- TELEGRAM HELPERS ----------------

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
