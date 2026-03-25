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

class Header:

    def __init__(self, page, x, y, dx, dy):
        self.anchor = page
        self.x = x
        self.y = y
        self.width = dx
        self.height = dy

    def render(self):
        return f"""
        <div class="header" style="
            position: absolute;
            left: {self.x}px;
            top: {self.y}px;
            width: {self.width}px;
            height: {self.height}px;
            border: 2px solid blue;
            background-color: rgba(0, 0, 255, 0.1);
        ">
            <span style="font-size:10px;">HEADER</span>
        </div>
        """