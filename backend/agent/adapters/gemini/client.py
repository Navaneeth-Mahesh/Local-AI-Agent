from google import genai

class GeminiClient:

    def __init__(self, api_key: str):
        self._client = genai.Client(
            api_key=api_key,
        )

    @property
    def client(self):
        return self._client