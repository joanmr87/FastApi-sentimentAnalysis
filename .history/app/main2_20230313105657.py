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


class SentimentRequest(BaseModel):
    fromTimestamp: str
    toTimestamp: str
    email: str

@app.post("/")
def sentiment_analysis(sentiment_request: SentimentRequest):
    # emails = obtenerEmails(fromTimestamp, toTimestamp, email)
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
      # Translate email to English
    translated_email = TextBlob(clean_email).translate(to='en')
    # Remove stop words in English
    clean_email = ' '.join(
        word for word in translated_email.split() if word not in stopwords.words('english'))
    return clean_email


def cal_polarity(email):
    polarity_scores = []
    for sentence in TextBlob(email).sentences:
        polarity_scores.append(sentence.sentiment.polarity)
    return polarity_scores
