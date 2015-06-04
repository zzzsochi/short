import asyncio
import logging

import aioredis

from aiohttp.web import Application
from aiohttp_traversal.router import TraversalRouter

from . import resources
from . import views

log = logging.getLogger(__name__)


def includeme(app):
    app.router.bind_view(resources.Root, views.Root)
    app.router.bind_view(resources.Url, views.Url)


@asyncio.coroutine
def setup_redis(app, host='localhost', port=6379):
    log.info('connecting to redis ({}:{})'.format(host, port))

    app['redis'] = yield from aioredis.create_pool(
        (host, port),
        minsize=5, maxsize=10,
        loop=app.loop)

    app.register_on_finish(lambda app: app['redis'].clear())


def configure(loop, redis):
    app = Application(loop=loop, router=TraversalRouter())
    app.router.set_root_factory(resources.Root)
    includeme(app)

    loop.run_until_complete(setup_redis(app, *redis))

    return app
