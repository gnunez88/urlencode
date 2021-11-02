#!/usr/bin/env python3
# coding: utf-8

import argparse
import base64
import pyperclip
import re
import sys
from urllib.parse import quote, unquote

php_codes = {
    '%20': '+',
    '%21': '!',
    '%22': '"',
    '%26': '&',
    '%28': '(',
    '%29': ')',
    '%3c': '<',
    '%3d': '=',
    '%3e': '>'
}

def php_urlencode(input_code:str, php_codes=php_codes) -> str:
    code = input_code
    for key in php_codes.keys():
        code = re.sub(key, php_codes[key], code, re.I)
    return code

def php_urldecode(input_str:str, php_codes=php_codes) -> str:
    string = input_str
    codes_php = dict(zip(php_codes.values(), php_codes.keys()))
    for key in codes_php.keys():
        string = re.sub(key, codes_php[key], string, re.I)
    return string

def base64_urlencode(input_code:str) -> str:
    decoded = base64.b64decode(input_code).decode('utf-8')
    return decoded

def main(args):

    if args.decode:
        payload = args.payload
        if args.php:
            payload = php_urldecode(payload)
        output = unquote(payload)
    else:
        if args.base64:
            output = quote(base64_urlencode(args.payload))
        else:
            output = quote(args.payload)
        if args.php:
            output = php_urlencode(output)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)

    if args.copy:
        pyperclip.copy(output)

    if not args.quiet:
        print(output)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'payload',
        nargs='?',
        type=str,
        default=(None if sys.stdin.isatty() else sys.stdin.read()),
        help="Text to encode/decode")
    parser.add_argument('-d', '--decode', help="Decoding mode", action='store_true')
    parser.add_argument('-i', '--input', help="File to get the input from")
    parser.add_argument('-o', '--output', help="File to store the output")
    parser.add_argument('-q', '--quiet', help="Quiet mode", action='store_true')
    parser.add_argument('-b', '--base64', help="Input encoded in base64", action='store_true')
    parser.add_argument('-php', help="PHP URL code", action='store_true')
    parser.add_argument('-c', '--copy', help="Copy in clipboard", action='store_true')

    args = parser.parse_args()
    main(args)
