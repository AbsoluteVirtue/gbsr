from controllers import base


def setup_routes(app):
    app.router.add_view(r'/', handler=base.Servers)
