# Steps

1.  Create virtual env
    `python3 -m venv "env_name"`

        1.1 Set to use venv interpreter for VSCode
        Python:Select Interpreter >> Select venv bin/python

        1.2 Set terminal to use venv python interpreter
        `source env_name/bin/activate`

2.  Install fastAPI(make sure you use venv interpreter)

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

7. Packages
    Psycopg: Python PostgreSQL database adapter
    `pip install psycopg2-binary`

    sqlalchemy
        - it is an ORM(Object Relation Mapper)
        - it let us use Python to interact with DB, and abstract away SQL
        - under the hood uses psycopg
    `pip install SQLAlchemy==1.4.49`
