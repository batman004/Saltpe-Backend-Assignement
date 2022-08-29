cd app

docker-compose run server alembic revision --autogenerate -m "First migration"

docker-compose run server alembic upgrade head

docker-compose run server
