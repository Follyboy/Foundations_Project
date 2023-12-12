from setuptools import setup

authors = [
    'Carrie Magee',
    'Alex khater',
    'Folaranmi Adeyeri'
]

setup(
    name='pyjack_foundations',
    version='1.1.0',
    py_modules=['Blackjack'], 
    install_requires=[
        # No external dependencies, since 'random' is part of Python's Standard Library
    ],
    entry_points={
        'console_scripts': [
            'pyjack_foundations = Blackjack:start',
        ],
    },
    author=', '.join(authors),
    author_email='',
    description='Black jack in python',
    license='',
    url='https://github.com/Follyboy/Foundations_Project',
)
