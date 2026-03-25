"""
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

class Page:

    def __init__(self, config : str):
        with open(config, "r") as f:
            config = json.load(f)

        page_cfg = config["page"]
        section_cfg = config["section"]
        header_cfg = config["header"]
        footer_cfg = config["header"]

        # PAGE PARAMS
        self.width = page_cfg["width"]
        self.height = page_cfg["height"]

        self.header_probability = page_cfg["header probability"]
        self.footer_probability = page_cfg["footer probability"]

        self.minimum_column_width = page_cfg["minimum column width"]
        self.minimum_section_height = page_cfg["minimum section height"]

        self.upper_margin = min(page_cfg["upper margin"]["max"], max(page_cfg["upper margin"]["min"], random.gauss(mu = page_cfg["upper margin"]["mu"], sigma = page_cfg["upper margin"]["sigma"])))
        self.lower_margin = min(page_cfg["lower margin"]["max"], max(page_cfg["lower margin"]["min"], random.gauss(mu = page_cfg["lower margin"]["mu"], sigma = page_cfg["lower margin"]["sigma"])))
        self.right_margin = min(page_cfg["right margin"]["max"], max(page_cfg["right margin"]["min"], random.gauss(mu = page_cfg["right margin"]["mu"], sigma = page_cfg["right margin"]["sigma"])))
        self.left_margin = min(page_cfg["left margin"]["max"], max(page_cfg["left margin"]["min"], random.gauss(mu = page_cfg["left margin"]["mu"], sigma = page_cfg["left margin"]["sigma"])))

        self.column_margin = page_cfg["column margin"]
        self.between_section_margin = page_cfg["between section margin"] # remember this is the parameter for a truncated gaussian

        # SECTION PARAMS
        self.recursion_limit = section_cfg["recursion limit"]
        self.split_probability = section_cfg["split probability"]

        # HEADER PARAMS
        self.header_height_range = header_cfg["height"]

        # FOOTER PARAMS
        self.footer_height_range = footer_cfg["height"]

        self.date = random_datetime()

        self.section_space = {
            "x_min": self.left_margin,
            "y_min": self.upper_margin,
            "x_max": self.width - self.right_margin,
            "y_max": self.height - self.lower_margin
        }

        self.generate_header()
        self.generate_footer()
        self.generate_sections()    

        for section in self.sections:
            section.generate()

    def generate_header(self):
        self.header = None
        if random.random() < self.header_probability:
            dy = random.randint(*self.header_height_range)
            self.header = Header(self, self.left_margin, self.lower_margin, self.width - self.right_margin - self.left_margin, dy)
            self.section_space["y_min"] += self.header.height

    def generate_footer(self):
        self.footer = None
        if random.random() < self.footer_probability:
            dy = random.randint(*self.footer_height_range)
            self.footer = Footer(self, self.left_margin, self.height - self.lower_margin - dy, self.width - self.right_margin - self.left_margin, dy)
            self.section_space["y_max"] -= self.footer.height

    def generate_sections(self):
        self.sections = Section(
            self,
            self.section_space["x_min"],
            self.section_space["y_min"],
            self.section_space["x_max"] - self.section_space["x_min"],
            self.section_space["y_max"] - self.section_space["y_min"],
            0
        ).split()

    def render(self):
        # to insert the fact that css is actually taken by external files
        html = f"""
        <html>
        <head>
        <style>
            .page {{
                position: relative;
                width: {self.width}px;
                height: {self.height}px;
                border: 2px solid black;
            }}
            .section {{
                position: absolute;
                border: 1px solid red;
            }}
            .column {{
                position: absolute;
                border: 1px dashed blue;
            }}
        </style>
        </head>
        <body>
        <div class="page">
        """

        if self.header:
            html += self.header.render()

        if self.footer:
            html += self.footer.render()

        for section in self.sections:
            html += section.render()

        html += "</div></body></html>"

        with open("src/generator/debug.html", "w") as f:
            f.write(html)

if __name__ == '__main__':

    page = Page(r"configs/historical/config.json")
    page.render()