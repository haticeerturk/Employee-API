from views import routes

def setup_routes(app):
    app.router.add_routes(routes)
