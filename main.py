from aiohttp import web
from routes import setup_routes
from database import init_db, close_db, create_table

app = web.Application()

app.on_startup.append(init_db)
#app.on_startup.append(create_table)
app.on_cleanup.append(close_db)

setup_routes(app)
web.run_app(app, host='127.0.0.1', port=8080)
