# backend

    - Python version: 3.11.3
    - pip verison: 22.3

## Project structure

```
ITA-APP-SERVER
└───src
|   │   └───app
|   │   |   ├───crud         # crud services
|   │   |   ├───db           # database connection and config
|   │   |   ├───models       # db models
|   │   |   ├───routers
|   │   |   ├───schemas      # pydantic models
|   │   |   ├───constants    # local configs
|   │   |   ├───utils        # local utils such as logging module
|   │   |   ├───api.py
|   │   |   ├───Dockerfile
|   │   |   ├───poetry.lock
|   │   |   ├───pyproject.toml
|   |   |___logs             # include log files
```

### Development
Run docker

```
docker compose --profile dev up --build -d
```
