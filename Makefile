run:
	docker-compose build
	docker-compose up -d
	docker exec library_app python manage.py collectstatic --noinput --clear

migrate:
	docker exec library_app python manage.py migrate

seed:
	docker exec library_app python manage.py user_seeder
	docker exec library_app python manage.py book_seeder
