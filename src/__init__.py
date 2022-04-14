__author__ = "Laxman Desai"
__date__ = "2021-05-16"
__version__ = "0.1.0"

try:
    from .main import parse, get_regex, chk_url, download_and_link, main

except ImportError:
    from main import parse, get_regex, chk_url, download_and_link, main
