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
from src.generator.banner import Banner
from src.generator.article import Article
from src.generator.component import Component

class Section(Component):

    """
        Class for the section.
        It is part of the page, which is its anchor.
        The section receives the position of the top-left corner (x, y),
        the height (height) and the width (width). 
        Width and height are alreaheight ensured to be inside the page.
        The page object contains also the dimension of the columns (range).
        The section could contains banner.
    """

    def __init__(self, anchor_page, x : float, y : float, width : float, height : float, recursion_index : int = 0):
        # this could be reframed in such a way that this follows the components protocol
        self.anchor = anchor_page
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.recursion_index = recursion_index
        self.columns = []

    def split(self):
        if (
            self.recursion_index >= self.anchor.recursion_limit or # MAXIMUM RECURSION REACHED
            random.random() > self.anchor.split_probability or # SPLITTING EVENT FAILED
            self.width < 2 * self.anchor.minimum_column_width or # MINIMUM SPACE OVER X AXIS REACHED
            self.height < 2 * self.anchor.minimum_section_height # MINIMUM SPACE OVER Y AXIS REACHED
        ):
            return [self]

        horizontal = random.random() > 0.5

        if horizontal:
            split = random.uniform(0.3, 0.7) * self.height # TO UNDERSTAND IF IT IS SUFFICIENT OR NOT
            s1 = Section(self.anchor, self.x, self.y, self.width, split, self.recursion_index + 1)
            s2 = Section(self.anchor, self.x, self.y + split, self.width, self.height - split, self.recursion_index + 1)
        else:
            split = random.uniform(0.3, 0.7) * self.width # TO UNDERSTAND IF IT IS SUFFICIENT OR NOT
            s1 = Section(self.anchor, self.x, self.y, split, self.height, self.recursion_index + 1)
            s2 = Section(self.anchor, self.x + split, self.y, self.width - split, self.height, self.recursion_index + 1)

        return [*s1.split(), *s2.split()]

    def _generate(self):
        self.generate_columns()
        self.place_banners()
        self.generate_articles()

    def generate_columns(self):
        """
            Function to generate columns
        """
        available_width = self.width
        min_w = self.anchor.minimum_column_width
        margin = self.anchor.column_margin

        max_cols = int(available_width // min_w)
        
        n_cols = random.randint(1, max_cols) if max_cols > 1 else 1

        col_width = (available_width - (n_cols - 1) * margin) / n_cols

        self.columns = []
        for i in range(n_cols):
            # x = self.x + i * (col_width + margin)
            x = i * (col_width + margin)   # relative to section
            y = 0
            self.columns.append({
                "x": x,
                "y": y,
                "width": col_width,
                "height": self.height,
                "cursor_y": self.y  # where next content goes
            })

    def place_banners(self):
        # must think about how to determine how many banners to put in a section
        # and how big each banner should be
        pass
        self.n_banners = ...
        self.banners = ...
    
    def generate_articles(self):
        # must think about how to determine how many article to put in a section 
        # and how long each article should be
        pass
        self.n_articles = ...
        self.articles = ...

    def render(self):
        html = f"""
        <div class="section" style="
            left:{self.x}px;
            top:{self.y}px;
            width:{self.width}px;
            height:{self.height}px;">
        """

        for col in self.columns:
            html += f"""
            <div class="column" style="
                left:{col['x']}px;
                top:{col['y']}px;
                width:{col['width']}px;
                height:{col['height']}px;">
            </div>
            """

        html += "</div>"
        return html