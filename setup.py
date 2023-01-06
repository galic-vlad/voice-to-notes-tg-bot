#!/usr/bin/env python
"""The setup script."""
from pathlib import Path

from setuptools import find_packages, setup

# readme = Path('README.rst').read_text().strip()
# history = Path('HISTORY.rst').read_text().strip()
VERSION = Path('VERSION').read_text().strip()


def is_link(url):
    prefixes = ('http', 'git:', 'git+')
    return url.strip().startswith(prefixes)


def parse_requirements(file):
    lines = (line.strip() for line in Path(file).read_text().split('\n'))
    return [line for line in lines if line and not line.startswith("#")]


def get_requirements(*filenames):
    return [
        require
        for filename in filenames
        for require in parse_requirements(filename)
        if not (is_link(require) or require.startswith('-'))
    ]


def get_links(filename):
    return [
        require
        for require in parse_requirements(filename)
        if is_link(require)
    ]


setup(
    name='voice-to-notes-tg-bot',
    version=VERSION,
    packages=find_packages(include=['tgbot', 'tgbot.*']),
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
    ],
    description="Telegram bot to parse voice messages and\n "
                "convert them into text notes for\n "
                "future export to Markdown files.",
    install_requires=get_requirements('requirements.txt'),
    dependency_links=get_links('requirements.txt'),
    long_description="",  # readme + '\n\n' + history,
    include_package_data=True,

    keywords='tgbot',
    zip_safe=False,
)
