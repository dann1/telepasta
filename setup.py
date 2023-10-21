from setuptools import setup, find_packages

setup(
    name='telepasta',
    version='0.1.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'bs4',
        'requests',
        'python-telegram-bot',
        'pyyaml'
    ],
    entry_points={
        'console_scripts': [
            'telepasta=telepasta.bot:run_bot_wrapper',
        ],
    },
    author='Daniel Clavijo Coca',
    description='A Currency Scrapper Telegram Bot',
    license='GPL-3.0',
    keywords="telegram bot currency exchange rate",
    url='http://github.com/dann1/telepasta',
)
