import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            return self.render_articles(data)

        if data is None:
            return ''

        errors = data.get('errors', None)


        article = data.get('article', None)

        if errors is not None:
            return super(ArticleJSONRenderer, self).render(data)

        return json.dumps({'article': data}, default=str)

    def render_articles(self, data):
        articles = json.loads(
            super(ArticleJSONRenderer, self).render(data).decode()
        )
        return json.dumps({
            "articles": articles,
            "articlesCount": len(articles)
        })
