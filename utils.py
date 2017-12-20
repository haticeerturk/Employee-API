import aiofiles
import asyncio
import aiobotocore
import settings

async def upload():
    filename = 'Employees.csv'
    folder = 'employees'
    key = '{}/{}'.format(folder, filename)

    session = aiobotocore.get_session()
    async with session.create_client('s3', region_name='eu-central-1', verify=False,
                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID) as client:
        async with aiofiles.open(filename, newline='') as file:
            data = await file.read()
        response = await client.put_object(Bucket=settings.S3_BUCKET,
                                            Key=key,
                                            Body=data)
        print(response)
