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
from faker import Faker
import random

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
        fake = Faker(['en_US', 'it_IT'])
        self.name = fake.sentence(nb_words=2, variable_nb_words=True)
        self.subtitle = fake.sentence(nb_words=4, variable_nb_words=True)
        self.date = f"{self.anchor.date.strftime('%B %d, %Y')}"
        self.price = f"{round(random.random(), 1)}0 {random.choice(["£", "$", "¥", "€"])}"
        self.date_type = random.choice(['center', 'top-right', 'bottom-right', 'none'])
        
        

    def render(self):

        font_family = random.choice(self.anchor.page_cfg["fonts"])
        
        font_size = random.randint(8, 14)
        title_size = random.randint(28, 64)
        subtitle_size = random.uniform(0.2, 0.5)*title_size

        # Upper section
        upper_lines = ['<div class="line"></div>' for _ in range (random.randint(1, 3))]
        div_top = ""
        if random.random() < self.anchor.header_cfg["upper probability"]:
            div_top = f"""
                <div class="header-top">
                {self.price} • {random.randint(18908, 37827)} • {self.date}
                {''.join(upper_lines) if upper_lines else ''}
            </div>
            """

        # Lower section
        lower_lines = ['<div class="line"></div>'  for _ in range (random.randint(1, 3))]
        div_bottom = ""
        if random.random() < self.anchor.header_cfg["lower probability"]:
            div_bottom = f"""{''.join(lower_lines) if lower_lines else ''}"""

        # Logo -> THIS MUST BE IMPLEMENTED -> could be a subclass of banner
        # look at this https://github.com/msn199959/Logo-2k-plus-Dataset
        logo_sx = f"""
            <div class="logo left">
            {"***" if random.random() < self.anchor.header_cfg["logo probability"] else ""}
            </div>
        """
        logo_dx = f"""
            <div class="logo right">
            {"***" if random.random() < self.anchor.header_cfg["logo probability"] else ""}
            </div>
        """

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