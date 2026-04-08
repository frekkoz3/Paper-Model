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
from faker import Faker
import random
from src.generator.component import Component

class Article():

    """
        Class to generate random articles.
    """

    def __init__(self):
        self.fake = Faker()
        self._generate()

    def _generate(self):
        """
        Generate using Faker library random sentences that resamble articles (not just Lorem Ipsum).
        """
        self.title = self.fake.sentence(nb_words=6, variable_nb_words=True)
        self.subtitle = self.fake.sentence(nb_words=10, variable_nb_words=True)
        self.corpus = " ".join(self.fake.paragraphs(nb=random.randrange(3, 8)))
        self.author = self.fake.name()
        # self.symbols = ... THIS SHOULD BE ADDED 
    
    def __str__(self):
        s = ""
        return f"{self.title}\n-----------------\n{self.subtitle}\n-----------------\n{self.corpus}\n-----------------\n{self.author}"
    
class ArticleComponent(Component):
    def __init__(self, anchor_page, x, y, width, height, article_data : Article | None = None, num_cols=1):
        super().__init__(anchor_page, x, y, width, height)
        self.data = article_data if article_data else Article()
        self.num_cols = num_cols

    def render(self):
        return f"""
        <div class="article" style="
            position: absolute; 
            left: {self.x}px; 
            top: {self.y}px; 
            width: {self.width}px; 
            height: {self.height}px;
        ">
            <div class="article-title">{self.data.title}</div>
            <div class="article-subtitle">{self.data.subtitle}</div>
            
            <div class="article-corpus" style="
                column-count: {self.num_cols}; 
                height: 100%;
            ">
                {self.data.corpus}
            </div>
        </div>
        """


if __name__ == '__main__':
    a = Article()
    print(a)
