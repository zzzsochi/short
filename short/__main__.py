import asyncio
import argparse
import logging
from functools import wraps

from . import configure, connect_to_redis

log = logging.getLogger(__name__)


def setup_logging(func):
    @wraps(func)
    def wrapper(args):
        logging.getLogger('asyncio').setLevel('ERROR')
        logging.basicConfig(level=args.loglevel.upper())
        log.setLevel(level=args.loglevel.upper())
        return func(args)

    return wrapper


@setup_logging
def clear(args):
    loop = asyncio.get_event_loop()

    @asyncio.coroutine
    def coro(args):
        pool = yield from connect_to_redis(
            loop, args.redis_host, args.redis_port, args.redis_db)

        with (yield from pool) as redis:
            log.info("clear redis")
            yield from redis.flushdb()

        redis.close()

    loop.run_until_complete(coro(args))


@setup_logging
def serve(args):
    loop = asyncio.get_event_loop()

    log.info("start configuring application")
    redis_info = (args.redis_host, args.redis_port, args.redis_db)
    app = configure(loop=loop, redis=redis_info)

    log.info("start listening socket ({}:{})".format(args.host, args.port))
    handler = app.make_handler()
    fut = loop.create_server(handler, args.host, args.port)
    srv = loop.run_until_complete(fut)

    try:
        log.info("start event loop")
        loop.run_forever()  # run event loop
    except KeyboardInterrupt:
        pass
    finally:
        # stopping
        log.info("stopping")
        loop.run_until_complete(handler.finish_connections(timeout=5.0))
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(app.finish())
        loop.close()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    clear_serve = subparsers.add_parser('clear', help="Clear redis")
    clear_serve.set_defaults(func=clear)
    clear_serve.add_argument(
        '--loglevel',
        choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='WARNING',
        help='Set log level (default: WARNING)')
    clear_serve.add_argument(
        '--redis-host',
        default='localhost',
        help='Redis host (default: localhost)')
    clear_serve.add_argument(
        '--redis-port',
        type=int,
        default=6379,
        help='Redis port (default: 6379)')
    clear_serve.add_argument(
        '--redis-db',
        type=int,
        default=0,
        help='Redis db number (default: 0)')

    parser_serve = subparsers.add_parser('serve', help="Start server")
    parser_serve.set_defaults(func=serve)
    parser_serve.add_argument(
        '--loglevel',
        choices=['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='WARNING',
        help='Set log level (default: WARNING)')
    parser_serve.add_argument(
        '--host',
        default='localhost',
        help='Host for HTTP listening (default: localhost)')
    parser_serve.add_argument(
        '--port',
        type=int,
        default=8080,
        help='Port for HTTP listening (default: 8080)')
    parser_serve.add_argument(
        '--redis-host',
        default='localhost',
        help='Redis host (default: localhost)')
    parser_serve.add_argument(
        '--redis-port',
        type=int,
        default=6379,
        help='Redis port (default: 6379)')
    parser_serve.add_argument(
        '--redis-db',
        type=int,
        default=0,
        help='Redis db number (default: 0)')

    args = parser.parse_args()

    if getattr(args, 'func', None):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
