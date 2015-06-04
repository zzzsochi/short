import asyncio
import string
from random import choice

from aiohttp_traversal.ext.resources import Resource, InitCoroMixin

CHARS = string.ascii_lowercase + string.digits


class UrlNotFound(Exception):
    pass


class Root(Resource):
    def __init__(self, request):
        super().__init__(parent=None, name=None)
        self.request = request
        self.app = self.request.app

    @asyncio.coroutine
    def __getchild__(self, name):
        try:
            return (yield from Url(self, name))
        except UrlNotFound:
            return None

    @asyncio.coroutine
    def create(self, url):
        """ Add new url to db for get if exist
        """
        with (yield from self.app['redis']) as redis:
            if not (yield from redis.setnx('u:' + url, '')):
                short = yield from self._get_exist(redis, url)

            else:
                short = yield from self._set_new(redis, url)

        return short

    @asyncio.coroutine
    def _get_exist(self, redis, url):
        short = (yield from redis.get('u:' + url)).decode()

        if short:
            return short
        else:
            # collision found
            yield from asyncio.sleep(0.05)
            short = (yield from redis.get('u:' + url)).decode()

            if short:
                return short
            else:
                # try fix error
                yield from redis.delete('u:' + url)
                return (yield from self.create(url))

    @asyncio.coroutine
    def _set_new(self, redis, url, length=2, retries=5):
        for _ in range(retries):
            short = self._gen_short(length)

            if (yield from redis.setnx('s:' + short, url)):
                redis.set('u:' + url, short)
                return short

        else:
            return (yield from self._set_new(redis, url, length+1, retries*2))

    @staticmethod
    def _gen_short(length):
        return ''.join(choice(CHARS) for _ in range(length))


class Url(InitCoroMixin, Resource):
    @asyncio.coroutine
    def __init_coro__(self):
        self.url = yield from self.get()

    @asyncio.coroutine
    def get(self):
        """ Get url from db
        """
        with (yield from self.app['redis']) as redis:
            url = yield from redis.get('s:' + self.name)

        if not url:
            raise UrlNotFound()
        else:
            return url.decode('utf8')
