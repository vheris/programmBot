![CI](https://github.com/vheris/programmBot/actions/workflows/ci.yml/badge.svg)

# Программ Бот — Конвертер кода в Telegram

Бот для автоматической конвертации кода из одного языка программирования в другой через Telegram. Использует локальную нейросеть qwen2.5-coder (через Ollama) для обработки кода, а для управления проектом — менеджер uv.

## Возможности

- **Автоопределение языка**: Бот автоматически определяет исходный язык программирования.
- **Поддержка 9 направлений**: Python, JavaScript, Java, C++, Ruby, Kotlin, Swift, Go, C#.
- **Работа с файлами**: Принимает код текстом или файлами (.py, .js, .cpp и т.д.).
- **Асинхронность**: Обработка запросов через библиотеку telebot (AsyncTeleBot).
- **Чистый код**: Интегрирован линтер Ruff и тесты Pytest.

## Требования

- Python 3.10+
- Менеджер пакетов uv
- Локально запущенный Ollama (http://127.0.0.1:11434)
- Токен Telegram бота (получить у https://t.me/botfather)

---

## 🛠 1. Установка Ollama

### Windows
Скачайте инсталлятор с официального сайта: https://ollama.com/download

### Linux
Выполните команду в терминале:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Запуск и загрузка модели
1. Запустите сервер Ollama:
   ```bash
   ollama serve
   ```
2. **В новом окне терминала** скачайте модель:
   ```bash
   ollama pull qwen2.5-coder:0.5b
   ```

---

## 🚀 2. Установка uv и проекта

Проект использует менеджер пакетов uv и структуру src-layout.

### Установка uv
- **Windows (PowerShell)**:
  ```powershell
  powershell -ExecutionPolicy ByRef -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Linux / macOS**:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Настройка бота
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/vheris/programmBot
   cd programmBot
   ```
2. Синхронизируйте окружение:
   ```bash
   uv sync
   ```
3. Запустите бота:
   ```bash
   uv run programm-bot
   ```

---

## 🧪 3. Качество кода и Тесты

В проекте настроен Ruff для линтинга и Pytest для проверки логики.

- **Запуск тестов**:
    ```bash
    uv run pytest -v
    ```
- **Проверка линтером**:
    ```bash
    uv run ruff check src/
    ```
- **Форматирование кода**:
    ```bash
    uv run ruff format src/
    ```

---

## 🏗 Структура проекта

```text
programmBot/
├── .github/workflows/    # CI/CD: автоматический прогон тестов на GitHub
│   └── ci.yml
├── src/
│   └── programm_bot/     # Исходный код пакета (только логика)
│       ├── bot.py        # Основная логика и точка входа (run)
│       └── ollama_async.py # Клиент Ollama API
├── tests/                # Модульные тесты (Mock-тестирование)
│   ├── __init__.py
│   ├── test_bot.py
│   └── test_ollama.py
├── docs/                 # Документация Sphinx
├── pyproject.toml        # Конфигурация проекта, зависимостей и Ruff
├── uv.lock               # Зафиксированные версии пакетов
└── README.md
```

---

## 🛡 Безопасность

**Внимание**: Для использования в production уберите токен бота из исходного кода. Используйте `.env` файл:

```python
from dotenv import load_dotenv
import os

load_dotenv()
bot = AsyncTeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
```

---

## 📚 Документация

Для генерации HTML-документации из docstrings:
```bash
uv run sphinx-build -b html docs docs/_build/html
```
Файл для открытия в браузере: docs/_build/html/index.html

---

## 🔧 Решение проблем

### Бот не отвечает
- Проверьте, что токен в `bot.py` актуальный.
- Убедитесь, что интернет-соединение активно.

### Ошибка "Connection refused"
- Убедитесь, что Ollama запущен: `ollama serve`.
- Проверьте доступность API: `curl http://127.0.0.1:11434`.

### Модель не найдена
- Скачайте модель вручную: `ollama pull qwen2.5-coder:0.5b`.

### Таймаут при конвертации
- Увеличьте `timeout` в `ollama_async.py` (по умолчанию 120 секунд).
- Проверьте ресурсы ПК — нейросеть требует значительной мощности CPU/GPU.

### Ошибка импорта (ImportError)
Не запускайте бота напрямую через `python bot.py`. Используйте только команду:
`uv run programm-bot`