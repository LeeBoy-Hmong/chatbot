from fastapi import FastAPI, HTTPException,status
import uvicorn

app = FastAPI()

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


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)