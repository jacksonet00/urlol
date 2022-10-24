# urlol
by Jackson Taylor

### run in development mode

1. `docker stop CONTAINER_NAME` (if running)

2. `docker rm CONTAINER_NAME` (if created)

3. `docker run --name CONTAINER_NAME -p 5455:5432 -e POSTGRES_USER=POSTGRES_USER -e POSTGRES_PASSWORD=POSTGRES_PASSWORD -e POSTGRES_DB=POSTGRES_DB -d postgres`

4. `start venv` (if deactivated)

5. `python3 init_db.py`

6. `python3 app.py`'

GET '/' -- Dashboard
GET '/search?q={query}' -- Search
