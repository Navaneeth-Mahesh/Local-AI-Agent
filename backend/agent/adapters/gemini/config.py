from  dataclasses import dataclass

@dataclass(slot=True)
class GeminiConfig:
    model: str = "gemini-2.5-flash"
    temperature: float = 0.7
    max_output_token: int = 2048
    timeout: float  = 60.0
    maxx_retries: int =  3
    
     