from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
import sqlite3

app = Flask(__name__)

# ==============================
# OpenAI Key (from Render env)
# ==============================
openai.api_key = os.getenv("OPENAI_KEY")


# ==============================
# DATABASE (auto creates chat.db)
# ==============================
conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages(
    phone TEXT,
    role TEXT,
    content TEXT
)
""")
conn.commit()


def save_msg(phone, role, content):
    cursor.execute(
        "INSERT INTO messages VALUES (?, ?, ?)",
        (phone, role, content)
    )
    conn.commit()


def load_history(phone):
    cursor.execute(
        "SELECT role, content FROM messages WHERE phone=? ORDER BY rowid DESC LIMIT 10",
        (phone,)
    )
    rows = cursor.fetchall()
    return rows[::-1]


# ==============================
# OpenAI Chat
# ==============================
def ask_ai(messages):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content


# ==============================
# BOT ROUTE
# ==============================
@app.route("/bot", methods=["POST"])
def bot():

    user_msg = request.form.get("Body")
    phone = request.form.get("From")

    resp = MessagingResponse()

    history = load_history(phone)

    messages = [{
        "role": "system",
        "content": """
You are an English Teacher.

Rules:
- ONLY teach English
- Correct grammar
- Teach vocabulary
- Explain simply
- Give Malayalam meanings when useful
- If user asks unrelated topics, redirect to English learning politely
"""
    }]

    # add history
    for role, content in history:
        messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_msg})

    reply = ask_ai(messages)

    # save to DB
    save_msg(phone, "user", user_msg)
    save_msg(phone, "assistant", reply)

    resp.message(reply)
    return str(resp)


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    app.run()
