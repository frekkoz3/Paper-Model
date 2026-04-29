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
        self.date = f"{self.anchor.date.strftime('%B %d, %Y')}"
        self.date_type = random.choice(['center', 'top-right', 'bottom-right', 'none'])
        self.font_size = random.randint(28, 64)
        pass

    def render(self):
        formatted_date = f"<center> {self.date} </center>" # to think how to place elsewhere

        hr_h = random.randint(1, 5)
        upper_lines = ['<div class="line"></div>' for _ in range (random.randint(0, 2))] if random.random() < 0.5 else ['<hr>']
        lower_lines = ['<div class="line"></div>'  for _ in range (random.randint(0, 2))]

        return f"""
        <div class="header"
        style="--header-padding:{self.padding}px;
               --header-font-size:{self.font_size}px;
               --header-h:{self.height}px;
               --header-w:{self.width}px;
               --hr-height : {hr_h}px;">
            {''.join(upper_lines) if upper_lines else ''}
            <center> {self.name} </center> 
            <div class="date"> {self.date} </div>
            {''.join(lower_lines) if lower_lines else ''}
        </div>
        """
