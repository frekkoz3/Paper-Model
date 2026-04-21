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
from src.generator.page import Page, to_jpg
from src.utils import start_server

from pathlib import Path

def generate_train_and_validation_set(
        train_size : int = 1000,
        val_size : int = 100,
        base_path : str = "data",
        img_name : str = "debug",
        directory : str = ".",
        port : int = 8000,
        page_config_path : str = r"configs/config.json"
        ):
    
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

    # starting the server 
    server = start_server(directory, port)

    pages = []

    try:

        img_path = train_img_path / img_name
        lab_path = train_lbl_path / img_name
        html_path = train_html_path / img_name

        for i in range(train_size):
            page = Page(config=page_config_path, html_path=f"{html_path}_{i}.html")
            pages.append(page)
            url = f"http://localhost:{port}/{html_path}_{i}.html"
            to_jpg(page, url = url, o_path=f"{str(img_path)}_{i}.jpg", l_path=f"{str(lab_path)}_{i}.txt")

        img_name = "val"

        img_path = val_img_path / img_name
        lab_path = val_lbl_path / img_name
        html_path = val_html_path / img_name

        for i in range(val_size):
            page = Page(config=page_config_path, html_path=f"{html_path}_{i}.html")
            pages.append(page)
            url = f"http://localhost:{port}/{html_path}_{i}.html"
            to_jpg(page, url = url, o_path=f"{str(img_path)}_{i}.jpg", l_path=f"{str(lab_path)}_{i}.txt")

    finally:
        server.shutdown()

    return pages

if __name__ == '__main__':

    pages = generate_train_and_validation_set(train_size=20, val_size=5)