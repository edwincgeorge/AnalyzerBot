import json
import glob
import csv
import sys
import os

BASE_DIR = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

# ---------- HELPERS ----------

def extract_username(href):
    parts = href.strip().split("/")
    return parts[-1] if parts[-1] else parts[-2]

def clean(username):
    return username.strip().lower()

def is_valid(username):
    return username and not username.startswith("__deleted__")


# ---------- LOAD FOLLOWING ----------

with open(os.path.join(BASE_DIR, "following.json"), "r", encoding="utf-8") as f:
    following_data = json.load(f)

following = {}

for entry in following_data.get("relationships_following", []):
    for item in entry.get("string_list_data", []):
        href = item.get("href", "")
        username = clean(extract_username(href))

        if is_valid(username):
            following[username] = {
                "username": username,
                "profile_url": href,
                "timestamp": item.get("timestamp", "")
            }


# ---------- LOAD FOLLOWERS ----------

followers = {}

for file in glob.glob(os.path.join(BASE_DIR, "followers_*.json")):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        data = data.get("relationships_followers", [])

    for entry in data:
        for item in entry.get("string_list_data", []):
            href = item.get("href", "")
            username = clean(extract_username(href))

            if is_valid(username):
                followers[username] = {
                    "username": username,
                    "profile_url": href,
                    "timestamp": item.get("timestamp", "")
                }


# ---------- COMPARE ----------

not_following_back = {
    uname: info
    for uname, info in following.items()
    if uname not in followers
}


# ---------- SAVE CSV ----------

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["username", "profile_url", "followed_on"])
    writer.writeheader()

    for info in sorted(not_following_back.values(), key=lambda x: x["username"]):
        writer.writerow({
            "username": info["username"],
            "profile_url": info["profile_url"],
            "followed_on": info["timestamp"]
        })