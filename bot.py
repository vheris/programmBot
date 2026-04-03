"""ProgrammBot - Telegram код конвертер

Бот для конвертации кода между различными языками программирования
используя локальную модель Ollama.

Модули:
    telebot: API для работы с Telegram ботом
    ollama_async: Асинхронный клиент для Ollama API

Примеры:
    Запуск бота:
    >>> python bot.py
"""

import asyncio
from telebot import types
import os

from telebot.async_telebot import AsyncTeleBot
from ollama_async import ollama_chat

bot = AsyncTeleBot('8469870119:AAE5IG0YpKQT7Fv3EozFjNK_Msm1qxAALIE')

user_data = {}

@bot.message_handler(commands=['start'])
async def welcome_message(message):
    """Обработчик команды /start - приветствие и выбор исходного языка.
    
    Отправляет приветственное сообщение и показывает кнопки для выбора
    исходного языка программирования (из какого языка переводить).
    
    Args:
        message: Telegram message object с данными пользователя
        
    Returns:
        None
    """
    text = f'Привет, {message.from_user.first_name}!👋 \nМы поможем тебе конвертировать твой код на другой ЯП!😁\n\nВыбери исходный язык программирования:'

    markup = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton('Python', callback_data='from_python')
    btn2 = types.InlineKeyboardButton('JavaScript', callback_data='from_javascript')
    btn3 = types.InlineKeyboardButton('Java', callback_data='from_java')
    btn4 = types.InlineKeyboardButton('C++', callback_data='from_cpp')
    btn5 = types.InlineKeyboardButton('Ruby', callback_data='from_ruby')
    btn6 = types.InlineKeyboardButton('Kotlin', callback_data='from_kotlin')
    btn7 = types.InlineKeyboardButton('Swift', callback_data='from_swift')
    btn8 = types.InlineKeyboardButton('Go', callback_data='from_go')
    btn9 = types.InlineKeyboardButton('C#', callback_data='from_csharp')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    
    await bot.send_message(message.chat.id, text, reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: call.data.startswith('from_'))
async def choose_from_language(call):
    """Обработчик выбора исходного языка.
    
    Сохраняет выбранный пользователем исходный язык и показывает
    кнопки для выбора целевого языка (на какой язык переводить).
    
    Args:
        call: Callback query object с данными о нажатой кнопке
        
    Returns:
        None
    """
    user_id = call.from_user.id
    lang = call.data.replace('from_', '')
    user_data[user_id] = {'from_lang': lang} 
    
    text = f'Выбран язык: {lang.upper()}\n\nТеперь выбери язык, на который нужно перевести:'
    
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton('Python', callback_data='to_python')
    btn2 = types.InlineKeyboardButton('JavaScript', callback_data='to_javascript')
    btn3 = types.InlineKeyboardButton('Java', callback_data='to_java')
    btn4 = types.InlineKeyboardButton('C++', callback_data='to_cpp')
    btn5 = types.InlineKeyboardButton('Ruby', callback_data='to_ruby')
    btn6 = types.InlineKeyboardButton('Kotlin', callback_data='to_kotlin')
    btn7 = types.InlineKeyboardButton('Swift', callback_data='to_swift')
    btn8 = types.InlineKeyboardButton('Go', callback_data='to_go')
    btn9 = types.InlineKeyboardButton('C#', callback_data='to_csharp')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    
    await bot.edit_message_text(text, call.message.chat.id, call.message.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('to_'))
async def choose_to_language(call):
    """Обработчик выбора целевого языка.
    
    Сохраняет выбранный пользователем целевой язык и уведомляет,
    что бот готов к получению кода.
    
    Args:
        call: Callback query object с данными о нажатой кнопке
        
    Returns:
        None
    """
    user_id = call.from_user.id
    lang = call.data.replace('to_', '')
    user_data[user_id]['to_lang'] = lang
    
    from_lang = user_data[user_id]['from_lang']
    
    text = f'Переведем с {from_lang.upper()} на {lang.upper()}. Пришли свой код:'
    
    await bot.edit_message_text(text, call.message.chat.id, call.message.id)


async def send_restart_prompt(chat_id):
    """Отправляет приглашение к новой конвертации с клавиатурой.
    
    После успешной конвертации отправляет сообщение с предложением
    провести ещё одну конвертацию и кнопками выбора исходного языка.
    
    Args:
        chat_id (int): Telegram ID чата для отправки сообщения
        
    Returns:
        None
    """
    text = 'Хочешь конвертировать ещё? Выбери исходный язык:'
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton('Python', callback_data='from_python')
    btn2 = types.InlineKeyboardButton('JavaScript', callback_data='from_javascript')
    btn3 = types.InlineKeyboardButton('Java', callback_data='from_java')
    btn4 = types.InlineKeyboardButton('C++', callback_data='from_cpp')
    btn5 = types.InlineKeyboardButton('Ruby', callback_data='from_ruby')
    btn6 = types.InlineKeyboardButton('Kotlin', callback_data='from_kotlin')
    btn7 = types.InlineKeyboardButton('Swift', callback_data='from_swift')
    btn8 = types.InlineKeyboardButton('Go', callback_data='from_go')
    btn9 = types.InlineKeyboardButton('C#', callback_data='from_csharp')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    await bot.send_message(chat_id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.from_user.id in user_data and 'to_lang' in user_data[message.from_user.id])
async def convert_code(message):
    """Обработчик текста кода для конвертации.
    
    Получает текст кода от пользователя, отправляет запрос на конвертацию
    в Ollama и возвращает результат с форматированием.
    
    Args:
        message: Telegram message object с текстом кода
        
    Raises:
        Exception: Если возникает ошибка при конвертации
        
    Returns:
        None
    """
    user_id = message.from_user.id
    code = message.text

    from_lang = user_data[user_id]['from_lang']
    to_lang = user_data[user_id]['to_lang']

    await bot.send_message(message.chat.id, "Конвертация кода, подождите...")

    try:
        prompt = (
            f"Конвертируй следующий код с языка программирования {from_lang} "
            f"на язык программирования {to_lang}. Верни только код, без объяснений.\n\n{code}"
        )

        messages = [
            {"role": "system", "content": "Ты программист, который конвертирует код из одного языка программирования в другой."},
            {"role": "user", "content": prompt},
        ]

        converted_code = await ollama_chat(messages)

        await bot.send_message(
            message.chat.id,
            f"Конвертированный код:\n\n```{to_lang}\n{converted_code}\n```",
            parse_mode="Markdown",
        )

        del user_data[user_id]

        await send_restart_prompt(message.chat.id)

    except Exception as err:
        await bot.send_message(message.chat.id, f"Ошибка при конвертации: {str(err)}")


@bot.message_handler(content_types=['document'], func=lambda message: message.from_user.id in user_data and 'to_lang' in user_data[message.from_user.id])
async def convert_code_from_file(message):
    """Обработчик файлов с кодом для конвертации.
    
    Получает файл с кодом, скачивает его, и конвертирует содержимое
    между выбранными языками программирования.
    
    Поддерживаемые форматы: .py, .js, .java, .cpp, .rb, .kt, .swift, .go, .cs, .txt
    
    Args:
        message: Telegram message object с документом
        
    Raises:
        Exception: Если возникает ошибка при скачивании или обработке файла
        
    Returns:
        None
    """
    user_id = message.from_user.id

    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        code = downloaded_file.decode('utf-8')

        from_lang = user_data[user_id]['from_lang']
        to_lang = user_data[user_id]['to_lang']

        await bot.send_message(message.chat.id, "Конвертация кода, подождите...")

        prompt = (
            f"Конвертируй следующий код с языка программирования {from_lang} "
            f"на язык программирования {to_lang}. Верни только код, без объяснений.\n\n{code}"
        )

        messages = [
            {"role": "system", "content": "Ты программист, который конвертирует код из одного языка программирования в другой."},
            {"role": "user", "content": prompt},
        ]

        converted_code = await ollama_chat(messages)

        await bot.send_message(
            message.chat.id,
            f"Конвертированный код:\n\n```{to_lang}\n{converted_code}\n```",
            parse_mode="Markdown",
        )

        del user_data[user_id]
        await send_restart_prompt(message.chat.id)

    except Exception as err:
        await bot.send_message(message.chat.id, f"Ошибка при обработке файла: {str(err)}")



if __name__ == "__main__":
    """Запуск бота в режиме polling.
    
    Бот будет постоянно проверять серверы Telegram на наличие
    новых сообщений и обрабатывать их.
    """
    asyncio.run(bot.polling())