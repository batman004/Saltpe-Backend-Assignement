# Salt-Backend-Assignement

⚠️ Deployment Paused for now

### Technologies Used
Backend REST API
 - Python(FastAPI)
 - PostgreSQL
 - JWT Tokens for authorization
 - Containerized via Docker 
 - Deployed on [Railway](https://railway.app/) at [endpoint](https://saltpe-backend-assignment-production.up.railway.app/)

Frontend
 - HTML, Bootstrap CSS and JS 
 - Deployed on Cloudflare Pages at [Link](https://saltpe-backend-assignment.pages.dev/)

### API Routes

#### `users` Module

Routes | HTTP | Description
--- | --- | ---
**/user/login** | `POST` | Login a user
**/user/logout** | `POST` | Logout a user
**/user/me** | `GET` | Get user data for currently logged in user(based on token verification)
**/user/signup** | `POST` | Signup a new user


### Directory Structure

```
├── README.md
├── app
│   ├── __init__.py
│   ├── alembic
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── 9ed0fc4984ca_first_migration.py
│   ├── api
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── users
│   │       ├── __init__.py
│   │       ├── auth
│   │       │   ├── __init__.py
│   │       │   ├── hashing.py
│   │       │   ├── jwt.py
│   │       │   └── utils.py
│   │       ├── endpoints
│   │       │   ├── __init__.py
│   │       │   ├── models.py
│   │       │   ├── routers.py
│   │       │   └── serializers.py
│   │       ├── handlers
│   │       │   ├── __init__.py
│   │       │   └── user_handler.py
│   │       └── utils
│   │           ├── __init__.py
│   │           ├── blacklist_db.txt
│   │           └── blacklist_tokens.py
│   ├── db
│   │   └── 01-init.sh
│   ├── docker-compose.yaml
│   ├── main.py
│   ├── requirements.txt
│   └── server.Dockerfile
├── build.sh
└── run.sh
```

### Steps to run
Open your terminal and run the following commands
```
git clone https://github.com/batman004/Saltpe-Backend-Assignement.git
cd Saltpe-Backend-Assignement
```
add a `.env` file inside `./app` (refer .env.example)

Initialise alembic
```
rm -r alembic // delete the existing folder first
alembic init alembic
```

open the `alembic.ini` file with your editor and change line 38 from

```
sqlalchemy.url = driver://user:pass@localhost/dbname
```
to
```
sqlalchemy.url =
```

Next, we will add the postgres db url in the `alembic/env.py` file (refer the given file)


Dockerize the project by running the following script
```
sh build.sh
```

Next create your first database migration via alembic and spin up the server via Docker

```
sh run.sh
```

The server will start running at `port:8000`


Sample payloads

1. Logging in a user

```
curl --location --request POST 'http://localhost:8000/user/login' \
--header 'Content-Type: application/json' \
--data-raw '{
  "email": "user@mail.com",
  "password": "password"
}'
```

2. Getting details about current user

```
curl --location --request GET 'http://localhost:8000/user/me' \
--header 'Authorization: Bearer {{token}}'

```
3. Signing up a new user

```
curl --location --request POST 'http://localhost:8000/user/signup' \
--header 'Content-Type: application/json' \
--data-raw '{
  "first_name": "xyz",
  "last_name": "abc",
  "username": "spidey",
  "email": "abs1s@mail.com",
  "password": "123"
}'

```
4. Logging out a user

```
curl --location --request POST 'http://localhost:8000/user/logout' \
--header 'Authorization: Bearer {{token}}'
```
