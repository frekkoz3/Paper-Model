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
class Component:
    """
        Basic layout component of the article.
    """
    
    def __init__(self, anchor_page, x, y, width, height):
        self.anchor = anchor_page
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._generate()

    def _generate(self):
        pass

    def render(self):
        pass