import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="getskin",
    version="1.0.0",
    author="FeelinVoids_",
    author_email="felucca24@gmail.com",
    description="Python module for getting Minecraft skins information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FeelinVoids/getskin",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
