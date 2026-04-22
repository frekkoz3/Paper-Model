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
from src.generator.page import Page, get_labels
from playwright.sync_api import sync_playwright

import argparse

from pathlib import Path

from tqdm import tqdm

def generate_train_and_validation_set(
        train_size : int = 1000,
        val_size : int = 100,
        base_path : str = "data",
        img_name : str = "debug",
        directory : str = ".",
        page_config_path : str = r"configs/config.json",
        base_index : int = 0,
        verbose : int = 0
        ):
    """
    verbose :
        - 0 = False (do not show anything)
        - 1 = True (just using print)
        - 2 = True with tqdm
    """
    
    base_path = Path(base_path)

    train_img_path = base_path / "images/train"
    train_lbl_path = base_path / "labels/train"
    train_html_path = base_path / "html/train"

    val_img_path = base_path / "images/val"
    val_lbl_path = base_path / "labels/val"
    val_html_path = base_path / "html/val"

    train_img_path.mkdir(parents=True, exist_ok=True)
    train_lbl_path.mkdir(parents=True, exist_ok=True)
    train_html_path.mkdir(parents=True, exist_ok=True)
    val_img_path.mkdir(parents=True, exist_ok=True)
    val_lbl_path.mkdir(parents=True, exist_ok=True)
    val_html_path.mkdir(parents=True, exist_ok=True)

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)
            browser_page = browser.new_page()

            img_path = train_img_path / img_name
            lab_path = train_lbl_path / img_name
            html_path = train_html_path / img_name

            if verbose == 1:
                print("Starting generating training set")

            for i in tqdm(range(train_size), desc="Generating training set", disable=(verbose==0 or verbose == 1)):

                idx = i + base_index

                page = Page(config=page_config_path, html_path=f"{html_path}_{idx}.html")
                page.render()

                html_file = Path(f"{html_path}_{idx}.html").resolve().as_uri()

                browser_page.goto(html_file, wait_until="networkidle")
                
                browser_page.wait_for_timeout(200)  # small buffer

                browser_page.locator(".page").screenshot(path=f"{img_path}_{idx}.jpg", quality=100, scale="device")
                get_labels(browser_page=browser_page.locator(".page"), page_width=page.width*page.scale, page_height=page.height*page.scale, l_path=f"{str(lab_path)}_{idx}.txt")

            if verbose == 1:
                print("Finished generating trainig set")
                print("----------------------------------------")
                print("Starting generating validation set")

            img_name = "val"

            img_path = val_img_path / img_name
            lab_path = val_lbl_path / img_name
            html_path = val_html_path / img_name

            for i in tqdm(range(val_size), desc="Generating validation set", disable=(verbose==0 or verbose == 1)):

                idx = i + base_index

                page = Page(config=page_config_path, html_path=f"{html_path}_{idx}.html")
                page.render()

                html_file = Path(f"{html_path}_{idx}.html").resolve().as_uri()

                browser_page.goto(html_file, wait_until="networkidle")
                
                browser_page.wait_for_timeout(200)  # small buffer

                browser_page.locator(".page").screenshot(path=f"{img_path}_{idx}.jpg", quality=100, scale="device")
                get_labels(browser_page=browser_page.locator(".page"), page_width=page.width*page.scale, page_height=page.height*page.scale, l_path=f"{str(lab_path)}_{idx}.txt")

            browser_page.close()

            if verbose ==  1:
                print("Finished generating validation set")
                print("---------------------------")

    except Exception as e:
        print(e)
        raise

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate dataset (train + val)")

    parser.add_argument("--train_size", type=int, default=10)
    parser.add_argument("--val_size", type=int, default=1)
    parser.add_argument("--base_index", type=int, default=0)
    parser.add_argument("--base_path", type=str, default="data")
    parser.add_argument("--img_name", type=str, default="debug")
    parser.add_argument("--directory", type=str, default=".")
    parser.add_argument("--config", type=str, default="configs/config.json")
    parser.add_argument("--verbose", type=int, default=2)

    args = parser.parse_args()

    generate_train_and_validation_set(
        train_size=args.train_size,
        val_size=args.val_size,
        base_path=args.base_path,
        directory=args.directory,
        img_name=args.img_name,
        page_config_path=args.config,
        base_index=args.base_index, 
        verbose = args.verbose
    )