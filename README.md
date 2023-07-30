# Steps

1.  Create virtual env
    `python3 -m venv "env_name"`

        1.1 Set to use venv interpreter for VSCode
        Python:Select Interpreter >> Select venv bin/python

        1.2 Set terminal to use venv python interpreter
        `source env_name/bin/activate`

2.  Install [FastAPI](https://fastapi.tiangolo.com/tutorial/) (make sure you use venv interpreter)

    `pip install fastapi`

    `pip freeze` #to see all packages installed

    `pip install "uvicorn[standard]"`

3.  start the server
    `uvicorn _main_script_loc_:_fastAPI_instance_name_ --reload`
    Ex: `uvicorn app.main:app --reload`

4.  API docs
    `/doc` or `/redoc` routes of the host server URL will give Swagger or Redoc API documentation automatically

5.  Create modules
    Adding `__init__.py` inside a folder will make it a module

6.  Database constraints
    `NOT NULL`
    `UNIQUE`

7.  Packages
    - [Psycopg](https://www.psycopg.org/docs/): 
        
        - Python PostgreSQL database adapter
        
            `pip install psycopg2-binary`

    - [sqlalchemy](https://docs.sqlalchemy.org/en/20/tutorial/index.html) 
        - it is an ORM(Object Relation Mapper) - it let us use Python to interact with DB, and abstract away SQL - under the hood uses psycopg
        
            `pip install SQLAlchemy==1.4.49`

    - [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
        - If you update any tables, you have to drop current tables and replace it with the new old. While dropping you could loose the data that already exist. This is coz, sqlAlchemy don't push the table schema changes if the table is already present in the DB.
        - it can keep track of changes to DB and tables

        `alembic init __dir__`


8.  [PostgresSQL](https://www.postgresqltutorial.com/)

    - Composite key
        - primary keys that span more than one column
        - there might be duplicate in a column, but the row-wise combination of entries will be unique
 