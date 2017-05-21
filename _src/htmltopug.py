#!/usr/bin/env python3
"""
cat file.html | htmltopug.py | xclip -sel clip
Run the clipboard on html2jade.org
xclip -sel clip -o | htmltopug.py -r
"""
from bs4 import BeautifulSoup
import sys, argparse

parser = argparse.ArgumentParser(description="Prepares HTML files for conversion to pug, because all existing converters are bad")
parser.add_argument("-r", "--after", action="store_true", required=False)
args = parser.parse_args()

replace_dict = {
    " ": "THISWASASPACEBUTISNTANYMORE",
    "\t": "THISWASATABBUTISNTANYMORE",
    "\n": "THISWASANEWLINEBUTISNTANYMORE",
}

pre_replace = "preReplacement"

if args.after:
    val = sys.stdin.read().replace(pre_replace, "pre")
    for key, value in replace_dict.items():
        val = val.replace(value, key)
    print(val)
else:
    soup = BeautifulSoup(sys.stdin.read().replace("\r", ""), "lxml")
    for tag in soup.find_all("pre"):
        tag.name = pre_replace
    for tag in soup.find_all("font"):
        tag.unwrap()
    for tag in soup.find_all("code"):
        val = tag.text
        for key, value in replace_dict.items():
            val = val.replace(key, value)
        tag.string = val
    print(soup.prettify())
