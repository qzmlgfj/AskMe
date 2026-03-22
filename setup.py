from setuptools import setup, find_packages

from pathlib import Path
import re


def read_version():
    version_file = Path(__file__).parent / "ask_me" / "version.py"
    text = version_file.read_text(encoding="utf-8")
    m = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", text)
    if not m:
        raise RuntimeError("Unable to find __version__ in ask_me/version.py")
    return m.group(1)

setup(
    name="ant_ask_me",
    version=read_version(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "blinker>=1.8.2",
        "click>=8.1.7",
        "colorama>=0.4.6",
        "flask>=3.0.3",
        "Flask-Cors>=4.0.2",
        "flask-sqlalchemy>=3.1.1",
        "greenlet>=3.0.3",
        "gunicorn>=22.0.0",
        "importlib-metadata>=7.1.0",
        "itsdangerous>=2.2.0",
        "jinja2>=3.1.4",
        "MarkupSafe>=2.1.5",
        "packaging>=24.0",
        "PyJWT>=2.8.0",
        "SQLAlchemy>=2.0.30",
        "typing-extensions>=4.11.0",
        "werkzeug>=3.0.3",
        "zipp>=3.18.2"
    ],
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding='utf-8').read(),
    url="https://github.com/qzmlgfj/AskMe",
)
