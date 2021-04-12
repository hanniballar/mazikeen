import setuptools
import mazikeen.version

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
with open("LICENSE", "r", encoding="utf-8") as fh:
    LICENSE = fh.read()

setuptools.setup(
    name="mazikeen",
    version=mazikeen.version.__version__,
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
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities"
    ],
    packages=["mazikeen"],
    install_requires=["junit_xml>=1.8", "pyyaml>=5.4.1"],
    entry_points={"console_scripts": ["mazikeen=mazikeen.__main__:main"]},
)