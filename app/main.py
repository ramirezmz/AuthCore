from fastapi import FastAPI
from adapters.web.api import api_router

app = FastAPI()


@app.get("/check-health")
def check_health():
    return {"status": "ok"}


app.include_router(api_router)
