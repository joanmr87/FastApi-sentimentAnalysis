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
    emails = ['Buenos dias Sentiment!¡Espero que te encuentres bien! Me pongo en contacto con vos para expresarte mis mas sinceras felicitaciones por tu excelente desempeno en el proyecto que acabamos de finalizar. Desde el inicio del proyecto, pude observar tu compromiso y dedicacion para llevarlo adelante, lo cual fue fundamental para alcanzar los objetivos propuestos en el tiempo estipulado. Tu habilidad para coordinar al equipo, manejar situaciones complejas y tomar decisiones acertadas fueron realmente impresionantes. No puedo dejar de mencionar la calidad del trabajo entregado. Tu atencion al detalle, tu capacidad de analisis y tu creatividad contribuyeron en gran medida al exito del proyecto. En definitiva, quiero agradecerte por tu esfuerzo y trabajo en equipo, y felicitarte nuevamente por este logro. Estoy segura de que seguiras aportando valor en futuros proyectos.¡Felicitaciones nuevamente!']
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
