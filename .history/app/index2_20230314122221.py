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

@app.post("/")
def sentiment_analysis(sentiment_request: SentimentRequest):
   print(sentiment_request.email)
   user, password = get_credentials()
   print(user)

   