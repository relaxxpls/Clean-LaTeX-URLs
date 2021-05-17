from argparse import ArgumentParser
from pathlib import Path
import re
import requests
import sys

# ----------- TeXURL CLI
parser = ArgumentParser(description='URL support for LaTeX')

# Positional arguments
parser.add_argument('input', type=Path, help='Input file')

# Optional arguments
parser.add_argument('--output', '-o', type=Path, help='Output file')
parser.add_argument('--dump', '-d', type=Path,
                    help='Folder to store the downloaded content.')
parser.add_argument('--all', '-a', action='store_true',
                    help='Flag to download every URL present')
parser.add_argument('--tag', '-t', type=str, nargs='+',
                    default=["includegraphics", "url"],
                    help='LaTeX tags that contain required URLs')

args = parser.parse_args()

INPUT_FILE = args.input.resolve()
BASE_DIR = INPUT_FILE.parent
INPUT_FILE_NAME = INPUT_FILE.name
INPUT_FILE_STEM = INPUT_FILE.stem
OUTPUT_FILE = BASE_DIR / f'{INPUT_FILE_STEM} TeXURL_out.tex'
DUMP_DIR = BASE_DIR / '.TeXURL_dump/'
ALL = args.all
TAGS = args.tag

if INPUT_FILE.is_file() == False:
    raise FileNotFoundError(
        'No file named "%s" was found at "%s"' % (INPUT_FILE_NAME, BASE_DIR))

# Use the user's output file if its valid
if args.output is not None:
    if args.output.resolve().is_file():
        OUTPUT_FILE = args.output
    else:
        print(f'''"{args.output.resolve()}" is not a valid file (or file name).
Switching to the default instead.
Default = "{OUTPUT_FILE}")''', file=sys.stderr)
        
if args.dump is not None:
    if args.dump.resolve().is_dir():
        DUMP_DIR = args.dump
    else:
        print(f'''"{args.dump.resolve()}" is not a valid directory.
Switching to the default instead.
Default = "{DUMP_DIR}")''', file=sys.stderr)

# ----------- search for URLs via regex
url_regex = re.compile(
    'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
if not ALL:
    tags_merged = '|'.join(TAGS)
    url_regex = re.compile(r'\\(?:%s){(?P<url>[^}]+)}' % tags_merged)


# ----------- download & link
try:
    with open(INPUT_FILE) as f:
        text = f.read()
    
    urls = url_regex.findall(text)

except IOError:
    print('No file named "%s" was found at "%s"' % (INPUT_FILE_NAME, BASE_DIR))