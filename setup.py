import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concepttordf-stigbd",
    version="0.1.4",
    author="Stig B. Dørmænen",
    author_email="stigbd@gmail.com",
    description=(
                 "A small Python library for mapping a concept collection"
                 "to the skos-ap-no specification"
                 ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Informasjonsforvaltning/concepttordf",
    packages=setuptools.find_packages(),
    install_requires=[
        'rdflib',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
