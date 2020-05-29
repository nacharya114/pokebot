import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pokebot-nacharya114", # Replace with your own username
    version="0.0.1",
    author="Neil Acharya, Leo Medrano, Colin",
    author_email="nacharya114@gmail.com",
    description="A package for interacting with poke_env to create a Pokemon Showdown agent.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nacharya114/pokebot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)