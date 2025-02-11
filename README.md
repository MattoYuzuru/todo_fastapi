# University To-Do App

A lightweight and intuitive **task management application** designed for university students to boost productivity.

## Features

_What I want/ed to implement to my app_

1. Task management with categories and priorities.
2. Calendar integration.
3. Pomodoro timer in each todo task.
5. Collaboration for projects.
6. Visual statistics.
7. Streak tracking.
8. Friendly design.

## Project Structure

```
todo_fastapi
├───.env
├───.env_db
├───.gitignore
├───LICENCE
├───README.md
├───alembic.ini
├───backend
│   ├───Dockerfile
│   ├───alembic
│   │   ├───README
│   │   ├───env.py
│   │   ├───script.py.mako
│   │   └───versions
│   │       ├───79fbd9de33e5_add_total_time_spent_cur_streak_to_todo_.py
│   │       └───d73804355bae_initial_migration.py
│   ├───app
│   │   ├───__init__.py
│   │   ├───auth.py
│   │   ├───config.py
│   │   ├───crud
│   │   │   ├───__init__.py
│   │   │   ├───todo_crud.py
│   │   │   └───user_crud.py
│   │   ├───db
│   │   │   ├───__init__.py
│   │   │   └───session.py
│   │   ├───main.py
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
│   ├───requirements.txt
│   └───tests
│       ├───__init__.py
│       └───test_todo.py
├───docker-compose.yml
└───frontend
    ├───Dockerfile
    ├───babel.config.js
    ├───jsconfig.json
    ├───package-lock.json
    ├───package.json
    ├───public
    │   └───favicon.ico
    ├───src
    │   ├───App.vue
    │   ├───assets
    │   │   └───custom.css
    │   ├───components
    │   │   ├───AddTodo.vue
    │   │   ├───HomePage.vue
    │   │   ├───PomodoroPage.vue
    │   │   ├───TimerPage.vue
    │   │   ├───TodoDetails.vue
    │   │   ├───TodoList.vue
    │   │   ├───UserLogin.vue
    │   │   └───UserRegister.vue
    │   ├───main.js
    │   ├───router
    │   │   └───index.js
    │   └───store
    │       └───index.js
    └───vue.config.js
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


# Getting Started
To get a local copy up and running, follow these steps.


#### Clone the repository:

```bash

git clone https://github.com/MattoYuzuru/todo_fastapi.git
cd todo_fastapi
```

#### Configure all .env files

Run this command and copy the secret key


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


#### Run docker-compose to start Todo App

```bash

docker compose up -d --build
```


#### Access Site
http://localhost:8080/register

## Contributing

Contributions are welcome! This is my first time using these technologies.
