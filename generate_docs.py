"""Простой генератор документации из docstrings."""

import inspect
import sys
from pathlib import Path

def extract_docs():
    """Вытаскивает docstrings из модулей и создаёт простой документ."""
    
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    modules = {}
    
    for module_name in ['bot', 'ollama_async']:
        try:
            module = __import__(module_name)
            modules[module_name] = module
        except Exception as e:
            print(f"Ошибка при импорте {module_name}: {e}")
    

    doc = "# API Документация programmBot\n\n"
    for module_name, module in modules.items():
        doc += f"## {module_name}.py\n\n"
        doc += f"{inspect.getdoc(module) or 'Нет описания'}\n\n"
        
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith('_'):
                doc += f"### {name}\n\n"
                doc += f"```\n{inspect.signature(obj)}\n```\n\n"
                if obj.__doc__:
                    doc += f"{obj.__doc__}\n\n"
                else:
                    doc += "*(Нет описания)*\n\n"
    
    output_file = project_root / 'API.md'
    output_file.write_text(doc, encoding='utf-8')
    print(f"Документация сохранена в {output_file}")
    return str(output_file)


if __name__ == '__main__':
    extract_docs()
