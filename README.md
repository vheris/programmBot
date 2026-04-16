# Программ Бот — Конвертер кода в Telegram

Бот для автоматической конвертации кода из одного языка программирования в другой через Telegram. Использует локальную нейросеть `qwen2.5-coder` (через Ollama) для обработки кода, а для управления зависимостями — менеджер `uv`.

## Возможности

- Поддержка 9 языков: Python, JavaScript, Java, C++, Ruby, Kotlin, Swift, Go, C#
- Принимает код в виде **текста** или **файлов** (поддерживаются все популярные форматы: `.py`, `.js`, `.cpp` и т.д.)
- Асинхронная обработка запросов
- Новый цикл перевода без перезапуска бота
- Интерактивное меню

## Требования

- Python 3.9+
- Менеджер пакетов `uv`
- Локально запущенный Ollama (`http://127.0.0.1:11434`)
- Токен Telegram бота

---

## 🛠 1. Установка Ollama

* **Windows**: Скачайте с [официального сайта](https://ollama.com/download) и установите.
* **Linux**: Выполните команду:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

После установки запустите сервис и скачайте модель:
```bash
ollama serve
# В новом окне терминала:
ollama pull qwen2.5-coder:0.5b
```

---

## 🚀 2. Установка проекта (`uv`)

Проект использует современный и быстрый пакетный менеджер [uv](https://docs.astral.sh/uv/) со структурой `src-layout`.

### Установка `uv`
* **Windows** (PowerShell):
  ```powershell
  powershell -ExecutionPolicy ByRef -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
* **Linux / macOS**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Настройка бота
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/vheris/programmBot
   cd programmBot
   ```
2. Установите все зависимости:
   ```bash
   uv sync
   ```
3. Запустите бота:
   ```bash
   uv run python src/programm_bot/bot.py
   ```

---

## 🏗 Структура проекта

```text
programmBot/
├── src/
│   └── programm_bot/   # Исходный код пакета
│       ├── __init__.py
│       ├── bot.py      # Основной файл Telegram-бота
│       └── ollama_async.py # Клиент Ollama API
├── docs/               # Настройки для документации Sphinx
├── pyproject.toml      # Единая конфигурация проекта (uv / hatchling)
├── uv.lock             # Зафиксированные версии пакетов
└── README.md           # Этот файл
```

## Использование

1. Откройте Telegram и найдите бота.
2. Отправьте команду `/start`.
3. Выберите исходный и целевой языки программирования.
4. Отправьте код (текстом или файлом).
5. Получите результат и, при желании, начните новую конвертацию.

## Безопасность

**Внимание**: Для использования в production уберите токен бота из исходного кода. Используйте `.env` файл:

```python
from dotenv import load_dotenv
import os

load_dotenv()
bot = AsyncTeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
```

## 📚 Документация API

Проект использует **Sphinx** для сборки документации прямо из исходного кода.

### Сборка документации
Выполните команду в корне проекта:

```bash
uv run sphinx-build -b html docs docs/_build/html
```

Готовая документация будет лежать здесь: `docs/_build/html/index.html`. Откройте этот файл в браузере, чтобы увидеть подробное описание всех модулей.