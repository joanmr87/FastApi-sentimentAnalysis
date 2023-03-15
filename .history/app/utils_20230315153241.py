import datetime
import os
import re
import urllib.parse
from typing import List
from email.message import Message

import email
import email.header
import imaplib
from datetime import datetime

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
        to_imap_date = to_date
