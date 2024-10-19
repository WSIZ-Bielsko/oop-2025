from pydantic import BaseModel


class Dimension(BaseModel):
    height: int
    width: int


class Article(BaseModel):
    ean: str
    name: str
    dimensions: Dimension


class Parcel:

    def __init__(self):
        self.articles: list[Article] = []

    def add_article(self, article: Article):
        self.articles.append(article)

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
    pass
