from setuptools import setup, find_packages

setup(
    name="dissmodel",
    version="0.1.0",
    author="Sérgio Costa",
    description="dissmodel - Discrete Spatial Modeling",
    long_description=open("readme.md").read(),
    packages=find_packages(),
    install_requires=["numpy>=1.25.0"],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
