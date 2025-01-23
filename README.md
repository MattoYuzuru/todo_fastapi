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

├───.env \
├───.gitignore\
├───LICENCE\
├───README.md\
├───backend\
│   backend\
│   ├───Dockerfile\
│   ├───app\
│   │   app\
│   │   ├───__init__.py\
│   │   ├───config.py\
│   │   ├───crud\
│   │   │   crud\
│   │   │   ├───__init__.py\
│   │   │   └───todo_crud.py\
│   │   ├───db\
│   │   │   db\
│   │   │   ├───__init__.py\
│   │   │   └───session.py\
│   │   ├───main.py\
│   │   ├───models\
│   │   │   models\
│   │   │   ├───__init__.py\
│   │   │   ├───base.py\
│   │   │   ├───todo_item.py\
│   │   │   └───user.py\
│   │   ├───routes\
│   │   │   routes\
│   │   │   ├───__init__.py\
│   │   │   └───todo_router.py\
│   │   └───schemas\
│   │       schemas\
│   │       ├───__init__.py\
│   │       └───todo_schemas.py\
│   └───tests\
│       tests\
│       ├───__init__.py\
│       └───test_todo.py\
├───docker-compose.yml\
├───frontend\
│   frontend\
│   ├───package.json\
│   ├───public\
│   │   public\
│   ├───src\
│   │   src\
│   │   ├───App.vue\
│   │   ├───components\
│   │   │   components\
│   │   │   ├───AddToDo.vue\
│   │   │   └───ToDoList.vue\
│   │   ├───main.js\
│   │   ├───router\
│   │   │   router\
│   │   │   └───index.js
│   │   └───views\
│   │       views\
│   │       └───Home.vue\
│   └───store\
│       store\
│       └───index.js\
└───requirements.txt


## Requirements and Installation

Python 3.11 or higher \
Docker (I used it for hosting) \
Backend (FastAPI) \
Frontend (Vue.js)

### Clone the repository:

```bash
git clone https://github.com/MattoYuzuru/todo_fastapi.git
cd todo_fastapi

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Fill your .env file

This command is for secret key for user auth.
```bash

openssl rand -hex 32
```

Tech Stack
FastAPI, Alchemy, Alembic, PostgreSQL
Frontend: Vue.js
Deployment: Docker, Nginx, etc

## Contributing

Contributions are welcome! My code is bad pls comment :(
