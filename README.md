# Employee-API

A simple asynchronous project. The project uses aiohttp, aiofiles, aiobotocore for asynchronous operations. PostgreSQL was used for the database management system and the operations on the database were done with SqlAlchemy. The data is kept in both csv file and uploaded to AWS s3. <br>

:heavy_check_mark: ***What are the things to do before using it?*** <br>
- You must activate the virtual environment in the project: **source employee/bin/active**
- You must install requirements: **pip install requirements.txt**
- You should have a PostgreSQL database called **employeeapi**.
  - When the first time it is run, app.on_startup.append(create_table) line needs to be removed from the comment line for the **Employee** table to be created. Then, you can add the comment line.
- You must have an aws s3 for use in the project. Create s3 on AWS and write s3 bucket name in **settings.py** file.
- Then you can run the project: **python main.py**
- And done. :tada:
