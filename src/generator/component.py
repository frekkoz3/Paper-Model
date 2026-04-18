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
    
    def __init__(self, anchor_page, x, y, width, height, padding):
        self.anchor = anchor_page
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.padding = padding
        self._generate()

    def _generate(self):
        pass

    def render(self):
        """
        Return the html (plus css) needed in order to render the component into the page
        """
        pass

    def get_YOLO_annotation(self, class_id : int = 0):
        """
        YOLO format : class_id center_x center_y width height
        Return the YOLO annotation format.
        """
        return f"{class_id} {(self.x + self.width/2)/self.anchor.width} {(self.y + self.height/2)/self.anchor.height} {(self.width)/self.anchor.width} {(self.height)/self.anchor.height}"