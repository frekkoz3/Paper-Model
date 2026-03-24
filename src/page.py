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
import random
from src.header import Header
from src.footer import Footer
from src.section import Section
from utils import random_datetime

class Page:

    def __init__(self, config : str):
        """
            Read the config and assign the values to the parameters.
        """
        # read and assign values from the config file

        # PAGE PARAMS
        self.width = ...
        self.height = ...
        self.header_probability = ...
        self.footer_probability = ...
        self.minimum_column_width = ...
        self.minimum_section_height = ...
        self.upper_margin = ...
        self.lower_margin = ...
        self.right_margin = ...
        self.left_margin = ...
        self.column_margin = ...
        self.between_section_margin = ...

        # SECTION PARAMS
        self.recursion_limit = ...
        self.split_probability = ...

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
            self.header = Header(self)
            self.section_space["y_min"] += self.header.height

    def generate_footer(self):
        self.footer = None
        if random.random() < self.footer_probability:
            self.footer = Footer(self)
            self.section_space["y_max"] -= self.footer.height

    def generate_sections(self):
        self.sections = Section(self, 0, 0, self.width, self.height, 0).split()

    def render(self):
        """
            Function to render with HTML and css the page.
        """
        self.header.render()
        self.footer.render()
        for section in self.sections:
            section.render()
        