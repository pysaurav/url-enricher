import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'enricher'
AUTHOR = 'Saurav'
AUTHOR_EMAIL = 'pysaurav@gmail.com'
URL = 'https://github.com/you/your_package'
LICENSE = 'Apache License 2.0'
DESCRIPTION = 'To enrich urls for all companies'
LONG_DESCRIPTION = 'This package will take your company name and enriches url for all the company names'
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ["bs4", "requests_html",
                    "tldextract", "requests", "google"]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      keywords=['urlenricher', 'company enricher'],
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
