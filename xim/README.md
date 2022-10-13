# webserver

### functionality

- **GET /user/<id>** fetch user by id
- **GET /user?email=<email>** fetch user by email
- **POST /signup body={ email, password }** create new user and login
- **POST /login body={ email, password }** login
- **GET /logout** logout

### start dev

1. `docker stop CONTAINER_NAME` (if running)

2. `docker rm CONTAINER_NAME` (if created)

3. `docker run --name CONTAINER_NAME -p 5455:5432 -e POSTGRES_USER=POSTGRES_USER -e POSTGRES_PASSWORD=POSTGRES_PASSWORD -e POSTGRES_DB=POSTGRES_DB -d postgres`

4. `start venv` (if deactivated)

5. `python3 init_db.py`

6. `python3 app.py`