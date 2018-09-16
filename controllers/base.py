from aiohttp import web
import aiohttp_jinja2

from utils import steam


class Base(web.View):

    async def get(self):
        pass


class Servers(Base):

    async def get(self):
        data = await steam.get_server_list_with_players(self.request.app['logger'])
        response = aiohttp_jinja2.render_template('home.html', self.request, context=data)
        return response
