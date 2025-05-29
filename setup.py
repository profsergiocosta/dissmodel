from setuptools import setup, find_packages

setup(
    name="dissmodel",
    version="0.1.2b",
    author="Sérgio Costa, Nerval Santos Junior",
    description="dissmodel - Discrete Spatial Modeling",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LambdaGeo/dissmodel",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.25.0",
        # Outras dependências aqui
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # Inclui dados extra do MANIFEST.in
)
