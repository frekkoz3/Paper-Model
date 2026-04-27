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
from src.generator.page import Page, get_labels_from_page
from playwright.sync_api import sync_playwright
from src.augmenter.augment import augment_page

from pathlib import Path
from tqdm import tqdm

import argparse

def generate_train_and_validation_set(
        train_size : int = 1000,
        val_size : int = 100,
        base_path : str = "data",
        img_name : str = "debug",
        page_config_path : str = r"configs/config.json",
        base_index : int = 0,
        augment : bool = True,
        verbose : int = 0
        ):
    """
    Generate a synthetic dataset for YOLO training and validation.

    This function creates HTML pages, renders them in a headless browser,
    captures screenshots, and produces corresponding YOLO annotation files.
    The dataset is split into training and validation subsets and stored
    in a structured directory layout.

    Directory structure created under `base_path`:
        - images/train, images/val
        - labels/train, labels/val
        - html/train, html/val

    Each sample consists of:
        - An HTML file (rendered layout)
        - A JPG screenshot of the page
        - A TXT file with YOLO annotations

    Parameters
    ----------
    train_size : int, optional
        Number of training samples to generate. Default is 1000.
    val_size : int, optional
        Number of validation samples to generate. Default is 100.
    base_path : str, optional
        Root directory where the dataset will be stored.
        Subdirectories are created automatically. Default is "data".
    img_name : str, optional
        Base name used for generated training images and labels.
        The final filename is suffixed with an index. Default is "debug".
    page_config_path : str, optional
        Path to the JSON configuration file used to generate pages.
        This is passed to the `Page` constructor. Default is "configs/config.json".
    base_index : int, optional
        Starting index for file naming. Useful for dataset continuation
        or avoiding overwrites. Default is 0.
    verbose : int, optional
        Controls logging and progress display:
            - 0 : no output
            - 1 : basic print statements
            - 2 : progress bars using tqdm
        Default is 0.

    Returns
    -------
    None

    Side Effects
    ------------
    - Creates directories under `base_path` if they do not exist.
    - Writes HTML files, JPG images, and YOLO TXT label files to disk.
    - Launches a headless Chromium browser via Playwright.

    Notes
    -----
    - Each page is rendered locally and loaded via a file URI.
    - A short delay is introduced after page load to ensure stable rendering.
    - The same browser instance is reused for efficiency.
    - Validation samples use "val" as the base filename instead of `img_name`.

    Raises
    ------
    Exception
        Propagates any exception encountered during dataset generation
        after printing the error message.
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
                get_labels_from_page(browser_page=browser_page.locator(".page"), page_width=page.width*page.scale, page_height=page.height*page.scale, l_path=f"{str(lab_path)}_{idx}.txt")

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
                get_labels_from_page(browser_page=browser_page.locator(".page"), page_width=page.width*page.scale, page_height=page.height*page.scale, l_path=f"{str(lab_path)}_{idx}.txt")

                if augment:
                    augment_page(img_path=f"{img_path}_{idx}.jpg", l_path=f"{str(lab_path)}_{idx}.txt")
                    
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
    parser.add_argument("--config", type=str, default="configs/config.json")
    parser.add_argument("--augment", type=bool, default=True)
    parser.add_argument("--verbose", type=int, default=2)

    args = parser.parse_args()

    generate_train_and_validation_set(
        train_size=args.train_size,
        val_size=args.val_size,
        base_path=args.base_path,
        img_name=args.img_name,
        page_config_path=args.config,
        base_index=args.base_index, 
        augment=args.augment,
        verbose = args.verbose
    )