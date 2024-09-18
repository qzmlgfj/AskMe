from setuptools import setup, find_packages

from ask_me import __version__

setup(
    name="ant_ask_me",
    version=__version__,
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
