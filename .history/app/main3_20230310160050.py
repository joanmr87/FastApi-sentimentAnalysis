from fastapi import FastAPI
from pydantic import BaseModel
from nltk.corpus import stopwords
from textblob import TextBlob
import re
import nltk
from sklearn.cluster import KMeans
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer


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
    emails = ['odio!!!  enojo, hate you!!!!', 'te amo, te quiero, love you']
    results = {"reportGeneratedDate": "2023-03-09 00:00:00",
               "extractedEmail": sentiment_request.email,
               "status": "succeeded",
               "emails": []}

    for email in emails:
        email_cleaned = email_cleaning(email)
        polarity_scores, topics = cal_polarity_and_topics(email_cleaned)
        email_result = {"emailSentDate": "2023-03-09 00:00:00",
                        "sentences": []}
        for i, sentence in enumerate(email_cleaned.split(". ")):
            sentence_result = {"topic": topics[i],
                               "polarityScore": polarity_scores[i]}
            email_result["sentences"].append(sentence_result)
        results["emails"].append(email_result)

    return results


def email_cleaning(email):
    clean_email = re.sub(r"@[a-zA-Z0-9]+", "", email)
    clean_email = re.sub(r"<.*?>", "", clean_email)
    clean_email = ' '.join(
        word for word in clean_email.split() if word not in stp_words)
    return clean_email


def cal_polarity_and_topics(email):
    # Realizar el análisis de sentimiento y obtener las polaridades de cada oración
    polarity_scores = []
    for sentence in TextBlob(email).sentences:
        polarity_scores.append(sentence.sentiment.polarity)

    # Realizar la segmentación por temas utilizando KMeans clustering
    vectorizer = CountVectorizer(stop_words=stp_words)
    X = vectorizer.fit_transform(TextBlob(email).sentences)
    kmeans = KMeans(n_clusters=3, random_state=0)
    kmeans.fit(X)
    centroids = kmeans.cluster_centers_

    # Asignar cada oración al tema más cercano utilizando la similitud del coseno
    topics = []
    for sentence in TextBlob(email).sentences:
        sentence_vector = vectorizer.transform([str(sentence)])
        similarities = np.array([cosine_similarity(sentence_vector, centroid.reshape(1, -1)) for centroid in centroids])
        topic_index = np.argmax(similarities)
        topics.append(vectorizer.get_feature_names()[topic_index])
    return polarity_scores, topics
