from pydantic import BaseModel, Field

# llama3.2:1b
# llama3.2:latest
# deepseek-r1:latest 
# gpt-oss:latest

class LLMRequest(BaseModel):
    prompt: str
    model: str = "gpt-oss:latest"
    system: str = ""
    temperature: float = Field(default=1.0, ge=0, le=2.0)
    num_predict: int = -1         
    stream: bool = True