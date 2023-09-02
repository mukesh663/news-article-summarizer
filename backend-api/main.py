from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from predict import summary

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/result/{text}")
async def create_item(text: str):
    res, ps, ng, nu = summary(text)
    return {"result": res,
            "pos_sentiment": ps*100,
            "neg_sentiment": ng*100,
            "neu_sentiment": nu*100
            }