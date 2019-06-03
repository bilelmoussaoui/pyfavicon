import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyfavicon",
    version="0.0.1",
    author="Bilal Elmoussaoui",
    author_email="bil.elmoussaoui@gmail.com",
    description="An async favicon fetcher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/bilelmoussaoui/pyfavicon",
    packages=['pyfavicon'],
    install_requires=[
        'aiohttp',
        'beautifulsoup4',
        'Pillow'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Utilities',
        'Topic :: Internet :: WWW/HTTP',
    ],
    tests_require=[
        'pytest',
        'python-coveralls',
        'pytest-cov'
    ],
    test_suite='tests',
)