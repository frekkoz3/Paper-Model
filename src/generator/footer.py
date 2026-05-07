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

fake = Faker()

class Footer(Component):

    def _generate(self):
        """
        Footer usually presents simple components.
        Things like:
        - straight lines
        - bar code (the newest one)
        - prices 
        - partnership advertisement
        - legal/burocratic little text
        - page number
        """

        self.footer_text = fake.sentence(nb_words = 2)
        self.burocratic_text = fake.sentence(nb_words = 40, variable_nb_words=True)

    def render(self):
        burocratic = random.random() < self.anchor.footer_cfg["burocratic text prob"]
        bur_text_alignment = random.choice(["center", "left", "right", "justify"])
        font_size = random.randint(8, 16)
        return f"""
        <div class="footer"
        style="--footer-padding:{self.padding}px;
            --footer-font-size:{font_size}px;
            --footer-h:{self.height}px;
            --footer-w:{self.width}px;
            --burocratic-text-alignment:{bur_text_alignment};">
            <div class="line"></div>
            {self.footer_text}
            <div class="bur">{self.burocratic_text if burocratic else ''}</div>
        </div>
        """