import aiofiles
import csv
import json
import logging
import uuid

from aiohttp import web
from utils import upload
from database import Employee

routes = web.RouteTableDef()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@routes.get('/api/employee/')
async def handle_get(self):
    self.uuid = uuid.uuid4()
    logger.info('***** Running the {} for GET request *****'.format(self.uuid))

    async with aiofiles.open('Employees.csv', newline='') as file:
        logger.info('***** Opening the file by the {} for GET request *****'.format(self.uuid))
        employees = []
        async for line in file:
            row = line.split(',')
            employees.append({
                'name': row[0],
                'surname': row[1],
                'mail': row[2],
                'birthday': row[3]
            })

    async with self.app['db'].acquire() as conn:
        logger.info('***** Connecting database by the {} for GET request *****'.format(self.uuid))
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
async def handle_post(self):
    self.uuid = uuid.uuid4()
    logger.info('***** Running the {} for POST request ******'.format(self.uuid))
    data = await self.json()

    async with aiofiles.open('Employees.csv', mode='a') as file:
        logger.info('***** Opening the file by the {} for POST request ******'.format(self.uuid))
        writer = csv.writer(file)
        await writer.writerow(data.values())

    async with self.app['db'].acquire() as conn:
        logger.info('***** Connecting database by the {} for POST request ******'.format(self.uuid))
        result = await conn.scalar(Employee.insert().values(
                                                        name=data['name'],
                                                        surname=data['surname'],
                                                        mail=data['mail'],
                                                        birthday=data['birthday']))

    await upload(self)
    return web.json_response(data)
