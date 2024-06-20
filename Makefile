REDIS_TEST_HOST=redis-test

up:
	docker-compose -f docker-compose.yml up --build

down:
	docker-compose -f docker-compose.yml down

test:
	REDIS_HOST=$(REDIS_TEST_HOST) docker-compose -f docker-compose.test.yml run --rm test pytest --maxfail=1 --disable-warnings -v
