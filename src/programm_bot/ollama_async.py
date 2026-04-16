"""Асинхронный клиент для работы с API Ollama."""

import httpx

OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
OLLAMA_MODEL: str = "qwen2.5-coder:0.5b"


async def ollama_chat(
    messages: list[dict[str, str]], model: str = OLLAMA_MODEL
) -> str:
    """Отправляет запрос к локальной нейросети Ollama и возвращает ответ.

    Функция устанавливает асинхронное соединение с API Ollama, передает
    историю сообщений и получает сгенерированный результат.

    Args:
        messages (list[dict[str, str]]): Список словарей с сообщениями.
            Каждый словарь должен содержать ключи 'role' (например, 'user'
            или 'system') и 'content' с текстом запроса.
        model (str, optional): Имя используемой модели.
            По умолчанию `qwen2.5-coder:0.5b`.

    Returns:
        str: Сгенерированный моделью текст (конвертированный код).

    Raises:
        httpx.HTTPStatusError: Если сервер Ollama вернул код ошибки.
        httpx.RequestError: В случае проблем с сетевым подключением к API.
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {"model": model, "messages": messages, "stream": False}

    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()

    return data["message"]["content"]