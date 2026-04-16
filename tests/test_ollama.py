from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from programm_bot.ollama_async import ollama_chat


@pytest.mark.asyncio
async def test_ollama_chat_success():
    """Тест успешного ответа от Ollama."""

    # Испольуем MagicMock, так как json() и raise_for_status() — синхронные методы
    mock_response = MagicMock()
    mock_response.json.return_value = {"message": {"content": "print('hello world')"}}
    mock_response.raise_for_status.return_value = None

    # Сама функция post асинхронная, поэтому патчим её через AsyncMock
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        messages = [{"role": "user", "content": "test"}]
        result = await ollama_chat(messages)

        assert result == "print('hello world')"

@pytest.mark.asyncio
async def test_ollama_chat_http_error():
    """Тест обработки ошибки сервера."""

    mock_response = MagicMock()
    # Настраиваем генерацию исключения при вызове синхронного метода
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="500 Internal Server Error",
        request=MagicMock(),
        response=mock_response
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

        with pytest.raises(httpx.HTTPStatusError):
            await ollama_chat([{"role": "user", "content": "test"}])
