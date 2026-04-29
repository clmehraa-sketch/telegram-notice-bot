import requests
from bs4 import BeautifulSoup
import time
import telegram
from flask import Flask
import threading
import os

TOKEN = "8795217786:AAGN7jzyPv-rHISq87r2pyU-fgEgVcxaPJQ"
CHAT_ID = "-1003980509745"

URLS = [
    "https://rpsc.rajasthan.gov.in/syllabus",
    "https://rpsc.rajasthan.gov.in/results",
    "https://rpsc.rajasthan.gov.in/advertisements",
    "https://rpsc.rajasthan.gov.in/news",
    "https://rssb.rajasthan.gov.in/news",
    "https://rssb.rajasthan.gov.in/results",
    "https://rssb.rajasthan.gov.in/answerkeys",
    "https://rssb.rajasthan.gov.in/advertisements",
    "https://rssb.rajasthan.gov.in/oldpapers",
    "https://rssb.rajasthan.gov.in/examscheme"
]

bot = telegram.Bot(token=TOKEN)
sent_links = set()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def check_updates():
    global sent_links

    for url in URLS:
        try:
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, "html.parser")

            links = soup.find_all("a")

            for link in links:
                href = link.get("href")

                if href and ".pdf" in href:
                    if href.startswith("http"):
                        full_link = href
                    else:
                        full_link = url + href

                    if full_link not in sent_links:
                        message = f"📢 New PDF Found:\n{full_link}"

                        bot.send_message(
                            chat_id=CHAT_ID,
                            text=message
                        )

                        print("Sent:", full_link)

                        sent_links.add(full_link)

        except Exception as e:
            print("Error:", e)

def run_bot():
    print("Bot started... Checking immediately")

    check_updates()

    while True:
        check_updates()
        time.sleep(600)

# Run bot in background thread
threading.Thread(target=run_bot).start()

# Start web server (for Render free plan)
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
