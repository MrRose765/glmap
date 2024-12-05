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
        'argparse',  
        'os', 
        'shutil',  
        'json', 
    ],
    entry_points={  # CLI command configuration
        'console_scripts': [
            'ghmap=src.cli:main', 
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6', 
)