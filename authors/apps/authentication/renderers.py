import json

# from rest_framework.renderers import JSONRenderer
from authors.apps.core.renderers import AuthorsJSONRenderer

class UserJSONRenderer(AuthorsJSONRenderer):
    # charset = 'utf-8'
    object_label = 'user'

    def render(self, data, media_type=None, renderer_context=None):
        
        # Finally, we can render our data under the "user" namespace.
        return json.dumps({
            'user': data
        })
        
