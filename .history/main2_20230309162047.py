from fastapi import FastAPI
app = FastAPI()

#cambiar a post
@app.get("/")
def index():
    return "Holaaaa"
