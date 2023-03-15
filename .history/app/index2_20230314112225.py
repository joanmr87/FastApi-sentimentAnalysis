import datetime
import os
import urllib.parse
from typing import List
from email.message import Message

import email
import email.header
import imaplib
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

import nltk
from nltk.corpus import stopwords
from nltk import download as nltk_download
from nltk import sent_tokenize, word_tokenize, pos_tag
from textblob import TextBlob
from googletrans import Translator
from dotenv import load_dotenv

# Descargar recursos de NLTK
nltk_download('punkt')
nltk_download('stopwords')
nltk_download('averaged_perceptron_tagger')

# Cargar variables de entorno del archivo .env
load_dotenv()

# Inicializar variables y objetos
stp_words = stopwords.words('english')
translator = Translator()
app = FastAPI()

# Definir clase Pydantic para solicitud de análisis de sentimientos
class SentimentRequest(BaseModel):
    fromTimestamp: str
    toTimestamp: str
    email: str

# Definir ruta POST en la raíz del servidor para análisis de sentimientos
@app.post("/")
def sentiment_analysis(sentiment_request: SentimentRequest):

    # Obtener las sentences de los emails 
    emails = 
    now = datetime.datetime.now()
    results = {"reportGeneratedDate": now.strftime("%Y-%m-%d %H:%M:%S"),
               "extractedEmail": sentiment_request.email,
               "status": "succeeded",
               "emails": []}

    for email in emails:
        translated_emails = translator.translate(email, src='es', dest='en').text
        print(translated_emails)
        email_cleaned = email_cleaning(translated_emails)
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
    

    VERB_TAGS = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
    NOUN_TAGS = ['PRP', 'PRP$', 'NN', 'NNS', 'NNP', 'NNPS']

def get_credentials():
    """
    Read the user and password from an environment variable.

    Args:
        None

    Returns:
        Tuple[str, str]: A tuple containing the user and password.

    """
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    return user, password

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


def fetch_emails(mail, from_timestamp, to_timestamp):
    """
    Fetch all emails in the INBOX folder and yield them one at a time.

    Args:
        mail (imaplib.IMAP4_SSL): An IMAP4_SSL connection to the mail server.
        from_timestamp (str): A string in ISO 8601 format indicating the earliest date from which to fetch emails.
        to_timestamp (str): A string in ISO 8601 format indicating the latest date from which to fetch emails.

    Raises:
        ValueError: If the mailbox selection fails.

    """
    status, messages = mail.select('INBOX')
    if status != "OK":
        raise ValueError("Incorrect mail box")

    # Domains to filter by
    domains = ["patagonian.it", "patagonian.com", "patagoniansys.com"]

    if from_timestamp:
        # Convert timestamp string to datetime object
        from_date = datetime.fromisoformat(from_timestamp)

        # Convert datetime object to IMAP-compliant date format
        from_imap_date = from_date.strftime("%d-%b-%Y")

        # Set search criterion for "since" the specified date
        criterion_since = f'(SINCE "{from_imap_date}")'

    if to_timestamp:
        # Convert timestamp string to datetime object
        to_date = datetime.fromisoformat(to_timestamp)

        # Convert datetime object to IMAP-compliant date format
        to_imap_date = to_date.strftime("%d-%b-%Y")

        # Set search criterion for "before" the specified date
        criterion_before = f'(BEFORE "{to_imap_date}")'

    # Combine the search criteria
    search_criteria = f'{criterion_since} {criterion_before}'

    # Fetch emails using the search criteria
    _, message_numbers = mail.search(None, search_criteria)

    for num in message_numbers[0].split():
        res, msg = mail.fetch(num, '(RFC822)')
        for response in msg:
            if isinstance(response, tuple):
                msg_str = response[1].decode('utf-8')
                email_message = email.message_from_string(msg_str)
                if any(domain in email_message["from"] for domain in domains):
                    yield email_message

def format_email_contents(email_message):
    sentences = []
    subject = email_message["subject"]
    body = b""
    for part in email_message.walk():
        if part.get_content_type() == 'text/plain':
            body += part.get_payload(decode=True)

    if body:
        text = body + subject.encode('utf-8')
        decoded_text = urllib.parse.unquote(text.decode('utf-8'))
        translation_table = str.maketrans(
            "áéíóúñÁÉÍÓÚÑ",
            "aeiounAEIOUN" )
        cleaned_text = decoded_text.translate(translation_table)

        # Tokenize the text into sentences
        raw_sentences = nltk.sent_tokenize(cleaned_text)

        # Filter the sentences with a subject, verb, and complement
        for raw_sentence in raw_sentences:
            tokens = nltk.word_tokenize(raw_sentence)
            tags = nltk.pos_tag(tokens)
            if any(tag in VERB_TAGS for word, tag in tags):
                if any(tag in NOUN_TAGS for word, tag in tags):
                    if any(tag in NOUN_TAGS for word, tag in tags[::-1]):
                        if len(raw_sentence.strip()) > 0:  # Check if sentence is not empty
                            sentences.append(raw_sentence)

    return sentences



if __name__ == "__main__":
    user, password = get_credentials()
    mail = connect_to_mail_server('imap.gmail.com', user, password)
    for email_message in fetch_emails(mail):
        texts = format_email_contents(email_message)
        print(texts)