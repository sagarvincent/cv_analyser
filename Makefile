dev:
	docker compose -f docker-compose.dev.yaml up -d

prod:
	docker compose up -d

down-dev:
	docker compose -f docker-compose.dev.yaml down

down:
	docker compose down

build:
	docker compose build --no-cache

logs:
	docker compose logs -f

logs-acme:
	docker compose logs -f nginx-proxy-acme
