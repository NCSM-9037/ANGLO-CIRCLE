from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai, os, random

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_KEY")


# ---------- AI FUNCTION ----------
def ask_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# ---------- PASTE YOUR BOT FUNCTION HERE ----------
@app.route("/bot", methods=["POST"])
def bot():

    msg = request.form.get("Body").lower().strip()
    resp = MessagingResponse()

    # ---------------- WELCOME ----------------
    if msg in ["hi", "hello", "hey", "start"]:
        reply = """👋 Hello, I am a Grammar Bot
Created by Anglo Circle (2026–27)
📍 MHS Edupark

Type 'help' to see commands 😊
"""

    # ---------------- HELP ----------------
    elif msg == "help":
        reply = """📘 HOW TO USE

correct <sentence>
meaning <word>
daily
quiz
about
credit
"""

    # ---------------- ABOUT ----------------
    elif msg == "about":
        reply = "This is an AI-powered English Grammar Assistant."

    # ---------------- CREDIT ----------------
    elif msg == "credit":
        reply = "Developed by Anglo Circle English Club | Secretary: Rashid"

    # ---------------- FEATURES ----------------
    elif msg.startswith("correct"):
        reply = ask_ai(f"Correct grammar and explain simply with Malayalam: {msg}")

    elif msg.startswith("meaning"):
        reply = ask_ai(f"Meaning + Malayalam meaning: {msg}")

    elif msg == "daily":
        word = random.choice(["Serene","Resilient","Gratitude","Eloquent"])
        reply = ask_ai(f"Explain meaning of {word} with Malayalam")

    elif msg == "quiz":
        reply = "Quiz: He ___ to school daily (go/goes)"

    else:
        reply = "Type 'help' to see commands 😊"

    resp.message(reply)
    return str(resp)


# ---------- START SERVER ----------
if __name__ == "__main__":
    app.run()
