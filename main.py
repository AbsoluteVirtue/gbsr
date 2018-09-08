from aiohttp import web, ClientSession

from routes import setup_routes
from settings import config


async def close_session(app):
    app['http'].close()


async def on_shutdown(app):
    await close_session(app)


if __name__ == '__main__':
    app = web.Application()

    app['config'] = config
    setup_routes(app)

    app.on_cleanup.append(close_session)
    app.on_shutdown.append(on_shutdown)

    web.run_app(app, host=config['host'], port=config['port'])
