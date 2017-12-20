import sqlalchemy as sa
from aiopg.sa import create_engine

meta = sa.MetaData()

Employee = sa.Table('employees', meta,
    sa.Column('id', sa.Integer, nullable=False),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('surname', sa.String(100), nullable=False),
    sa.Column('mail', sa.String(60), nullable=False),
    sa.Column('birthday', sa.String(30), nullable=False),
    sa.PrimaryKeyConstraint('id', name='employees_id_pkey'))

async def init_db(app):
    engine = await create_engine(
        database='employeeapi',
        user='postgres',
        password='',
        host='127.0.0.1')
    app['db'] = engine


async def close_db(app):
    app['db'].close()
    await app['db'].wait_closed()

async def table(conn):
    await conn.execute('DROP TABLE IF EXISTS employees')
    await conn.execute('''CREATE TABLE employees (
                        id serial PRIMARY KEY,
                        name varchar(100) not null,
                        surname varchar(100) not null,
                        mail varchar(60) not null,
                        birthday varchar(30) not null)''')

async def create_table(app):
    async with app['db'] as engine:
        async with engine.acquire() as conn:
            await table(conn)
