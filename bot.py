import asyncio
import random
from telegram import Bot
from flask import Flask
import os

app = Flask(__name__)

TOKEN = os.environ.get("TOKEN")
CHAT_ID = int(os.environ.get("CHAT_ID"))

equipes = [
    "Real Madrid", "Barcelona",
    "Manchester City", "Liverpool",
    "PSG", "Bayern Munich",
    "Arsenal", "Juventus",
    "Inter", "AC Milan"
]

def analyse_match(home, away):
    xg_home = round(random.uniform(0.8, 2.5), 2)
    xg_away = round(random.uniform(0.5, 2.0), 2)
    total_xg = round(xg_home + xg_away, 2)

    prob_over25 = min(int((total_xg / 2.5) * 50), 95)
    prob_btts = min(int(((xg_home + xg_away) / 2.5) * 50), 90)

    return f"""
⚽ {home} vs {away}
xG : {xg_home} - {xg_away}
Total xG : {total_xg}
Over 2.5 : {prob_over25}%
BTTS : {prob_btts}%
"""

async def envoyer():
    random.shuffle(equipes)
    matchs = []

    for i in range(0, 10, 2):
        matchs.append(analyse_match(equipes[i], equipes[i+1]))

    message = "📊 ANALYSE DU JOUR\n\n" + "\n".join(matchs)

    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

@app.route("/")
def home():
    asyncio.run(envoyer())
    return "Message envoyé !"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
