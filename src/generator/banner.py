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

# consider using also something from 
# https://people.cs.pitt.edu/~kovashka/ads_workshop/#intro
# in order to obtains random advertisement images (really helpful)

# or also 
# https://huggingface.co/datasets/yunusserhat/TextOCR-Dataset
# https://huggingface.co/datasets/howard-hou/COCO-Text
# https://github.com/cs-chan/Total-Text-Dataset
# https://www.kaggle.com/datasets/dataclusterlabs/vertical-text
# for images with text within it

# banner could also been just simple symbols within a black-bordered box
# and some text within it (old one especially)

import polars as pl
from faker import Faker
import random
from src.utils import download_300x250_parallel
from pathlib import Path

fake = Faker()

if not Path("resources/300x250").exists():
    print("Wait a bit. We are gonna download the 300x250 dataset.")
    download_300x250_parallel()
    print("Done, now we will proceede.")

folder = Path("resources/300x250").resolve()
BANNER_URLS = [f.as_uri() for f in folder.iterdir() if f.is_file()]

class Banner(Component):

    def __init__(self, anchor_page, x, y, width, height, padding, photo_prob :int = 0.5):
        self.photo_prob = photo_prob
        super().__init__(anchor_page, x, y, width, height, padding)
        

    def _generate(self):
        if random.random() < self.photo_prob:
            self.img_url = f"https://picsum.photos/{int(self.width)}/{int(self.height)}?random"
        else:
            self.img_url = random.choice(BANNER_URLS)

    def render(self):
        font_size = random.randint(5, 12)

        description = fake.sentence(nb_words=5, variable_nb_words=True)

        border_size = random.choice([0, 2, 4])
        text_alignment = random.choice(["left", "right"])

        show_description = ( random.random() < self.anchor.banner_cfg["description probability"] )

        description_html = (
            f'<div class="description">{description}</div>'
            if show_description else ""
        )

        return f"""
        <div class="banner"
            style="
                --banner-height:{self.height}px;
                --banner-width:{self.width}px;"
                --banner-font-size:{font_size}px;
                --banner-border-size:{border_size}px;
                --banner-text-alignment:{text_alignment};
            ">
            <img src="{self.img_url}" width={self.width - 2*border_size} height={self.height - 2*border_size}/>
        </div>

        {description_html}
        
        """

if __name__ == '__main__':
    pass

