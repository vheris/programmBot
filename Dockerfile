FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# Принимаем ID пользователя (по умолчанию 1000)
ARG UID=1000
ARG GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_DEV=1 \
    UV_TOOL_BIN_DIR=/usr/local/bin \
    PYTHONPATH=/app

# Создаем группу и пользователя
RUN groupadd -g ${GID} appuser && \
    useradd -u ${UID} -g ${GID} -m appuser

WORKDIR /app

# Копируем зависимости
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Установка зависимостей системно через uv
RUN uv pip install -r pyproject.toml --system

# Копируем весь проект
COPY --chown=appuser:appuser . .

RUN chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["python", "src/programm_bot/bot.py"]
