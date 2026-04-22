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
from src.utils import random_datetime, start_server

from playwright.sync_api import sync_playwright

from pathlib import Path

from src.utils import make_css_urls_absolute

class Page:

    def __init__(self, config : str, html_path : str = "output/debug.html"):
        with open(config, "r") as f:
            config = json.load(f)

        page_cfg = config["page"]
        section_cfg = config["section"]
        header_cfg = config["header"]
        footer_cfg = config["footer"]
        banner_cfg = config["banner"]

        # CSS
        if not Path(page_cfg["css_path"]["absolute"]).exists():
            make_css_urls_absolute(page_cfg["css_path"]["relative"], page_cfg["css_path"]["absolute"], page_cfg["root"])
            print(f"Created CSS file with absolute path references. You can find it here at {page_cfg["css_path"]["absolute"]}.")
        self.css_path = Path(page_cfg["css_path"]["absolute"]).resolve()

        # PAGE PARAMS
        self.width = page_cfg["width"]
        self.height = page_cfg["height"]
        self.scale = page_cfg["scale"] # this is a good way to improve the quality without changin dimensions but works only in some browsers

        self.header_probability = header_cfg["probability"]
        self.footer_probability = footer_cfg["probability"]
        self.banner_probability = banner_cfg["probability"]

        self.minimum_column_width = page_cfg["minimum column width"]
        self.minimum_section_height = page_cfg["minimum section height"]
        
        # These margins are not really used, to think if keeping or not them
        self.upper_margin = min(page_cfg["upper margin"]["max"], max(page_cfg["upper margin"]["min"], random.gauss(mu = page_cfg["upper margin"]["mu"], sigma = page_cfg["upper margin"]["sigma"])))
        self.lower_margin = min(page_cfg["lower margin"]["max"], max(page_cfg["lower margin"]["min"], random.gauss(mu = page_cfg["lower margin"]["mu"], sigma = page_cfg["lower margin"]["sigma"])))
        self.right_margin = min(page_cfg["right margin"]["max"], max(page_cfg["right margin"]["min"], random.gauss(mu = page_cfg["right margin"]["mu"], sigma = page_cfg["right margin"]["sigma"])))
        self.left_margin = min(page_cfg["left margin"]["max"], max(page_cfg["left margin"]["min"], random.gauss(mu = page_cfg["left margin"]["mu"], sigma = page_cfg["left margin"]["sigma"])))

        self.column_gap = min(page_cfg["column margin"]["max"], max(page_cfg["column margin"]["min"], random.gauss(mu = page_cfg["column margin"]["mu"], sigma = page_cfg["column margin"]["sigma"])))
        self.between_section_margin = page_cfg["between section margin"] # Not used

        # SECTION PARAMS
        self.recursion_limit = section_cfg["recursion limit"]
        self.split_probability = section_cfg["split probability"]

        # HEADER PARAMS
        self.header_height_range = header_cfg["height"]

        # FOOTER PARAMS
        self.footer_height_range = footer_cfg["height"]

        # RANDOM FONT
        self.font = random.choice(page_cfg["fonts"])

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
            self.header = Header(self, 0, 0, self.width, dy, 10)
            self.section_space["y_min"] += self.header.height

    def generate_footer(self):
        self.footer = None
        if random.random() < self.footer_probability:
            dy = random.randint(*self.footer_height_range)
            self.footer = Footer(self, 0, self.height - dy, self.width, dy, 10)
            self.section_space["y_max"] -= self.footer.height

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
         --header-h: {header_h}px; --footer-h: {footer_h}px;
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

def get_labels(browser_page, page_width, page_height, l_path: str = "output/debug.txt"):
    """
    Save labels in YOLO format:
    class_id x_center y_center width height (normalized)

    Class IDs:
    0 -> Header
    1 -> Section
    2 -> Section Title
    3 -> Column
    4 -> Footer
    """

    annotations = ""

    possible_divs = [".header", ".section", ".footer"]
    class_ids = {
        ".header": 0,
        ".section": 1,
        ".footer": 4
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
                xc = (box["x"] + box["width"] / 2) / page_width
                yc = (adj_y + adj_h / 2) / page_height
                w = box["width"] / page_width
                h = adj_h / page_height

                # annotations += f"1 {xc} {yc} {w} {h}\n" # we do not need it 

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

            # HEADER / FOOTER
            else:
                xc = (box["x"] + box["width"] / 2) / page_width
                yc = (box["y"] + box["height"] / 2) / page_height
                w = box["width"] / page_width
                h = box["height"] / page_height

                annotations += f"{class_ids[div]} {xc} {yc} {w} {h}\n"

    with open(l_path, "w") as f:
        f.write(annotations)

# this is deprecated. must be updated with removing the server
def to_jpg(page : Page , url : str = "http://localhost:8000/output/debug.html", o_path : str = "output/debug.jpg", l_path : str = "output/debug.txt", save_labels : bool = True):

    page.render()

    URL = url

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        browser_page = browser.new_page()
        browser_page.goto(URL, wait_until="load")
        browser_page.wait_for_function("document.fonts.ready") # probably this is the culprit
        browser_page.add_style_tag(content="""
            html, body {
                margin: 0;
                padding: 0;
            }
        """)
        browser_page.locator(".page").screenshot(path=o_path, quality=100, scale="device")
        if save_labels:
            get_labels(browser_page=browser_page.locator(".page"), page_width=page.width*page.scale, page_height=page.height*page.scale, l_path=l_path)
        browser.close()

# this will become deprecated
def generate_random_page(save_jpg: bool = True, directory : str = ".", port : int = 8000, page_config_path : str = r"configs/config.json", url_path: str = "output/debug.html", o_path: str = "output/debug", l_path : str = "output/debug.txt", save_labels : bool = True, n_images: int = 1):
    """
    Generates one or more pages.
    
    - If save_jpg=True → saves images
    - o_path is treated as a prefix when n_images > 1
    """

    pages = []

    directory = directory
    port = port
    url = f"http://localhost:{port}/{url_path}"

    server = None
    if save_jpg:
        server = start_server(directory, port)

    try:
        for i in range(n_images): # adding the progress bar maybe

            page = Page(config=page_config_path)
            pages.append(page)

            if save_jpg:
                if n_images == 1:
                    img_path = f"{o_path}.jpg"
                else:
                    img_path = f"{o_path}{i}.jpg"

                to_jpg(page, url=url, o_path=img_path, l_path=l_path, save_labels=True)

    finally:
        if server:
            server.shutdown()

    return pages if n_images > 1 else pages[0]

if __name__ == '__main__':
    
    generate_random_page()