from aiohttp import web

from utils import steam


class Base(web.View):

    async def get(self):
        pass


class NotFound(web.View):

    @staticmethod
    async def get():
        return web.json_response(status=404)


class Forbidden(web.View):

    @staticmethod
    async def get():
        return web.json_response(status=403)


class Servers(Base):

    async def get(self):
        data = steam.get_server_list_with_players()
        return web.json_response({'data': data})
