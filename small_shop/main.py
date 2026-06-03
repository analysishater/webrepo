from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello(lang: str = "fr"):
    if lang == "fr":
        return {"message": "bienvenue!"}
    else:
        return {"message": "welcome!"}