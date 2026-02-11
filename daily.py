import os
import random
from twilio.rest import Client
import openai

openai.api_key = os.getenv("OPENAI_KEY")

# ======================
# Random word list
# ======================
words = [
    "Serene",
    "Resilient",
    "Meticulous",
    "Eloquent",
    "Gratitude",
    "Compassion",
    "Diligent"
]

word = random.choice(words)

prompt = f"Explain meaning of {word} with Malayalam meaning and example sentence."

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

meaning = response.choices[0].message.content


# ======================
# Twilio credentials
# ======================
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")

client = Client(account_sid, auth_token)


# ======================
# Student numbers
# ======================
students = [
    "whatsapp:+91XXXXXXXXXX",
    "whatsapp:+91YYYYYYYYYY"
]

for s in students:
    client.messages.create(
        body=f"📘 Daily Vocabulary\n\nWord: {word}\n\n{meaning}",
        from_="whatsapp:+14155238886",
        to=s
    )
