import aiofiles
import asyncio
import csv
from aiohttp import web
from utils import upload

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
    return web.json_response(employees)

@routes.post('/api/employee/')
async def handle_post(request):
    data = await request.json()

    async with aiofiles.open('Employees.csv', mode='a') as file:
        writer = csv.writer(file)
        await writer.writerow(data.values())

    return web.json_response(data)
