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
        self.corpus = " ".join(self.fake.paragraphs(nb=random.randrange(10, 20)))
        self.author = self.fake.name()
        # self.symbols = ... THIS SHOULD BE ADDED 

    def render(self, is_main=False):
        main_class = "article article-main" if is_main else "article"

        return f"""
        <article class="{main_class}">
            <div class="article-title">{self.title}</div>
            <div class="article-subtitle">{self.subtitle}</div>
            <p>{self.corpus}</p>
            <div class="article-author">By {self.author}</div>
        </article>
        """
        
    def __str__(self):
        s = ""
        return f"{self.title}\n-----------------\n{self.subtitle}\n-----------------\n{self.corpus}\n-----------------\n{self.author}"

if __name__ == '__main__':
    a = Article()
    print(a)
