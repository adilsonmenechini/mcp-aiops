.PHONY: help tools start stop logs test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make start client=cli   - Start CLI client with MCP servers"
	@echo "  make start client=ui    - Start UI (Streamlit) client with MCP servers"
	@echo "  make tools client=cli   - Start only MCP servers for CLI client"
	@echo "  make tools client=ui    - Start only MCP servers for UI client"
	@echo "  make stop client=cli    - Stop CLI client and servers"
	@echo "  make stop client=ui     - Stop UI client and servers"
	@echo "  make logs client=cli    - Show logs for CLI client"
	@echo "  make logs client=ui     - Show logs for UI client"
	@echo "  make test client=cli    - Run CLI client test"
	@echo "  make clean              - Clean all containers and volumes"

# Validate client type
validate-client:
	@if [ "$(CLIENT)" != "cli" ] && [ "$(CLIENT)" != "ui" ]; then \
		echo "Error: CLIENT must be 'cli' or 'ui'"; \
		echo "Usage: make start cli  or  make start ui"; \
		exit 1; \
	fi

# Start services based on client type
start: validate-client
ifeq ($(CLIENT),cli)
	@echo "Starting CLI client with MCP servers..."
	docker compose -f docker-compose-cli.yaml up --build -d
else ifeq ($(CLIENT),ui)
	@echo "Starting UI client with MCP servers..."
	docker compose -f docker-compose-ui.yaml up --build -d
endif

# Start only MCP servers based on client type
tools: validate-client
ifeq ($(CLIENT),cli)
	@echo "Starting MCP servers for CLI client..."
	docker compose -f docker-compose-cli.yaml up --build -d mcpduckduckgo mcpdatadog
else ifeq ($(CLIENT),ui)
	@echo "Starting MCP servers for UI client..."
	docker compose -f docker-compose-ui.yaml up --build -d mcpduckduckgo mcpdatadog
endif

# Stop services based on client type
stop: validate-client
ifeq ($(CLIENT),cli)
	@echo "Stopping CLI client and servers..."
	docker compose -f docker-compose-cli.yaml down --volumes --remove-orphans
else ifeq ($(CLIENT),ui)
	@echo "Stopping UI client and servers..."
	docker compose -f docker-compose-ui.yaml down --volumes --remove-orphans
endif

# Show logs based on client type
logs: validate-client
ifeq ($(CLIENT),cli)
	@echo "Showing logs for CLI client..."
	docker compose -f docker-compose-cli.yaml logs -f
else ifeq ($(CLIENT),ui)
	@echo "Showing logs for UI client..."
	docker compose -f docker-compose-ui.yaml logs -f
endif

# Test CLI client (only available for CLI)
test:
	@if [ "$(CLIENT)" != "cli" ]; then \
		echo "Error: Test is only available for CLI client"; \
		echo "Usage: make test cli"; \
		exit 1; \
	fi
	@echo "Running CLI client test..."
	docker exec -it hostclient python main.py

# Start CLI client in host mode (interactive)
host:
	@echo "Starting CLI client in host mode..."
	docker compose -f docker-compose-cli.yaml up --build hostclient

# Clean all containers and volumes
clean:
	@echo "Cleaning all containers and volumes..."
	docker compose -f docker-compose-cli.yaml down --volumes --remove-orphans 2>/dev/null || true
	docker compose -f docker-compose-ui.yaml down --volumes --remove-orphans 2>/dev/null || true
	docker system prune -f