from setuptools import setup, find_packages

setup(
    name='ghmap',
    version='1.0.0',
    description='GitHub event mapping tool',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    author='Youness Hourri',
    author_email='hourri@yahoo.com',
    url='https://github.com/uhourri/ghmap',
    packages=find_packages(), 
    install_requires=[
        'argparse',  # argparse is needed, as it's not part of the Python standard library in some versions
    ],
    entry_points={  # CLI command configuration
        'console_scripts': [
            'ghmap=src.cli:main',  # Define the command and the main function
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)