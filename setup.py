import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="concepttordf",
    version="1.0.0.rc5",
    author="Stig B. Dørmænen",
    author_email="sbd@digdir.no",
    description=(
                 "A small Python library for mapping a concept collection"
                 " to the skos-ap-no specification"
                 ),
    project_urls={
        'Documentation': 'https://Informasjonsforvaltning.github.io/concepttordf',
        'Source': 'https://github.com/Informasjonsforvaltning/concepttordf',
        'Tracker': 'https://github.com/Informasjonsforvaltning/concepttordf/issues'
    },
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
