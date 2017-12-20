import aiofiles
import csv
import json

from aiohttp import web
from utils import upload
from database import Employee

routes = web.RouteTableDef()

@routes.get('/api/employee/')
async def handle_get(request):
    async with aiofiles.open('Employees.csv', newline='') as file:
        employees = []
        async for line in file:
            row = line.split(',')
            employees.append({
                'name': row[0],
                'surname': row[1],
                'mail': row[2],
                'birthday': row[3]
            })

    async with request.app['db'].acquire() as conn:
        employees = []
        async for row in conn.execute(Employee.select()):
            employees.append({
                'id': row['id'],
                'name': row['name'],
                'surname': row['surname'],
                'mail': row['mail'],
                'birthday': row['birthday']
            })

    return web.json_response(employees)

@routes.post('/api/employee/')
async def handle_post(request):
    data = await request.json()

    async with aiofiles.open('Employees.csv', mode='a') as file:
        writer = csv.writer(file)
        await writer.writerow(data.values())

    async with request.app['db'].acquire() as conn:
        result = await conn.scalar(Employee.insert().values(
                                                        name=data['name'],
                                                        surname=data['surname'],
                                                        mail=data['mail'],
                                                        birthday=data['birthday']))
        print(result)

    await upload()
    return web.json_response(data)
