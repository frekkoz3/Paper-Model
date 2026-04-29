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
from src.generator.component import Component

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
        pass

    def render(self):
        return f"""
        <div class="footer"
        style="--footer-padding: {self.padding}px;
            --footer-h:{self.height}px;
            --footer-w:{self.width}px;">
            <div class="line"></div>
            Page 1
        </div>
        """