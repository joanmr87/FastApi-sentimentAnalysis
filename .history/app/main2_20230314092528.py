import datetime
from fastapi import FastAPI
from pydantic import BaseModel

from nltk.corpus import stopwords
from textblob import TextBlob
import re
import nltk
from googletrans import Translator

nltk.download('punkt')
nltk.download('stopwords')

app = FastAPI()

stp_words = stopwords.words('english')
translator = Translator()

class SentimentRequest(BaseModel):
    fromTimestamp: str
    toTimestamp: str
    email: str

@app.post("/")
def sentiment_analysis(sentiment_request: SentimentRequest):
    # emails = obtenerEmails(fromTimestamp, toTimestamp, email)
    emails = ['Hola queria contarte que estoy muy contento, gracias por todo','Hola queria contarte que estoy muy enojado y disconforme']
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
    