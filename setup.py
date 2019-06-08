from os import path
from setuptools import setup, find_packages

this = path.abspath(path.dirname(__file__))
with open(path.join(this, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='telegrambot-py',
    version='0.0.1',
    description='Make your own telegram bot easily',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Do Hoerin',
    author_email='lyn@lynlab.co.kr',
    url='https://github.com/hellodhlyn/telegrambot-py',
    python_requires='>=3.5',
    packages= ['telegrambot'],
    install_requires=[
        'python-telegram-bot>=11.1.0,<12.0.0',
    ],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
