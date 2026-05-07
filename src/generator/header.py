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
from src.generator.component import Component
from src.generator.banner import BANNER_URLS
from src.generator.utils import random_logo
from faker import Faker
import random

fake = Faker(['en_US', 'it_IT'])

class Header(Component):

    def _generate(self):
        """
        Header usually presents simple components.
        Things like:
        - straight lines
        - bar code (the newest one)
        - prices 
        - partnership advertisement
        - legal/burocratic little text
        - page number
        - 
        """
        self.name = fake.sentence(nb_words=2, variable_nb_words=True)
        self.subtitle = fake.sentence(nb_words=4, variable_nb_words=True)
        self.date = f"{self.anchor.date.strftime('%B %d, %Y')}"
        self.price = f"{round(random.random(), 1)}0{random.choice(['£', '$', '¥', '€'])}"
        self.date_type = random.choice(['center', 'top-right', 'bottom-right', 'none'])
        

    def render(self):

        font_family = random.choice(self.anchor.page_cfg["fonts"])
        
        font_size = random.randint(8, 14)
        title_size = random.randint(28, 64)
        subtitle_size = random.uniform(0.2, 0.5)*title_size

        # Upper section
        upper_lines = ['<div class="line"></div>' for _ in range (random.randint(1, 3))]
        elements = [self.price, random.randint(18908, 37827), self.date]
        divider = random.choice(["•", "-", "*"])
        random.shuffle(elements)
        div_top = ""
        if random.random() < self.anchor.header_cfg["upper probability"]:
            div_top = f"""
                <div class="header-top", 
                style="word-spacing:{random.randint(2, 5)}px;">
                {elements[0]}
                {divider}
                {elements[1]}
                {divider}
                {elements[2]}
                {''.join(upper_lines) if upper_lines else ''}
            </div>
            """

        # Lower section
        lower_lines = ['<div class="line"></div>'  for _ in range (random.randint(1, 3))]
        div_bottom = ""
        if random.random() < self.anchor.header_cfg["lower probability"]:
            div_bottom = f"""{''.join(lower_lines) if lower_lines else ''}"""
        
        logo_side = random.randint(30, 60)
        
        def make_logo(side):
            if random.random() < self.anchor.header_cfg["logo probability"]:
                img = f'<img src="{random.choice(BANNER_URLS)}">'
            else:
                img = ""

            return f"""
            <div class="logo {side}" style="
                --logo-side:{logo_side}px;">
                {img}
            </div>
            """

        logo_sx = make_logo("left")
        logo_dx = make_logo("right")

        # Subtitle
        subt = ""
        if random.random() < self.anchor.header_cfg["subtitle"]:
            subt = f"""
            <div class="newspaper-subtitle">
                {self.subtitle}
            </div>
            """

        return f"""
        <div class="header"
        style="--header-padding:{self.padding}px;
               --header-font-family:{font_family};
               --header-font-size:{font_size}px;
               --header-title-font-size:{title_size}px;
               --header-subtitle-font-size:{subtitle_size}px;
               --header-h:{self.height}px;
               --header-w:{self.width}px;">

            {div_top}
            
            <div class="masthead">

                {logo_sx}
                
                <div class="title-group">
                    <div class="newspaper-title">
                        {self.name}
                    </div>
                    {subt}
                </div>

                {logo_dx}

            </div>

            {div_bottom}
            
        </div>
        """