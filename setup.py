from setuptools import setup
import subprocess
from pathlib import Path

try:
    subprocess.run([
        "python", "generate_docs.py"
    ], cwd=Path(__file__).parent, check=False)
except Exception as e:
    print(f"Предупреждение: не удалось сгенерировать документацию: {e}")

setup(
    name="programmBot",
    version="1.0.0",
    description="Telegram bot for code conversion using Ollama",
    py_modules=["bot", "ollama_async"],
    package_data={
        '': ['API.md', 'README.md', 'LICENSE'],
    },
    install_requires=[
        "pyTelegramBotAPI>=4.0",
        "httpx>=0.20.0",
    ],
    python_requires=">=3.8",
)
