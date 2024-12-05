from setuptools import setup, find_packages

setup(
    name="ghmap", 
    version="1.0.0",
    description="A tool to process GitHub events into structured actions and activities",
    long_description=open("README.md", "r", encoding="utf-8").read(),  # README as long description
    long_description_content_type="text/markdown",
    author="Youness Hourri",
    author_email="hourri@yahoo.com",
    url="https://github.com/uhourri/ghmap",  # GitHub URL
    license="MIT",
    packages=find_packages(where="src"),  # Automatically find packages in the `src` folder
    package_dir={"": "src"},  # Define the root source directory
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        # Add any dependencies your project requires
    ],
    entry_points={
        "console_scripts": [
            "ghmap=cli:main",  # Maps the `ghmap` command to `src/cli.py`
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)