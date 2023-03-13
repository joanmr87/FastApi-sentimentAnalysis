import imaplib
import email 
import email.header
import yaml
import urllib.parse

import datetime
from fastapi import FastAPI
from pydantic import BaseModel

from nltk.corpus import stopwords
from textblob import TextBlob
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')

app = FastAPI()

stp_words = stopwords.words('spanish')


class SentimentRequest(BaseModel):
    fromTimestamp: str
    toTimestamp: str
    email: str

@app.post("/")
def sentiment_analysis(sentiment_request: SentimentRequest):
    # emails = obtenerEmails(fromTimestamp, toTimestamp, email)

    user, password = get_credentials()
    mail = connect_to_mail_server('imap.gmail.com', user, password)
    emails = fetch_emails(mail)
    email_contents = [format_email_contents(email) for email in emails]

    now = datetime.datetime.now()
    results = {"reportGeneratedDate": now.strftime("%Y-%m-%d %H:%M:%S"),
               "extractedEmail": sentiment_request.email,
               "status": "succeeded",
               "emails": []}

    for email_content in email_contents:
        for text in email_content['texts']:
            email_cleaned = email_cleaning(text)
            polarity_scores = cal_polarity(email_cleaned)

            email_result = {"emailSentDate": email_content['date'],
                            "sentences": []}

            for polarity_score in polarity_scores:
                sentence_result = {"polarityScore": polarity_score}
                email_result["sentences"].append(sentence_result)

            results["emails"].append(email_result)

    return results

def get_credentials():
    """
    Read the user and password from a YAML file.

    Args:
        None

    Returns:
        Tuple[str, str]: A tuple containing the user and password.

    """
    with open('credentials.yaml') as f:
        content = f.read()

    credentials = yaml.load(content, Loader= yaml.FullLoader)
    return credentials["user"], credentials["password"]

def connect_to_mail_server(imap_url, user, password):
    """
    Establish a connection to the IMAP server and log in using the provided credentials.

    Args:
        imap_url (str): The URL of the IMAP server.
        user (str): The username for logging in.
        password (str): The password for logging in.

    Returns:
        imaplib.IMAP4_SSL: An IMAP4_SSL connection to the mail server.

    """
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, password)
    return mail

def fetch_emails(mail):
    """
    Fetch all emails in the INBOX folder and yield them one at a time.

    Args:
        mail (imaplib.IMAP4_SSL): An IMAP4_SSL connection to the mail server.

    Raises:
        ValueError: If the mailbox selection fails.

    """
    status, messages = mail.select('INBOX')
    if status != "OK": 
        raise ValueError("Incorrect mail box")

    for i in range(1, int(messages[0]) + 1):
        res, msg = mail.fetch(str(i), '(RFC822)')
        for response in msg:
            if isinstance(response, tuple):
                msg_str = response[1].decode('utf-8')
                yield email.message_from_string(msg_str)

def format_email_contents(email_message):
    """
    Args:
        email_message (email.message.Message): A message object representing an email.

    """
    texts = []
    subject = email_message["subject"]
    message_id = email_message["Message-ID"]
    date = email_message
