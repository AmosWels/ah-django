import json

from rest_framework.renderers import JSONRenderer


class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        article = data.get('article', None)

        if article is None:
            errors = {"errors": data}
            return super(ArticleJSONRenderer, self).render(errors)

        article_dict = self.convert_data_to_dictionary(data)

        return json.dumps({
            'article': article_dict
        })

    def convert_data_to_dictionary(self, data):

        article = data.pop("article")

        article_details = {
            "slug": article.slug,
            "createdAt": f"{article.created_at}",
            "updatedAt": f"{article.updated_at}",
            "favorited": article.favorited,
            "favoritesCount": article.favorites_count,
        }
        data.update(article_details)

        author = data.pop("author")
        author_details = {
            "username": author.username
        }
        data.update({"author": author_details})

        return data
