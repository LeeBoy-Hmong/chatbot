from fastapi import FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origin = [
    "https://goliexeegardens.com",
    "https://www.goliexeegardens.com",
]

@app.get("/")
async def root():
    return {"This endpoint for the chatbot is a working API - Please refer to '/chatbot/'"}

@app.get("/chatbot/")
async def get_chatbot():
    '''
        Retrieve the chatbot for my GolieXeeGarden Site.
    '''
    raise HTTPException(
        status_code= status.HTTP_200_OK,
        detail= "This is a working API endpoint, but the endpoint is functional."
    )
