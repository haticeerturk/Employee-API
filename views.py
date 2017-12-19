import csv
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/api/employee/')
async def handle_get(request):
    with open('Employees.csv') as file:
        reader = csv.reader(file, delimiter=';')
        employees = []
        for row in reader:
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
    str_data = data['name']+';'+data['surname']+';'+data['mail']+';'+data['birthday']

    with open('Employees.csv', 'a') as file:
        file.write(str_data)
        return web.json_response(data)
