from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import subprocess

app = FastAPI()

class Message(BaseModel):
    message: str

@app.post("/v1/ask")
async def ask(request: Request, message: Message):
    try:
        payload = json.dumps({"message": message.message})
        command = f'curl -X POST http://localhost:11434/v1/chat -H "Content-Type: application/json" -d "{payload}"'
        response = subprocess.check_output(command, shell=True, text=True)
        return {"response": response.strip()}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
