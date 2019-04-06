from django.test import TestCase

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import valid_article
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user


class ArticleTestCase(TestCase):
    """ This class defines the test suite for the article model """

    def setUp(self):
        self.user = User.objects.create_user(**valid_user)

        self.title = valid_article['title']
        self.description = valid_article['description']
        self.body = valid_article['body']

        valid_article.update(
            {"author_id": self.user.id}
        )

        self.article = Article(**valid_article)

    def test_model_can_create_an_article(self):
        previous_count = Article.objects.count()
        self.article.save()
        current_count = Article.objects.count()

        self.assertNotEqual(previous_count, current_count)

    def test_model_can_create_a_unique_slag(self):
        slug1 = self.article.get_unique_slag(self.title, 'slug')
        expected = "how-to-train-your-dragon"

        new_article = Article(**valid_article)
        new_article.save()
        slug2 = new_article.get_unique_slag(self.title, 'slug')

        self.assertEqual(slug1, expected)
        self.assertNotEqual(slug1, slug2)
