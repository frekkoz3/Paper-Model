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
import json
import random
from src.generator.header import Header
from src.generator.footer import Footer
from src.generator.section import Section
from src.utils import random_datetime

from playwright.sync_api import sync_playwright

from pathlib import Path

from src.utils import make_css_urls_absolute

from src.augmenter.augment import *

import cv2
import numpy as np

class Page:

    def __init__(self, config : str, html_path : str = "output/debug.html", reset_css : bool = False):
        with open(config, "r") as f:
            config = json.load(f)

        self.page_cfg = config["page"]
        self.section_cfg = config["section"]
        self.header_cfg = config["header"]
        self.footer_cfg = config["footer"]
        self.banner_cfg = config["banner"]
        self.article_cfg = config["article"]

        # CSS absolute path handling
        if not Path(self.page_cfg["css_path"]["absolute"]).exists() or reset_css:
            make_css_urls_absolute(self.page_cfg["css_path"]["relative"], self.page_cfg["css_path"]["absolute"], self.page_cfg["root"])
            print(f"Created CSS file with absolute path references. You can find it here at {self.page_cfg['css_path']['absolute']}.")
        self.css_path = Path(self.page_cfg["css_path"]["absolute"]).resolve()

        # PAGE PARAMS
        self.width = self.page_cfg["width"]
        self.height = self.page_cfg["height"]
        self.scale = self.page_cfg["scale"] # this is a good way to improve the quality without changin dimensions but works only in some browsers

        self.header_probability = self.header_cfg["probability"]
        self.footer_probability = self.footer_cfg["probability"]
        self.banner_probability = self.banner_cfg["probability"]

        self.minimum_column_width = self.page_cfg["minimum column width"]
        self.minimum_section_height = self.page_cfg["minimum section height"]
        
        # These margins are not really used, to think if keeping or not them
        self.upper_margin = min(self.page_cfg["upper margin"]["max"], max(self.page_cfg["upper margin"]["min"], random.gauss(mu = self.page_cfg["upper margin"]["mu"], sigma = self.page_cfg["upper margin"]["sigma"])))
        self.lower_margin = min(self.page_cfg["lower margin"]["max"], max(self.page_cfg["lower margin"]["min"], random.gauss(mu = self.page_cfg["lower margin"]["mu"], sigma = self.page_cfg["lower margin"]["sigma"])))
        self.right_margin = min(self.page_cfg["right margin"]["max"], max(self.page_cfg["right margin"]["min"], random.gauss(mu = self.page_cfg["right margin"]["mu"], sigma = self.page_cfg["right margin"]["sigma"])))
        self.left_margin = min(self.page_cfg["left margin"]["max"], max(self.page_cfg["left margin"]["min"], random.gauss(mu = self.page_cfg["left margin"]["mu"], sigma = self.page_cfg["left margin"]["sigma"])))

        self.column_gap = min(self.page_cfg["column margin"]["max"], max(self.page_cfg["column margin"]["min"], random.gauss(mu = self.page_cfg["column margin"]["mu"], sigma = self.page_cfg["column margin"]["sigma"])))
        self.between_section_margin = self.page_cfg["between section margin"] # Not used

        # SECTION PARAMS
        self.recursion_limit = self.section_cfg["recursion limit"]
        self.split_probability = self.section_cfg["split probability"]

        # HEADER PARAMS
        self.header_height_range = self.header_cfg["height"]

        # FOOTER PARAMS
        self.footer_height_range = self.footer_cfg["height"]

        # RANDOM FONT
        self.font = random.choice(self.page_cfg["fonts"])

        self.date = random_datetime()

        self.section_space = {
            "x_min": 0, #self.left_margin,
            "y_min": 0, #self.upper_margin,
            "x_max": self.width, # - self.right_margin,
            "y_max": self.height #- self.lower_margin
        }

        self.generate_header()
        self.generate_footer()
        self.generate_sections()

        self.html_path = html_path

    def generate_header(self):
        self.header = None
        if random.random() < self.header_probability:
            dy = random.randint(*self.header_height_range)
            padding = random.randint(10, 20)
            self.header = Header(self, 0, 0, self.width -2*padding, dy, padding)
            self.section_space["y_min"] += self.header.height
            self.section_space["y_min"] += 2*self.header.padding

    def generate_footer(self):
        self.footer = None
        if random.random() < self.footer_probability:
            dy = random.randint(*self.footer_height_range)
            padding = random.randint(10, 20)
            self.footer = Footer(self, 0, self.height - dy, self.width -2*padding, dy, padding)
            self.section_space["y_max"] -= self.footer.height
            self.section_space["y_max"] -= 2*self.footer.padding

    def generate_sections(self):
        self.section_space_h = self.section_space["y_max"] - self.section_space["y_min"]
        self.sections = Section(
            self,
            self.section_space["x_min"],
            self.section_space["y_min"],
            self.section_space["x_max"] - self.section_space["x_min"],
            self.section_space["y_max"] - self.section_space["y_min"],
            padding = 10,
            recursion_index=0
        ).split()
        for section in self.sections:
            section._generate()

    def render(self):
        header_h = self.header.height if self.header else 0
        footer_h = self.footer.height if self.footer else 0

        

        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="file:///{self.css_path}">
        </head>

        <body style=
        "--body-font:{self.font};
        zoom:{self.scale};">

        <div class="page"
         style="--page-width:{self.width}px; --page-height:{self.height}px;
         --section-space-h : {self.section_space_h}px;">
        """

        if self.header:
            html += self.header.render()

        html += """
        <div class="content">
        """

        for section in self.sections:
            html += section.render()

        html += """
        </div>
        """

        if self.footer:
            html += self.footer.render()

        html += """
        </div>

        </body>
        </html>
        """

        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write(html)

def get_labels_from_page(browser_page, page_width, page_height, l_path: str = "output/debug.txt"):
    """
    Extract object annotations from a rendered HTML page and save them
    in YOLO format.

    The function scans specific DOM elements (header, section, footer,
    section titles, banners and columns) and converts their bounding boxes into
    normalized YOLO annotations:

        class_id x_center y_center width height

    All coordinates are normalized with respect to the full page size.

    Class mapping:
        0 -> Header
        1 -> Section
        2 -> Section Title
        3 -> Column
        4 -> Banner
        5 -> Footer

    Parameters
    ----------
    browser_page : playwright.sync_api.Locator
        Playwright locator pointing to the root page element containing
        the layout (typically ".page").
    page_width : float
        Width of the rendered page in pixels.
    page_height : float
        Height of the rendered page in pixels.
    l_path : str, optional
        Output file path where YOLO annotations will be saved.
        Default is "output/debug.txt".

    Returns
    -------
    None
        The function writes annotations directly to `l_path`.
    """
    annotations = ""

    possible_divs = [".header", ".section", ".footer"]
    class_ids = {
        ".header": 0,
        ".section": 1,
        ".footer": 5
    }

    for div in possible_divs:
        divs = browser_page.locator(div)

        for i in range(divs.count()):
            element = divs.nth(i)
            box = element.bounding_box()

            if box is None:
                continue

            # SECTION LOGIC
            if div == ".section":
                section = element
                title_height = 0

                # ---- Section Title ----
                title = section.locator(".section-title")
                if title.count() > 0:
                    title_box = title.first.bounding_box()

                    if title_box:
                        title_height = title_box["height"]

                        xc = (title_box["x"] + title_box["width"] / 2) / page_width
                        yc = (title_box["y"] + title_box["height"] / 2) / page_height
                        w = title_box["width"] / page_width
                        h = title_box["height"] / page_height

                        annotations += f"2 {xc} {yc} {w} {h}\n"

                # ---- Columns info ----
                cols_var = section.evaluate("""
                (el) => getComputedStyle(el).getPropertyValue('--cols')
                """)

                try:
                    n_columns = int(cols_var.strip())
                except:
                    n_columns = 1

                # ---- Adjusted section (remove title) ----
                adj_y = box["y"] + title_height
                adj_h = box["height"] - title_height

                # ---- Section label ----
                s_xc = (box["x"] + box["width"] / 2) / page_width
                s_yc = (adj_y + adj_h / 2) / page_height
                s_w = box["width"] / page_width
                s_h = adj_h / page_height

                annotations += f"1 {s_xc} {s_yc} {s_w} {s_h}\n"

                # ---- Columns ----
                if n_columns > 0:
                    col_width = (box["width"]) / n_columns

                    for j in range(n_columns):
                        col_x = box["x"] + j * (col_width)

                        xc = (col_x + col_width / 2) / page_width
                        yc = (adj_y + adj_h / 2) / page_height
                        w = col_width / page_width
                        h = adj_h / page_height

                        annotations += f"3 {xc} {yc} {w} {h}\n"

                # --- Banners ---
                banners = section.locator(".banner")

                for i in range(banners.count()):

                    banner = banners.nth(i)

                    banner_box = banner.bounding_box()

                    if banner_box:

                        min_y = (banner_box["y"]) / page_height
                        if min_y > (s_yc + s_h/2): # completely out of border
                            continue
                        else:
                            max_y = min(((banner_box["y"] + banner_box["height"]) / page_height), (s_yc + s_h/2)) # max_y out of border

                            xc = (banner_box["x"] + banner_box["width"] / 2) / page_width
                            yc = (max_y + min_y) / 2
                            w = banner_box["width"] / page_width
                            h =  max_y - min_y

                            annotations += f"4 {xc} {yc} {w} {h}\n"

            # HEADER / FOOTER
            else:
                xc = (box["x"] + box["width"] / 2) / page_width
                yc = (box["y"] + box["height"] / 2) / page_height
                w = box["width"] / page_width
                h = box["height"] / page_height

                annotations += f"{class_ids[div]} {xc} {yc} {w} {h}\n"

    with open(l_path, "w") as f:
        f.write(annotations)

def from_page_to_jpg(page : Page , o_path : str = "output/debug.jpg", l_path : str = "output/debug.txt", save_labes : bool = True, verbose : bool = False):
    """
    Render an HTML page, capture a screenshot, and optionally generate
    corresponding YOLO annotations.

    The function uses Playwright to open the rendered HTML file, capture
    a screenshot of the ".page" element, and optionally extract layout
    annotations via `get_labels_from_page`.

    Parameters
    ----------
    page : Page
        Object istance of the class Page (not already rendered).
    o_path : str, optional
        Output file path for the screenshot image.
        Default is "output/debug.jpg".
    l_path : str, optional
        Output file path for YOLO annotations.
        Used only if `save_labes` is True.
        Default is "output/debug.txt".
    save_labes : bool, optional
        Whether to generate and save YOLO annotations.
        Default is True.

    Returns
    -------
    None

    Side Effects
    ------------
    - Launches a headless Chromium browser instance.
    - Saves a screenshot of the page to `o_path`.
    - Optionally writes annotation labels to `l_path`.

    Notes
    -----
    - The page is loaded via a local file URI.
    - A short timeout is used to ensure rendering stability.
    - Screenshot is taken from the ".page" DOM element only.
    """
    page.render()
    html_path = page.html_path
    html_file = Path(html_path).resolve().as_uri()

    with sync_playwright() as p:

        if verbose:
            print("Working...")

        browser = p.chromium.launch(headless=True)
        browser_page = browser.new_page()
        browser_page.goto(html_file, wait_until="networkidle")
        browser_page.wait_for_timeout(200)  # small buffer
        browser_page.locator(".page").screenshot(path=o_path, quality=100, scale="device")

        if save_labes:
            get_labels_from_page(browser_page=browser_page.locator(".page"), page_width=page.width*page.scale, page_height=page.height*page.scale, l_path=l_path)

        browser.close()

        if verbose:
            print(f"Work done. You can find the jpg result in {o_path}, while the txt result in {l_path}.")

def get_color_from_colormap(class_id, num_classes):
    value = int(255 * class_id / max(1, num_classes - 1))
    color = cv2.applyColorMap(
        np.array([[value]], dtype=np.uint8),
        cv2.COLORMAP_JET
    )[0][0]
    return tuple(int(c) for c in color)

def visualize_labels(img_path : str = "output/debug.jpg", l_path : str = "output/debug.txt", o_path : str = "output/annotated_debug.jpg"):
    """
    Visualize labels annotation.
    Labels are in YOLO notation (class id, x_center, y_center, width, height)
    """
    annotations = []
    with open(l_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                annotations.append(line.split())
    
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not read image at {img_path}")

    h, w, _ = img.shape

    for ann in annotations:
        class_id, x_center, y_center, bw, bh = map(float, ann)

        x_center *= w
        y_center *= h
        bw *= w
        bh *= h

        x1 = int(x_center - bw / 2)
        y1 = int(y_center - bh / 2)
        x2 = int(x_center + bw / 2)
        y2 = int(y_center + bh / 2)

        color = get_color_from_colormap(class_id, 6)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        # Draw class label
        label = f"{int(class_id)}"
        cv2.putText(img, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    cv2.imwrite(o_path, img)

if __name__ == '__main__':
    
    page = Page(config="configs/config.json", reset_css=True)
    from_page_to_jpg(page, verbose=True)
    augment_page()
    visualize_labels()