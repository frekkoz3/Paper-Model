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

    def __init__(self, anchor_page, x : float, y : float, width : float, height : float, padding : float, recursion_index : int = 0):
        self.anchor = anchor_page
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.padding = padding
        self.recursion_index = recursion_index
        self.columns = [] # this should be populated with some block or something like this in order to make it useful for the annotation process

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

        self.section_type = random.choice(["main", "standard"])

        self.title = None
        self.title_height = 0
        self.title_font_size = random.randrange(24, 48)
        if random.random() < 0.4:   # probability of having a title
            self.title = {
                "text": Article().title  # or a dedicated Title class later
            }
            # self.title_height = len(self.title["text"].split())*(self.title_font_size+5) # how to proxy the height of the title?

        self.banners = []

        n_banners = random.choices([0, 1, 2], weights=[1, 3, 3])[0]

        for _ in range(n_banners):
            banner = Banner(self.anchor, self.x, self.y, self.width, self.height, 5)
            self.banners.append(banner)

        self.elements = []


        n_articles = random.randint(20, 30)

        for i in range(n_articles):
            is_main = (self.section_type == "main" and i == 0)

            article = Article(probs=self.anchor.article_cfg["probability"])

            self.elements.append({
                "type": "article",
                "content": article,
                "is_main": is_main,
                "span": len(self.columns) if is_main else 1
            })

        flow = []

        if self.title:
            flow.append({
                "type": "title",
                "content": self.title["text"]
            })

        banner_index = 0

        for i, element in enumerate(self.elements):
            flow.append(element)

            # randomly inject banners between articles
            if banner_index < len(self.banners) and random.random() < 0.25:
                flow.append({
                    "type": "banner",
                    "content": self.banners[banner_index]
                })
                banner_index += 1

        # append remaining banners
        while banner_index < len(self.banners):
            flow.append({
                "type": "banner",
                "content": self.banners[banner_index]
            })
            banner_index += 1

        self.flow = flow
    
    def generate_columns(self):
        if self.width < 1.2*self.anchor.minimum_column_width : self.n_columns = 1
        elif self.width < 2.4*self.anchor.minimum_column_width : self.n_columns = 2
        else : self.n_columns = random.choice([2, 2, 3, 3, 3, 4, 4, 5])
        

    def place_banners(self):
        self.banners = []

        if random.random() < 0.3:  # 30% chance
            b = Banner(self.anchor, self.x, self.y, self.width, 150)
            b._generate()
            self.banners.append(b)

    def render(self):

        html = f"""
        <section class="section"
            style="
                top: {self.y - self.anchor.section_space["y_min"]}px;
                left: {self.x}px;
                width: {self.width}px;
                height: {self.height}px;
                --cols:{self.n_columns};
                --gap:{self.anchor.column_gap}px;
                --section-padding:{self.padding}px;
                --title-font-size:{self.title_font_size}px;">
            <div class="section-content">
        """
        for item in self.flow:
            if item["type"] == "title":
                self.title_height = (len(item["content"]) * 32)/self.width # approxximation
                html += f"""
                <div class="section-title">
                    {item["content"]}
                </div>
                """
            elif item["type"] == "article":
                span = item.get("span", 1)
                is_main = item.get("is_main", False)

                html += f"""
                <div class="article-wrapper" style="--span:{span};">
                    {item["content"].render(is_main=is_main)}
                </div>
                """
            elif item["type"] == "banner":
                html += f"""
                <div class="banner-wrapper">
                    {item["content"].render()}
                </div>
                """

        html += """
            </div>
        </section>
        """

        return html