from fastapi import FastAPI, HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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
    intent: str
    sucess: bool

class DefaultRequest(BaseModel):
    message: str

def reply(user_quesion: str) -> str:

    intent_map = {
        "location" : {
            "keywords": ["location", "where", "find you", "address", "address"],
            "response": "We are located at DragonStar Mark parking lot - Booth 16."
        },
        "hours" : {
            "keywords" : ["business hours", "hours", "location hours", "closing time", "opening time", "times", "time"],
            "response" : "We are open 9am - 4pm, from Monday - Friday, starting June 12th."
        }
    }

    message = user_quesion.lower()

    for intent_names, intent_data in intent_map.items():  # loops through my dictionary list "intent_names = location / hours" & "intent_data = keywords / response".
        if any(keyword in message for keyword in intent_data["keywords"]):
            return intent_data["response"]
        
    return "Sorry, I do not have the answer for that yet, I'm still learning. Please email one our members for further information."


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
    reply = basic_reply(request.message)
    return DefaultResponse(response=reply)
