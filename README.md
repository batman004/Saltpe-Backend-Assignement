# Salt-Backend-Assignement

### Tech Stack
Backend REST API
 - Python(FastAPI)
 - PostgreSQL
### API Routes

#### `users` Module

Routes | HTTP | Description
--- | --- | ---
**/user/login** | `POST` | Login a user
**/user/logout** | `POST` | Logout a user
**/user/me** | `GET` | Get user data for currently logged in user(based on token verification)
**/user/signup** | `POST` | Signup a new user

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
