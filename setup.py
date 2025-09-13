from setuptools import setup, find_packages

# Read the README.md for PyPI long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PetroMap",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "scipy",
        "plotly",
        "scikit-learn"
    ],
    author="Nashat Jumaah Omar",
    description="A Contour Mapping Utility for Oil and Gas Engineers",
    long_description=long_description,
    long_description_content_type="text/markdown",  # <-- This is important
    url="https://github.com/Nashat90/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
