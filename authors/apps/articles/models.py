from django.db import models
from authors.apps.authentication.models import User
from django.template.defaultfilters import slugify
# from django.utils import timezone
# import secrets


class Article(models.Model):

    slug = models.SlugField(max_length=255)

    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now_add=True)

    favorited = models.BooleanField(default=False)

    favorites_count = models.IntegerField(default=0)

    author = models.ForeignKey(
        User,
        related_name='articles',
        on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slag('title', 'slug')
        super().save(*args, **kwargs)

    def get_unique_slag(self, slugable_field_name, slug_field_name):
        slug = slugify(self.title)
        unique_slug = slug
        # Use a hash string to create a unigue extension to
        # append to the slug inorder to create a unique slag
        extention = 1
        ModelClass = self.__class__
        # Search through the existing slags to check whether
        # the slag we created above already exists. If it does,
        # make it unique by appending a hyphen and the extension
        # to it.
        while ModelClass.objects.filter(
            **{slug_field_name: unique_slug}
        ).exists():
            unique_slug = f"{slug}-{extention}"
            extention += 1

        return unique_slug
