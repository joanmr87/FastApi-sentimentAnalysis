@app.post("/")
def sentiment_analysis(sentiment_request: SentimentRequest):
   user, password = get_credentials()
   mail = connect_to_mail_server('imap.gmail.com', user, password)
   results = {"reportGeneratedDate": "",
              "extractedEmail": sentiment_request.email,
              "status": "succeeded",
              "emails": []}

   for email_message in fetch_emails(mail, sentiment_request.fromTimestamp, sentiment_request.toTimestamp):
        emails = format_email_contents(email_message)
    
        now = datetime.now()
        email_result = {"emailSentDate": now.strftime("%Y-%m-%d %H:%M:%S"),
                        "sentences": []}

        for email in emails:
            translated_emails = translator.translate(email, src='es', dest='en').text
            print(translated_emails)
            email_cleaned = email_cleaning(translated_emails)
            polarity_scores = cal_polarity(email_cleaned)

            for polarity_score in polarity_scores:
                sentence_result = {"polarityScore": polarity_score}
                email_result["sentences"].append(sentence_result)

        results["emails"].append(email_result)

   results["reportGeneratedDate"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   return results
