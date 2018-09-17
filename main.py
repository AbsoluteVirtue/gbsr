from aiohttp import web
import argparse
import os.path
import aiohttp_jinja2
import jinja2
import logging

from routes import setup_routes
from settings import get_config, get_logger


if __name__ == '__main__':
    app = web.Application()

    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--config_file', dest='config_file', default='./config/local.yaml', help='config file path')

    path = parser.parse_args().config_file

    app['config'] = get_config(path)
    app['logger'] = get_logger()

    setup_routes(app)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.abspath('templates')))

    logging.basicConfig(level=logging.INFO)
    logging.info('Web server started on port %s' % app['config']['port'])
    logging.info('Config file: %s' % path)

    web.run_app(app, host=app['config']['host'], port=app['config']['port'],
                access_log_format='%t "%r" %s %Tf ms -ip:"%a" -ref:"%{Referer}i"')
