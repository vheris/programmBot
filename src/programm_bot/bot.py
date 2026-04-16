"""ProgrammBot - Telegram код конвертер

Бот для конвертации кода между различными языками программирования
используя локальную модель Ollama.
"""

import asyncio

from telebot import types
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from .ollama_async import ollama_chat

bot = AsyncTeleBot("8469870119:AAE5IG0YpKQT7Fv3EozFjNK_Msm1qxAALIE")

# Типизируем словарь: ID пользователя -> настройки языков
user_data: dict[int, dict[str, str]] = {}


@bot.message_handler(commands=["start"])
async def welcome_message(message: Message) -> None:
    """Обработчик команды /start - приветствие и выбор исходного языка.

    Отправляет приветственное сообщение и показывает кнопки для выбора
    исходного языка программирования, включая опцию автоопределения.

    Args:
        message (Message): Объект сообщения Telegram.
    """
    text = (
        f"Привет, {message.from_user.first_name}!👋 \n"
        "Мы поможем тебе конвертировать твой код на другой ЯП!😁\n\n"
        "Выбери исходный язык программирования:"
    )

    markup = types.InlineKeyboardMarkup(row_width=3)

    # Кнопка автоопределения
    btn_auto = types.InlineKeyboardButton("🔍 Автоопределение",
                                           callback_data="from_auto",)

    btn1 = types.InlineKeyboardButton("Python",
                                      callback_data="from_python",)
    btn2 = types.InlineKeyboardButton("JavaScript",
                                      callback_data="from_javascript",)
    btn3 = types.InlineKeyboardButton("Java",
                                      callback_data="from_java",)
    btn4 = types.InlineKeyboardButton("C++",
                                      callback_data="from_cpp",)
    btn5 = types.InlineKeyboardButton("Ruby",
                                      callback_data="from_ruby",)
    btn6 = types.InlineKeyboardButton("Kotlin",
                                      callback_data="from_kotlin",)
    btn7 = types.InlineKeyboardButton("Swift", callback_data="from_swift,")
    btn8 = types.InlineKeyboardButton("Go",
                                       callback_data="from_go",)
    btn9 = types.InlineKeyboardButton("C#",
                                      callback_data="from_csharp",)

    # Добавляем автоопределение первой строкой, затем остальные 3х3
    markup.add(btn_auto)
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)

    await bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("from_"))
async def choose_from_language(call: CallbackQuery) -> None:
    """Обработчик выбора исходного языка.

    Args:
        call (CallbackQuery): Объект callback-запроса.
    """
    user_id = call.from_user.id
    lang = call.data.replace("from_", "")
    user_data[user_id] = {"from_lang": lang}

    if lang == "auto":
        text = (
            "Выбрано: 🔍 Автоопределение\n\n"
            "Теперь выбери язык, на который нужно перевести:"
        )
    else:
        text = (
            f"Выбран язык: {lang.upper()}\n\n"
            "Теперь выбери язык, на который нужно перевести:"
        )

    markup = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton("Python", callback_data="to_python")
    btn2 = types.InlineKeyboardButton("JavaScript", callback_data="to_javascript")
    btn3 = types.InlineKeyboardButton("Java", callback_data="to_java")
    btn4 = types.InlineKeyboardButton("C++", callback_data="to_cpp")
    btn5 = types.InlineKeyboardButton("Ruby", callback_data="to_ruby")
    btn6 = types.InlineKeyboardButton("Kotlin", callback_data="to_kotlin")
    btn7 = types.InlineKeyboardButton("Swift", callback_data="to_swift")
    btn8 = types.InlineKeyboardButton("Go", callback_data="to_go")
    btn9 = types.InlineKeyboardButton("C#", callback_data="to_csharp")

    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)

    await bot.edit_message_text(
        text, call.message.chat.id, call.message.id, reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("to_"))
async def choose_to_language(call: CallbackQuery) -> None:
    """Обработчик выбора целевого языка.

    Args:
        call (CallbackQuery): Объект callback-запроса.
    """
    user_id = call.from_user.id
    lang = call.data.replace("to_", "")
    user_data[user_id]["to_lang"] = lang

    from_lang = user_data[user_id]["from_lang"]

    if from_lang == "auto":
        text = (
            f"Переведем на {lang.upper()}. Бот сам определит исходный язык. "
            "Пришли свой код:"
        )
    else:
        text = f"Переведем с {from_lang.upper()} на {lang.upper()}. Пришли свой код:"

    await bot.edit_message_text(text, call.message.chat.id, call.message.id)


async def send_restart_prompt(chat_id: int) -> None:
    """Отправляет приглашение к новой конвертации.

    Args:
        chat_id (int): ID чата.
    """
    text = "Хочешь конвертировать ещё? Выбери исходный язык:"
    markup = types.InlineKeyboardMarkup(row_width=3)

    btn_auto = types.InlineKeyboardButton("🔍 Автоопределение",
                                          callback_data="from_auto",)
    btn1 = types.InlineKeyboardButton("Python",
                                      callback_data="from_python",)
    btn2 = types.InlineKeyboardButton("JavaScript",
                                      callback_data="from_javascript")
    btn3 = types.InlineKeyboardButton("Java",
                                       callback_data="from_java")
    btn4 = types.InlineKeyboardButton("C++",
                                      callback_data="from_cpp")
    btn5 = types.InlineKeyboardButton("Ruby",
                                      callback_data="from_ruby")
    btn6 = types.InlineKeyboardButton("Kotlin",
                                      callback_data="from_kotlin")
    btn7 = types.InlineKeyboardButton("Swift",
                                      callback_data="from_swift")
    btn8 = types.InlineKeyboardButton("Go",
                                      callback_data="from_go")
    btn9 = types.InlineKeyboardButton("C#",
                                       callback_data="from_csharp")

    markup.add(btn_auto)
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
    await bot.send_message(chat_id, text, reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.from_user.id in user_data
    and "to_lang" in user_data[message.from_user.id]
)
async def convert_code(message: Message) -> None:
    """Обработчик текста кода для конвертации.

    Args:
        message (Message): Объект сообщения.
    """
    user_id = message.from_user.id
    code = message.text

    from_lang = user_data[user_id]["from_lang"]
    to_lang = user_data[user_id]["to_lang"]

    await bot.send_message(message.chat.id, "Конвертация кода, подождите...")

    try:
        # Формирование промпта в зависимости от выбора языка
        if from_lang == "auto":
            instruction = (
                "Определи язык программирования следующего кода "
                f"и конвертируй его на {to_lang}."
            )
        else:
            instruction = (
                f"Конвертируй следующий код с языка {from_lang} на язык {to_lang}."
            )

        prompt = f"{instruction} Верни только код, без объяснений.\n\n{code}"

        messages = [
            {
                "role": "system",
                "content": "Ты профессиональный программист, конвертирующий код.",
            },
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


@bot.message_handler(
    content_types=["document"],
    func=lambda message: message.from_user.id in user_data
    and "to_lang" in user_data[message.from_user.id],
)
async def convert_code_from_file(message: Message) -> None:
    """Обработчик файлов с кодом для конвертации.

    Args:
        message (Message): Объект сообщения с документом.
    """
    user_id = message.from_user.id

    try:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        code = downloaded_file.decode("utf-8")

        from_lang = user_data[user_id]["from_lang"]
        to_lang = user_data[user_id]["to_lang"]

        await bot.send_message(message.chat.id, "Конвертация кода, подождите...")

        if from_lang == "auto":
            instruction = (
                "Определи язык программирования следующего кода "
                f"и конвертируй его на {to_lang}."
            )
        else:
            instruction = (
                f"Конвертируй следующий код с языка {from_lang} на язык {to_lang}."
            )

        prompt = f"{instruction} Верни только код, без объяснений.\n\n{code}"

        messages = [
            {
                "role": "system",
                "content": "Ты профессиональный программист, конвертирующий код.",
            },
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
        await bot.send_message(
            message.chat.id, f"Ошибка при обработке файла: {str(err)}"
        )


async def main() -> None:
    """Асинхронная основная функция."""
    await bot.polling()


def run() -> None:
    """
    Синхронная точка входа для консольного скрипта.
    Запускает асинхронный цикл событий.
    """
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем.")


if __name__ == "__main__":
    run()
