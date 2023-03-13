from fastapi import FastAPI
from nltk.corpus import stopwords
from textblob import TextBlob
import re
import nltk

nltk.download('punkt')
nltk.download('stopwords')

app = FastAPI()

stp_words = stopwords.words('spanish')

@app.get("/")
def sentimentAnalysis():
    emails = ['odio!!!  enojo, hate you!!!!', 'te amo, te quiero, love you']
    results = {"reportGeneratedDate": "2023-03-09 00:00:00",
              "extractedEmail": "sentiment@patagonian.com",
               "status": "succeeded",
              "email": []}

    for email in emails:
        email_cleaned = EmailCleaning(email)
        polarity_score = calPolarity(email_cleaned)
        segmentation_result = segmentation(polarity_score)

        email_result = {"emailSentDate": "2023-03-09 00:00:00",
                        "polarityScore": polarity_score,
                        "subjectivityScore": calSubjectivity(email_cleaned),
                        "segmentation": segmentation_result}

        results["email"].append(email_result)

    return results


def EmailCleaning(email):
    cleanEmail = re.sub(r"@[a-zA-Z0-9]+", "", email)
    cleanEmail = re.sub(r"<.*?>", "", cleanEmail)
    cleanEmail = ' '.join(
        word for word in cleanEmail.split() if word not in stp_words)
    return cleanEmail


def calPolarity(email):
    return TextBlob(email).sentiment.polarity


def calSubjectivity(email):
    return TextBlob(email).sentiment.subjectivity


def segmentation(polarity_score):
    if polarity_score > 0:
        return "positive"
    elif polarity_score == 0:
        return "neutral"
    else:
        return "negative"
