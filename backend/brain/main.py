from fastapi import FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chat_logic import reply

app = FastAPI()

origins = [
    "https://goliexeegardens.com",
    "https://www.goliexeegardens.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Use Pydantic BaseModel to set standard for a response - create a class.
class DefaultResponse(BaseModel):
    response: str

class DefaultRequest(BaseModel):
    message: str

''' # if "where" in message or "location" in message or "located" in message or "booth" in message:
    #     return "We are located by the DragonStar in Brooklyn Park, MN - Booth 16"
    
    # if "time" in message or "times" in message or "hours" in message:
    #     return "We are open 9am - 4pm, from Monday - Friday, starting June 12th."
'''
    # return "Sorry, I do not have the answer for that yet, I'm still learning. Please email one our members for further information."


@app.get("/")
async def root():
    return {"This endpoint for the chatbot is a working API - Please refer to '/chatbot/'"}

# @app.get("/chat/")
# async def get_chatbot():
#     '''
#         Retrieve the chatbot for my GolieXeeGarden Site.
#     '''
#     raise HTTPException(
#         status_code= status.HTTP_200_OK,
#         detail= "This is a working API endpoint, but the endpoint is functional."
#     )


@app.post("/chatbot/", response_model=DefaultResponse)  # Use response_model not response_class. You will run into open_ai json error if choose latter.
async def chatbot(request: DefaultRequest):
    chatreply = reply(request.message)
    return DefaultResponse(response=chatreply)

if __name__ == "__main__":
    reply()