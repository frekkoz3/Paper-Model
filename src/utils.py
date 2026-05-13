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

import csv
import hashlib
import requests
from urllib.parse import urlparse

from concurrent.futures import ThreadPoolExecutor, as_completed

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

def download_one(url, output_dir, timeout=10, chunk_size=1024, index=0):
    try:
        response = requests.get(url, stream=True, timeout=timeout)
        if response.status_code != 200:
            return (url, False)

        content_type = response.headers.get("Content-Type", "")

        path = urlparse(url).path
        name = os.path.basename(path)

        if not name or "." not in name:
            name = hashlib.md5(url.encode()).hexdigest()
            if "png" in content_type:
                name += ".png"
            elif "webp" in content_type:
                name += ".webp"
            else:
                name += ".jpg"

        file_path = Path(output_dir) / name

        if file_path.exists():
            file_path = file_path.with_stem(file_path.stem + f"_{index}")

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

        return (url, True)

    except Exception:
        return (url, False)


def download_300x250_parallel(
    n_imgs : int | None = None,
    url_column=0,
    max_workers=16
):
    def find_project_root(marker="src"):
        path = Path(__file__).resolve()
        for parent in path.parents:
            if (parent / marker).exists():
                return parent
        raise RuntimeError("Project root not found")

    BASE_DIR = find_project_root()
    RESOURCES_DIR = BASE_DIR / "resources"

    csv_path = RESOURCES_DIR / "banners_links_300_250.csv"
    output_dir = RESOURCES_DIR / "300x250"
    url_column = 0

    output_dir.mkdir(parents=True, exist_ok=True)

    urls = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                url = row[url_column].strip()
                if url:
                    urls.append(url)
                if n_imgs:
                    if len(urls) >= n_imgs:
                        break
            except Exception:
                continue

    results = {"success": 0, "failed": 0}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(download_one, url, output_dir, 10, 1024, i)
            for i, url in enumerate(urls)
        ]

        for future in as_completed(futures):
            url, ok = future.result()
            if ok:
                results["success"] += 1
            else:
                results["failed"] += 1

    return results

if __name__ == '__main__':

    download_300x250_parallel()