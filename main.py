from aiohttp import web, ClientSession
import aiohttp_jinja2
import jinja2
import pathlib

from routes import setup_routes
from settings import get_config

BASE_DIR = pathlib.Path(__file__).parent


async def close_session(app):
    app['http'].close()


async def on_shutdown(app):
    await close_session(app)


if __name__ == '__main__':
    app = web.Application()

    app['config'] = get_config(BASE_DIR / 'config' / 'local.yaml')
    setup_routes(app)

    app.on_cleanup.append(close_session)
    app.on_shutdown.append(on_shutdown)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(searchpath=str(BASE_DIR / 'templates')))

    web.run_app(app, host=app['config']['host'], port=app['config']['port'])
