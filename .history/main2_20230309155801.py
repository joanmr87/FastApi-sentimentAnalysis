app = FastAPI()

@app.get("/")
def index():
    return "Holaaaa"
