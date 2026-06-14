from fastapi import FastAPI, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from brain.chat_logic import reply
from asklee_ai.rag.chain import chain_with_hist

app = FastAPI()

origins = [
    "https://goliexeegardens.com",
    "https://www.goliexeegardens.com",
    # "http://localhost:5500",  # Used for testing only.
    # "http://127.0.0.1:5500"  # Used for testing only.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = [origins],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# Use Pydantic BaseModel to set standard for a response - create a class.
class DefaultResponse(BaseModel):
    response: str

class DefaultRequest(BaseModel):
    message: str

class ChatRequest(BaseModel):
    message: str
    session_id: str

''' # if "where" in message or "location" in message or "located" in message or "booth" in message:
    #     return "We are located by the DragonStar in Brooklyn Park, MN - Booth 16"
    
    # if "time" in message or "times" in message or "hours" in message:
    #     return "We are open 9am - 4pm, from Monday - Friday, starting June 12th."
'''
    # return "Sorry, I do not have the answer for that yet, I'm still learning. Please email one our members for further information."


@app.get("/")
async def root():
    return {"This endpoint for the chatbot is a working API - Please refer to '/chatbot/'"}


@app.get("/health")
async def health():
    is_healthy = True

    if is_healthy:
        return {"Status": "Up"}
    else:
        return Response(
            content= {"Status": "DOWN"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type="application/json"
        )

'''@app.post("/chatbot/", response_model=DefaultResponse)  # Use response_model not response_class. You will run into open_ai json error if choose latter.
async def chatbot(request: DefaultRequest):
    chatreply = reply(request.message)
    return DefaultResponse(response=chatreply)'''

@app.post("/api/chat")
async def chat_session(request: ChatRequest):
    print("Message:", request.message)
    print("Session ID:", request.session_id)

    ai_session = chain_with_hist.invoke(
        {"question": request.message},
        config={"configurable": {"session_id": request.session_id}}  
    )

    return {
        "response": ai_session,
        "session_id": request.session_id
    }


'''if __name__ == "__main__":
    reply()'''