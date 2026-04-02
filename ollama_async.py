import httpx

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "qwen2.5-coder:0.5b"

async def ollama_chat(messages, model: str = OLLAMA_MODEL) -> str:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {"model": model, "messages": messages, "stream": False}

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()

    return data["message"]["content"]