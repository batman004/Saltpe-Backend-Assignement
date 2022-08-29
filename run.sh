cd app

docker-compose --env-file .env  up --build

alembic init

docker-compose run web alembic revision --autogenerate -m "First migration"

docker-compose run web alembic upgrade head
