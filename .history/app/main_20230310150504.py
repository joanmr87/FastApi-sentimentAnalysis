from fastapi import FastAPI

from nltk.corpus import stopwords
from textblob import TextBlob
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')

app = FastAPI()

stp_words = stopwords.words('spanish')


@app.post("/")
def sentiment_analysis(fromTimestamp: str, toTimestamp: str, email: str):
    # emails = obtenerEmails(fromTimestamp, toTimestamp, email)
    emails = ['odio!!!  enojo, hate you!!!!', 'te amo, te quiero, love you']
    results = {"reportGeneratedDate": "2023-03-09 00:00:00",
               "extractedEmail": "sentiment@patagonian.com",
               "status": "succeeded",
               "email": []}

    for email in emails:
        email_cleaned = email_cleaning(email)
        polarity_score = cal_polarity(email_cleaned)
        segmentation_result = segmentation(polarity_score)

        email_result = {"emailSentDate": "2023-03-09 00:00:00",
                        "polarityScore": polarity_score,
                        "subjectivityScore": cal_subjectivity(email_cleaned),
                        "segmentation": segmentation_result}

        results["email"].append(email_result)

    return results


def email_cleaning(email):
    clean_email = re.sub(r"@[a-zA-Z0-9]+", "", email)
    clean_email = re.sub(r"<.*?>", "", clean_email)
    clean_email = ' '.join(
        word for word in clean_email.split() if word not in stp_words)
    return clean_email


def cal_polarity(email):
    return TextBlob(email).sentiment.polarity


def cal_subjectivity(email):
    return TextBlob(email).sentiment.subjectivity


def segmentation(polarity_score):
    if polarity_score > 0:
        return "positive"
    elif polarity_score == 0:
        return "neutral"
    else:
        return "negative"
