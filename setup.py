from setuptools import setup
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent
long_description = (BASE_DIR / "README.md").read_text(encoding="utf-8")

setup(
    name="TeXURL",
    version="1.0.0-dev1",
    description="LaTeX Parser for Content Containing URLs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/relaxxpls/TeXURL",
    author="Laxman Desai",
    author_email="desai.laxman2001@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: LaTeX",
    ],
    keywords=["latex", "url", "links", "download", "requests", "parse", "regex", "re"],
    package_dir={"": "src"},
    license="MIT",
    project_urls={
        "Bug Reports": "https://github.com/relaxxpls/TeXURL/issues",
        "Source": "https://github.com/relaxxpls/TeXURL/",
    },
)
