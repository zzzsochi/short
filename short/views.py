import asyncio

from aiohttp.web_exceptions import HTTPBadRequest, HTTPMovedPermanently
from aiohttp_traversal.ext.views import MethodsView, RESTView


HTML_TEMPLATE = """<html>
<head><title>Moved Permanently</title></head>
<body bgcolor="#FFFFFF" text="#000000">
<h1>Moved Permanently</h1>
The document has moved <a href="{}">here</a>.
</body></html>"""


class Root(RESTView):
    methods = {'post'}

    @asyncio.coroutine
    def post(self):
        try:
            data = yield from self.request.json()
        except ValueError:
            raise HTTPBadRequest(reason="invalid payload")

        if 'url' not in data:
            raise HTTPBadRequest(reason="key 'url' is required, but not found")

        url = data['url']
        if not (url.startswith('http://') or url.startswith('https://')):
            raise HTTPBadRequest(reason="bad url: {!r}".format(url))

        short = yield from self.resource.create(url)

        return {'url': short}


class Url(MethodsView):
    methods = {'get'}

    @asyncio.coroutine
    def get(self):
        return HTTPMovedPermanently(
            location=self.resource.url,
            text=HTML_TEMPLATE.format(self.resource.url))
