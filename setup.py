from setuptools import setup, find_packages

from ask_me import __version__

setup(
    name="askme",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "flask>=2.0.2",
        "flask-sqlalchemy>=2.5.1",
        "flask_cors>=3.0.10",
        "click>=8.0.3",
        "gunicorn>=20.1.0",
        "pyjwt>=2.5.0",
    ],
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    url="https://github.com/qzmlgfj/AskMe",
)
