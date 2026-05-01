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

def random_logo(side : int):
    chars = [" ", "•"]
    logo = f"""<pre style="font-size:1px;">"""
    shape = random.choice(["square", "rectangle", "rhombus", "triangle"])
    upper = random.random() < 0.5
    for i in range(side):
        if shape == "square":
            logo += "".join(random.choices(chars, weights = [3, 1], k=2*side))
        elif shape == "rectangle":
            logo += "".join(random.choices(chars, weights = [3, 1], k=1*side))
        elif shape == "triangle":
            logo += "".join(random.choices(chars, weights = [3, 1], k=2*i if upper else 2*(side - i)))
        elif shape == "rhombus":
            logo += "".join(random.choices(chars, weights = [3, 1], k=2*i if i < side/2 else 2*(side-i)))
        elif shape == "exagon":
            upper = random.random() < 0.5
            logo += "".join(random.choices(chars, weights = [3, 1], k=2*i if upper else 2*(side - i)))
        logo+="\n"
    logo+="</pre>"
    return logo