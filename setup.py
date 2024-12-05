from setuptools import setup, find_packages

setup(
    name="ghmap", 
    version="1.0.0",
    description="A tool to process GitHub events into structured actions and activities",
    long_description=open("README.md", "r", encoding="utf-8").read(),  # Load README content
    long_description_content_type="text/markdown",  # Specify README format
    author="Youness Hourri",
    author_email="hourri@yahoo.com", 
    url="https://github.com/uhourri/ghmap", 
    license="MIT", 
    packages=find_packages(where="src"), 
    package_dir={"": "src"}, 
    include_package_data=True, 
    install_requires=[],
    entry_points={
        "console_scripts": [
            "ghmap=src.cli:main",  # Directly refer to `cli.py` within the top-level package
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8", 
    keywords="github events actions activities mining", 
)