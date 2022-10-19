# urlol
by Jackson Taylor

### todo

- implement react renderer
    - write login page
    - write shortcut manager page
- use decoded session for uid rather than passing in json body or query param

### webserver functionality

- **GET /user/<id>** fetch user by id
- **GET /user?email=<email>** fetch user by email
- **POST /signup body={ email, password }** create new user and login
- **POST /login body={ email, password }** login
- **GET /logout** logout
- **GET /alias body={ user_id } cookie={ urlol-uid }** fetch list of user's aliases
- **GET /alias/<id>** fetch alias by id
- **POST /alias body={ user_id, name, url }** create alias
- **GET /shortcut body={ user_id } cookie={ urlol-uid }** fetch list of user's aliases
- **GET /shortcut/<id>** fetch shortcut by id
- **POST /shortcut body={ user_id, prefix, website }** create shortcut
- **GET /search?q={query}&uid={user_id}** make search request

### run in development mode

1. `docker stop CONTAINER_NAME` (if running)

2. `docker rm CONTAINER_NAME` (if created)

3. `docker run --name CONTAINER_NAME -p 5455:5432 -e POSTGRES_USER=POSTGRES_USER -e POSTGRES_PASSWORD=POSTGRES_PASSWORD -e POSTGRES_DB=POSTGRES_DB -d postgres`

4. `start venv` (if deactivated)

5. `python3 init_db.py`

6. `python3 app.py`