from setuptools import setup, find_packages

setup(
    name="gnl_api_framework",
    version="0.1.0",
    author="EAShibby",
    author_email="eashibby@gmx.de",
    description="A description of your framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Warcraft-Gym/api_framework",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "requests",
        "PyJWT"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.13',
)
