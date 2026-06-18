dev:
	docker compose -f docker-compose.dev.yaml up -d

prod:
	docker compose -f docker-compose.prod.yaml up -d

down-dev:
	docker compose -f docker-compose.dev.yaml down

down:
	docker compose -f docker-compose.prod.yaml down

build:
	docker compose -f docker-compose.prod.yaml build --no-cache

logs:
	docker compose -f docker-compose.prod.yaml logs -f

logs-acme:
	docker compose -f docker-compose.prod.yaml logs -f nginx-proxy-acme
