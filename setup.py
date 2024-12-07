from setuptools import setup, find_packages

setup(
    name="sql_upsert",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=1.4.0",
        "pandas>=1.0.0"
    ],
    author="vile319",
    author_email="vile319@gmail.com",
    description="A package for handling SQL upsert operations with pandas DataFrames",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vile319/sql_upsert",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 