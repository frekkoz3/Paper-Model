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

    def __init__(self, probs : dict = {"title" : 1, "subtitle" : 0.1, "corpus" : 1, "author" : 0.2, "italic" : 0.2}):
        self.probs = probs
        self.fake = Faker(['it_IT', 'en_US'])
        self._generate()

    def _generate(self):
        """
        Generate using Faker library random sentences that resamble articles (not just Lorem Ipsum).
        """
        self.title = self.fake.sentence(nb_words=6, variable_nb_words=True) if random.random() < self.probs["title"] else None
        self.subtitle = self.fake.sentence(nb_words=10, variable_nb_words=True) if random.random() < self.probs["subtitle"] else None
        self.corpus = " ".join(self.fake.paragraphs(nb=random.randrange(10, 20))) if random.random() < self.probs["corpus"] else None
        self.author = self.fake.name() if random.random() < self.probs["author"] else None
        # self.symbols = ... THIS SHOULD BE ADDED 

    def render(self, is_main=False):

        main_class = "article article-main" if is_main else "article"

        italic = random.random() < self.probs["italic"]
        font_size = random.randint(4, 14)
        text_alignment = "justify" # random.choice(["start", "end", "left", "right", "center", "justify"])
        padding = random.randint(0, 5)

        return f"""
        <article class="{main_class}", 
        style="
        --article-padding:{padding}px;
        --article-font-size:{font_size}px;
        --article-text-alignment:{text_alignment};">
            <div class="article-title">{self.title if self.title else ''}</div>
            <div class="article-subtitle">{self.subtitle if self.subtitle else ''}</div>
            {'<p>' if not italic else '<i>'}{self.corpus if self.corpus else ''}{'</p>' if not italic else '</i>'}
            <div class="article-author">{self.author if self.author else ''}</div>
        </article>
        """
        
    def __str__(self):
        s = ""
        return f"{self.title}\n-----------------\n{self.subtitle}\n-----------------\n{self.corpus}\n-----------------\n{self.author}"

if __name__ == '__main__':
    a = Article()
    print(a)
