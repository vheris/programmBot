import pytest
from unittest.mock import AsyncMock, MagicMock
from telebot.types import Message
from programm_bot.bot import welcome_message, choose_from_language, bot, user_data

@pytest.mark.asyncio
async def test_welcome_message():
    """Проверяем команду /start."""
    msg = MagicMock()
    msg.from_user.first_name = "Иван"
    msg.chat.id = 12345
    
    bot.send_message = AsyncMock()

    await welcome_message(msg)
    
    # Проверяем, что сообщение было отправлено
    bot.send_message.assert_called_once()
    
    # Проверяем текст приветствия
    assert "Привет, Иван!" in bot.send_message.call_args[0][1]

@pytest.mark.asyncio
async def test_choose_from_language():
    """Проверяем сохранение языка в user_data."""
    call = MagicMock()
    call.from_user.id = 999
    call.data = "from_python"
    call.message.chat.id = 12345
    call.message.id = 67890

    bot.edit_message_text = AsyncMock()

    await choose_from_language(call)

    # Проверяем логику сохранения
    assert user_data[999]["from_lang"] == "python"
    bot.edit_message_text.assert_called_once()
    assert "Выбран язык: PYTHON" in bot.edit_message_text.call_args[0][0]