from argparse import ArgumentParser
from pathlib import Path
import re
import requests
import sys
import hashlib

# ! Add support for --output given as filename to be valid
# ? Provides commandline interface support for the script
def parse():
    parser = ArgumentParser(description='URL support for LaTeX')
    parser.add_argument('input', type=Path, help='Input file.')
    parser.add_argument('--output', '-o', type=Path, help='Output file.')
    parser.add_argument('--dump', '-d', type=Path,
                        help='Folder to store the downloaded content.')
    parser.add_argument('--tag', '-t', type=str, nargs='+',
                        default=["includegraphics", "url"],
                        help='LaTeX tags that contain required URLs.')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Flag to download every URL present.')
    parser.add_argument('--force', '-f', action='store_const', default='x',
                        const='w', help='Force overwrite if file already exists.')
    args = parser.parse_args()

    INPUT_FILE = args.input.resolve()
    BASE_DIR = INPUT_FILE.parent
    OUTPUT_FILE = BASE_DIR / f'{INPUT_FILE.stem} TeXURL_out.tex'
    DUMP_DIR = BASE_DIR / '.TeXURL_dump/'

    try:
        open(INPUT_FILE)
    except:
        print(f'{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}')
        sys.exit()

    # ? Use the user's output file (if valid)
    if args.output is not None:
        if args.output.resolve().is_file():
            OUTPUT_FILE = args.output
        else:
            print(f'"{args.output.resolve()}" is not a valid file (or file name).',
                  file=sys.stderr)
            print('Switching to the default instead.', file=sys.stderr)
            print('Default = "{OUTPUT_FILE}")', file=sys.stderr)

    # ? Use the user's dump folder (if valid)
    if args.dump is not None:
        if args.dump.resolve().is_dir():
            DUMP_DIR = args.dump
        else:
            print(f'"{args.dump.resolve()}" is not a valid directory.',
                  file=sys.stderr)
            print('Switching to the default instead.', file=sys.stderr)
            print('Default = "{DUMP_DIR}")', file=sys.stderr)

    return INPUT_FILE, OUTPUT_FILE, DUMP_DIR, args.force, args.all, args.tag


# ? Returns the regex to search for URLs
def get_regex(ALL, TAGS):
    url_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    if not ALL:
        tags_merged = '|'.join(TAGS)
        url_regex = re.compile(r'\\(?:%s){(?P<url>[^}]+)}' % tags_merged)
    return url_regex


# ? Download content and link it
def main():
    INPUT_FILE, OUTPUT_FILE, DUMP_DIR, FORCE, ALL, TAGS = parse()
    url_regex = get_regex(ALL, TAGS)

    try:
        with open(INPUT_FILE, 'r') as f:
            lines = f.readlines()
        DUMP_DIR.mkdir(parents=True, exist_ok=True)

        with open(OUTPUT_FILE, FORCE) as f:
            for line in lines:
                urls = url_regex.findall(line)
                for url in urls:
                    download_name = url.split('/')[-1]
                    with requests.get(url, stream=True) as r:
                        print(DUMP_DIR / download_name)
                print(line, end='', file=f)

    except:
        print(f'{sys.exc_info()[0].__name__}: {sys.exc_info()[1]}')
        sys.exit()

if __name__ == '__main__':
    main()
