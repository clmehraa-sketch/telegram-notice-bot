import requests
from bs4 import BeautifulSoup
import time
import telegram

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

def check_updates():
    global sent_links
    for url in URLS:
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            links = soup.find_all("a")

            for link in links:
                href = link.get("href")
                if href and ".pdf" in href:
                    full_link = href if href.startswith("http") else url + href

                    if full_link not in sent_links:
                        bot.send_message(
                            chat_id=CHAT_ID,
                            text=f"📢 New PDF Found:\n{full_link}"
                        )
                        sent_links.add(full_link)

        except Exception as e:
            print("Error:", e)

while True:
    check_updates()
    time.sleep(600)
