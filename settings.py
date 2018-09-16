import os.path
import yaml
import logging


async def close_session(app):
    app['http'].close()


async def on_shutdown(app):
    await close_session(app)


def get_config(path):
    config_file = os.path.abspath(path)
    with open(config_file) as f:
        config = yaml.load(f)

    return config


def get_logger():
    logger = logging.getLogger(name='aiohttp.server')
    logger.setLevel(logging.INFO)

    return logger
