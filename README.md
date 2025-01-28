# University To-Do App

A lightweight and intuitive **task management application** designed for university students to boost productivity.

## Features

_What I want/ed to implement to my app_

1. Task management with categories and priorities.
2. Calendar integration.
3. Pomodoro timer in each todo task.
5. Collaboration for group projects.
6. Visual statistics.
7. Gamification with rewards and streak tracking.
8. Mobile-friendly design.

Getting Started
To get a local copy up and running, follow these steps.


## Project Structure

```
├───.env 
├───.env_db 
├───.gitignore
├───LICENCE
├───README.md
├───backend
│   ├───Dockerfile
│   ├───app
│   │   ├───__init__.py
│   │   ├───config.py
│   │   ├───auth.py
│   │   ├───main.py
│   │   ├───requirements.txt
│   │   ├───crud
│   │   │   ├───__init__.py
│   │   │   ├───todo_crud.py
│   │   │   └───user_crud.py
│   │   ├───db
│   │   │   ├───__init__.py
│   │   │   └───session.py
│   │   ├───models
│   │   │   ├───__init__.py
│   │   │   ├───base.py
│   │   │   ├───todo_item.py
│   │   │   └───user.py
│   │   ├───routes
│   │   │   ├───__init__.py
│   │   │   ├───todo_router.py
│   │   │   └───user_router.py
│   │   └───schemas
│   │       ├───__init__.py
│   │       ├───todo_schemas.py
│   │       ├───token_schemas.py
│   │       └───user_schemas.py
│   └───tests
│       ├───__init__.py
│       └───test_todo.py
├───frontend
│   ├───Dockerfile
│   ├───package.json
│   ├───public
│   ├───src
│   │   ├───App.vue
│   │   ├───components
│   │   │   ├───AddToDo.vue
│   │   │   ├───ToDoList.vue
│   │   │   └───Timer.vue
│   │   ├───main.js
│   │   ├───router
│   │   │   └───index.js
│   │   └───views
│   │       ├───Home.vue
│   │       ├───Login.vue
│   │       ├───Register.vue
│   │       └───Pomodoro.vue
│   └───store
│       └───index.js
└───docker-compose.yml
```

## Tech Stack
Backend: 
* FastAPI

DB, ORM, migrations management:
* PostgreSQL
* Alchemy
* Alembic

Frontend: 
* Vue.js

Deployment:
* Docker
* Nginx

etc


## Requirements and Installation

* Python 3.11 or higher 
* Docker 
* Backend (FastAPI) 
* Frontend (Vue.js) 

#### Clone the repository:

```bash

git clone https://github.com/MattoYuzuru/todo_fastapi.git
cd todo_fastapi

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configure all .env files

Run this command and copy the secret key\
It's for User Authentication (SECRET_KEY in .env)
```bash

openssl rand -hex 32
```

There are 2 .env in my project. 
1) .env (for all config variables)
```
DATABASE_URL=postgresql+psycopg2://username:password@localhost:port/db_name
SECRET_KEY=your_key
ALGORITHM=HS256
```
2) .env_db (to run postrgesql via its docker image)
```
POSTGRES_USER=username
POSTGRES_PASSWORD=password
POSTGRES_DB=db_name
```

#### Frontend installations
Install nodejs npm (if not installed)

Then run this:
```bash

nmp install frontend/package.json
```


#### Run docker-compose to init data base

```bash

docker compose up -d
```

## Contributing

Contributions are welcome! My code is bad pls comment :(
