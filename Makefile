include .env
export

show-env:
	@echo $(APP_ENV)

init:
	make destroy
	docker-compose build --no-cache
	make install-packages
up:
	make down
	docker-compose up $(OPT)

down:
	docker-compose down

destroy:
	make down -v
	docker container ls -a -qf name=$(COMPOSE_PROJECT_NAME) | xargs --no-run-if-empty docker container rm
	docker network   ls -qf    name=$(COMPOSE_PROJECT_NAME) | xargs --no-run-if-empty docker network rm
	docker volume    ls -qf    name=$(COMPOSE_PROJECT_NAME) | xargs --no-run-if-empty docker volume rm

install-packages:
	docker-compose run --rm python    bash -c "rm -rf site-packages/*; pip install -r requirements.txt -t site-packages --force-reinstall --upgrade"
	docker-compose run --rm vue npm install

shell:
	docker-compose exec python bash

be-check:
	docker-compose exec python ruff check  .

fe-lint:
	docker-compose exec vue npm run lint

fe-format:
	docker-compose exec vue npm run format

exec:
	@docker-compose exec $(args)

exec-be:
	@make exec args="python bash"

ps:
	@docker-compose ps

logs:
	@tail -f backend/src/storage/logs/python.log | jq -r -R 'fromjson? | . ${args}'

logs-error:
	@make logs args='| select(.log_level=="ERROR")'

logs-debug:
	@make logs args='| select(.log_level=="DEBUG")'

logs-info:
	@make logs ARGS='| select(.log_level=="INFO")'
