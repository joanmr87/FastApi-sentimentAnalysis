import os
import urllib.parse
from typing import List
from email.message import Message

from fastapi import FastAPI
from pydantic import BaseModel

from utils import get_credentials, connect_to_mail_server, fetch_emails, format_email_contents
from models import SentimentRequest, SentimentResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Sentiment Analysis API!"}

@app.post("/sentiment_analysis", response_model=SentimentResponse)
async def sentiment_analysis(request: SentimentRequest):
    user, password = get_credentials()
    mail = connect_to_mail_server(os.getenv("IMAP_URL"), user, password)
    emails = fetch_emails(mail, request.fromTimestamp, request.toTimestamp)
    results = []
    for email_message in emails:
        email_contents = format_email_contents(email_message)
        text = email_contents.translate(str.maketrans('', '', '\n\t\r'))
        text_blob = TextBlob(text)
        polarity = text_blob.sentiment.polarity
        subject = email_message["subject"]
        results.append({"subject": subject, "polarity": polarity})
    return {"results": results}
