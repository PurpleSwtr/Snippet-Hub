import json
import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import httpx
import requests

from src.ollama.schemas import LLMRequest

router = APIRouter(prefix='/ollama', tags=['Ollama'])

@router.post("/stream")
async def stream_ollama(request: LLMRequest):
    async def event_generator():
        url = "http://localhost:11434/api/generate"
        
        data = {
            "model": request.model,
            "prompt": request.prompt,
            "system": request.system,
            "stream": request.stream,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.num_predict
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                async with client.stream("POST", url, json=data) as response:
                    
                    if response.status_code != 200:
                        yield f"data: {json.dumps({'error': {response.status_code}})}\n\n"
                        return

                    async for line in response.aiter_lines():
                        if line:
                            try:
                                if line.strip():
                                    yield f"data: {line}\n\n"
                            except Exception as e:
                                yield f"data: {json.dumps({'error': {str(e)}})}\n\n"
                    
                    yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': {str(e)}})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )

@router.get("/models")
async def get_models():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        return response.json()
    except:
        return {"models": []}
