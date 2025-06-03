# Technical assessment
NOTE: Steps are provided for Linux

<!--TOC-->

- [Technical assessment](#technical-assessment)
  - [Setup Environment](#setup-environment)
  - [Run DB](#run-db)
  - [Configure .env file](#configure-env-file)
  - [Run application](#run-application)
  - [Testing the application](#testing-the-application)

<!--TOC-->


## Setup Environment

Source: https://docs.astral.sh/uv/

For new project
    uv init PROJECT_NAME
a. Create Virtual Environment
    uv venv
b. Activate venv
    source .venv/bin/activate
To add Livraries
    uv add LIBRARY_NAME
To sync uv:
    uv sync
To Deactivate venv
    deactivate


## Run DB

a. Install neo4j steps:
Source:https://neo4j.com/docs/operations-manual/current/installation/linux/debian/
b. Configurations ne4oj:
Source: https://www.linode.com/docs/guides/installing-and-configuring-neo4j-on-ubuntu-2204/
c. Install neo4j extension for VSCode:
Source: https://neo4j.com/blog/developer/run-cypher-without-leaving-your-ide-with-neo4j-vscode-extension/
d. Start/Stop DB:
    sudo service neo4j start
    sudo service neo4j stop


## Configure .env file

Example:
    AUTH_USERNAME=user
    AUTH_PASSWORD=pass
    DB_PREFIX=neo4j
    DB_HOST_NAME=127.0.0.1:7687
    DB_NAME=neo4j
    DB_USERNAME=neo4j
    DB_PASSWORD=12345678


## Run application

a. run
    PYTHONPATH="./app" uvicorn app.main:app --reload
b. lauch.json for debug mode:
    {
        // Use IntelliSense to learn about possible attributes.
        // Hover to view descriptions of existing attributes.
        // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python Debugger: FastAPI",
                "type": "debugpy",
                "request": "launch",
                "module": "uvicorn",
                "env": {"PYTHONPATH": "app"},
                "args": [
                    "app.main:app",
                    "--reload"
                ],
                "jinja": true
            }
        ]
    }
c. Endpoints and Doc:
    http://127.0.0.1:8000/docs


## Testing the application

For PyTest:
    pytest

For PyTest with coverage:
    pytest --cov
