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

class Banner(Component):

    def _generate(self):
        self.img_url = f"https://picsum.photos/{int(self.width)}/{int(self.height)}?random"

    def render(self):
        font_size = random.randint(5, 12)

        fake = Faker()
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
                --banner-font-size:{font_size}px;
                --banner-border-size:{border_size}px;
                --banner-text-alignment:{text_alignment};
            ">
            <img src="{self.img_url}" />
            {description_html}
        </div>
        """

if __name__ == '__main__':

    # this does not work for now, waiting the response from the guys of the AdImageNet
    try:
        with open("configs/hf_token.txt", "r") as f:
            hf_token = f.read()
    except Exception as e:
        print(e)
        print("Check the README in the configs folder")

    df = pl.read_parquet('hf://datasets/PeterBrendan/AdImageNet/data/train-*.parquet', 
                         storage_options={"token": hf_token})
    
    print(df.head())

