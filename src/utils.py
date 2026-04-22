r"""
     _____                        __  __           _      _ 
    |  __ \                      |  \/  |         | |    | |
    | |__) |_ _ _ __   ___ _ __  | \  / | ___   __| | ___| |
    |  ___/ _` | '_ \ / _ \ '__| | |\/| |/ _ \ / _` |/ _ \ |
    | |  | (_| | |_) |  __/ |    | |  | | (_) | (_| |  __/ |
    |_|   \__,_| .__/ \___|_|    |_|  |_|\___/ \__,_|\___|_|
                | |                                          
                |_|                         

    A simple rule-based model to generate realistical newspapers' pages for the training of the YOLO-Layout model.
"""
import random
from datetime import datetime, timedelta

import os
import shutil

import re
from pathlib import Path

MIN_YEAR = 1600
MAX_YEAR = 2026

def random_datetime():
    # generate a random datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(MIN_YEAR, 1, 1, 00, 00, 00)
    years = MAX_YEAR - MIN_YEAR + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

def clean_folder(folder="data/"):

    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)

        if os.path.isdir(item_path):
            shutil.rmtree(item_path)

def make_css_urls_absolute(input_css_path: str, output_css_path: str, root_dir: str):

    input_css_path = Path(input_css_path).resolve()
    output_css_path = Path(output_css_path).resolve()
    root_dir = Path(root_dir).resolve()

    css_text = input_css_path.read_text(encoding="utf-8")

    # regex to match url(...)
    url_pattern = re.compile(r'url\((.*?)\)', re.IGNORECASE)

    def replace_url(match):
        raw = match.group(1).strip().strip('"').strip("'")

        # Resolve relative path
        abs_path = Path(f"{root_dir}{raw}")

        if not abs_path.exists():
            print(f"[WARNING] File not found: {abs_path}")

        return f'url("{abs_path.as_uri()}")'

    new_css = url_pattern.sub(replace_url, css_text)

    output_css_path.write_text(new_css, encoding="utf-8")

if __name__ == '__main__':

    make_css_urls_absolute("css/relative style.css", "css/absolute style.css", ".")