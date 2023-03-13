from textblob import TextBlob
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

from fastapi import FastAPI


app = FastAPI()

#http://127.0.0.1:8000

@app.get("/")
def sentimentAnalysis():
    # Read the text file with the emails
    with open(r'C:\Users\joanm\OneDrive\Escritorio\texts4.txt', 'r') as file:
        emails = file.readlines()

    stp_wordsES = stopwords.words('spanish')

    results = {"reportGeneratedDate": "2023-03-03 00:00:00",
                "extractedEmail": "sentiment@patagonian.com",
                "status": "succeded",
                "email": []}

    for email in emails:
        email_cleaned = EmailCleaning(email)
        polarity_score = calPolarity(email_cleaned)
        segmentation_result = segmentation(polarity_score)

        email_result = {"emailSentDate": "2023-03-03 00:00:00",
                        "polarityScore": polarity_score,
                        "segmentation": segmentation_result}

        results["email"].append(email_result)

    return results



def EmailCleaning(email):
    cleanEmail = re.sub(r"@[a-zA-Z0-9]+","",email)
    cleanEmail = re.sub(r"<.*?>", "", cleanEmail)
    cleanEmail = ' '.join(word for word in cleanEmail.split() if word not in stp_wordsES )
    return cleanEmail

def calPolarity(email):
    return TextBlob(email).sentiment.polarity

def calSubjectivity(email):
    return TextBlob(email).sentiment.subjectivity

def segmentation(email):
    if email > 0:
        return "positive"
    elif email == 0:
        return "neutral"
    else:
        return "negative"
