import re
import requests
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='URL support for LaTeX')

# Positional arguments
parser.add_argument('input', type=Path, help='Input file')

# Optional arguments
parser.add_argument('--output', '-o', type=Path, default='TeXURL_output.tex', help='Output file')
parser.add_argument('--dump', '-d', type=Path, default='.TeXURL_dump',
                    help='Folder to store the downloaded content.')
parser.add_argument('--all', '-a', action='store_true',
                    help='Flag to download every URL present')
parser.add_argument('--tag', '-t', type=str, nargs='+', default=["includegraphics", "url"],
                    help='LaTeX tags that contain required URLs')

args = parser.parse_args()

BASE_DIR = Path(args.input).resolve().parent
args.dump = BASE_DIR / args.dump
print(args.dump)
print(BASE_DIR)

# ----------- regex
url_regex = re.compile(
    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
if(args.all == False):
    tags_merged = '|'.join(args.tag)
    url_regex = re.compile(r'\\(?:%s){(?P<url>[^}]+)}' % tags_merged)

# ----------- download & link
with open(args.input) as f:
    text = f.read()
    
urls = url_regex.findall(text)

# ----------- testing
# print(len(urls))
# print("Urls: ", urls)


# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
# args = parser.parse_args()
# print(args.accumulate(args.integers))
