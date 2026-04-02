import asyncio
from telebot import types
import os

from telebot.async_telebot import AsyncTeleBot
from ollama_async import ollama_chat

bot = AsyncTeleBot('8469870119:AAE5IG0YpKQT7Fv3EozFjNK_Msm1qxAALIE')

user_data = {}

@bot.message_handler(commands=['start'])
async def welcome_message(message):
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
    user_id = call.from_user.id
    lang = call.data.replace('to_', '')
    user_data[user_id]['to_lang'] = lang
    
    from_lang = user_data[user_id]['from_lang']
    
    text = f'Переведем с {from_lang.upper()} на {lang.upper()}. Пришли свой код:'
    
    await bot.edit_message_text(text, call.message.chat.id, call.message.id)

@bot.message_handler(func=lambda message: message.from_user.id in user_data and 'to_lang' in user_data[message.from_user.id])
async def convert_code(message):
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

    except Exception as err:
        await bot.send_message(message.chat.id, f"Ошибка при конвертации: {str(err)}")
        
asyncio.run(bot.polling())