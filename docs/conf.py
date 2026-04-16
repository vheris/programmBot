import os
import sys

# Теперь указываем Sphinx искать исходники в папке src
sys.path.insert(0, os.path.abspath('../src'))

project = 'programmBot'
copyright = '2024, vheris'
author = 'vheris'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = []
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv']

html_theme = 'sphinx_rtd_theme'
html_static_path = []