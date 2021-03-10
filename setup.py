import setuptools

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
with open("LICENSE", "r", encoding="utf-8") as fh:
    LICENSE = fh.read()

setuptools.setup(
    name="mazikeen",
    version="1.0.0",
    author="Neagă Septimiu",
    author_email="neagas@gmail.com",
    description="Test enviroment for CLI application",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/hanniballar/mazikeen",
    project_urls={
        "Bug Tracker": "https://github.com/hanniballar/mazikeen/issues",
    },
    license_file = LICENSE,
    license="Unlicense",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    packages=["mazikeen"],
    install_requires=["junit_xml", "pyyaml"],
    entry_points={"console_scripts": ["mazikeen=mazikeen.__main__:main"]},
)