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
    date = email_message["Date"]
    to = email_message["To"]
    sender = email_message["From"]
    content_type = email_message.get_content_type()
    content_transfer_encoding = email_message["Content-Transfer-Encoding"]
    body = b""
    for part in email_message.walk():
        if part.get_content_type() == 'text/plain':
            body += part.get_payload(decode=True)

    if body:
        text = body + subject.encode('utf-8')
        decoded_text = urllib.parse.unquote(text.decode('utf-8'))
        cleaned_text = decoded_text.replace('\r', '').replace('\n', '')
        texts.append(cleaned_text)
    
    return {
        "message_id": message_id,
        "date": date,
        "to": to,
        "from": sender,
        "subject": subject,
        "content_type": content_type,
        "content_transfer_encoding": content_transfer_encoding,
        "texts": texts
    }

if __name__ == "__main__":
    user, password = get_credentials()
    mail = connect_to_mail_server('imap.gmail.com', user, password)
    for email_message in fetch_emails(mail):
        contents = format_email_contents(email_message)
        print(contents)


    emails = ['hate you', 'love you','te odio']
    now = datetime.datetime.now()
    results = {"reportGeneratedDate": now.strftime("%Y-%m-%d %H:%M:%S"),
               "extractedEmail": sentiment_request.email,
               "status": "succeeded",
               "emails": []}

    for email in emails:
        email_cleaned = email_cleaning(email)
        polarity_scores = cal_polarity(email_cleaned)

        email_result = {"emailSentDate": "2023-03-03 00:00:00",
                        "sentences": []}

        for polarity_score in polarity_scores:
            sentence_result = {"polarityScore": polarity_score}
            email_result["sentences"].append(sentence_result)

        results["emails"].append(email_result)

    return results

def email_cleaning(email):
    clean_email = re.sub(r"@[a-zA-Z0-9]+", "", email)
    clean_email = re.sub(r"<.*?>", "", clean_email)
    clean_email = ' '.join(
        word for word in clean_email.split() if word not in stp_words)
    return clean_email


def cal_polarity(email):
    polarity_scores = []
    for sentence in TextBlob(email).sentences:
        polarity_scores.append(sentence.sentiment.polarity)
    return polarity_scores
