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
import requests
from src.generator.component import Component
import random

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

class Banner(Component):

    def _generate(self):
        self.img_url = f"https://picsum.photos/{int(self.width)}/{int(self.height)}"

    def render(self):
        return f"""
        <div class="banner">
            <img src="{self.img_url}" />
        </div>
        """