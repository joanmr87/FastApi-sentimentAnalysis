from pydantic import BaseModel

class SentimentRequest(BaseModel):
    fromTimestamp: str
    toTimestamp: str
    email: str
