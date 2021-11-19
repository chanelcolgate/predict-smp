from fastapi import FastAPI, Request
from typing import Dict, Any

app = FastAPI()

@app.get("/")
async def get_request_object(request: Request) -> Dict[str, Any]:
	return {"path": request.url.path}