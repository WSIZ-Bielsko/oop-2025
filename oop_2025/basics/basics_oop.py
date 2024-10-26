import copy

from pydantic import BaseModel


class Dimension(BaseModel):
    height: int
    width: int


class Article(BaseModel):
    ean: str
    name: str
    dimensions: Dimension


class Parcel:

    def __init__(self, name='kadabra'):
        # konstruktor
        print('creating parcel')
        self.articles: list[Article] = []
        self.name = name

    def add_article(self, article: Article):  # to jest "metoda"
        self.articles.append(article)

    def get_articles(self) -> list[Article]:
        return copy.deepcopy(self.articles)

    def remove_article(self, ean: str):
        idx = None
        for i, article in enumerate(self.articles):
            if article.ean == ean:
                idx = i
                break
        if idx is not None:
            self.articles.pop(idx)

    def fits_shape(self, shape: Dimension) -> bool:
        """
        Checks if all articles, upon adding their widths, fit in shape.width, and
        all their heights fit are <= shape.height.
        :param shape:
        :return:
        """
        pass


if __name__ == '__main__':
    p = Parcel(name='magic')
    print('parcel created')
    print(p.name)
    p2 = Parcel(name='arctic')
    print(f'{p2.name}')
    p2.get_articles().append(3.1415)
    print(p2.articles)
