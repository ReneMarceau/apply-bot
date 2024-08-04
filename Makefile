# Colors for logging
COLOR_RESET = \033[0m
COLOR_INFO = \033[1;34m
COLOR_SUCCESS = \033[1;32m
COLOR_ERROR = \033[1;31m

# Variables
ENV_FILE = .env
ENV_TEMPLATE = .env.template
VENV_DIR = venv
REQ_FILE = requirements.txt

# Default rule
.PHONY: all
all:
	@echo "${RED}Please specify a command.${RESET}"
	@make help

# Rule to display help
.PHONY: help
help:
	@echo "$(COLOR_INFO)Usage: make [command]$(COLOR_RESET)"
	@echo "$(COLOR_INFO)Commands:$(COLOR_RESET)"
	@echo "$(COLOR_INFO)  run:$(COLOR_RESET) Run the application"
	@echo "$(COLOR_INFO)  check:$(COLOR_RESET) Check if everything is setup"
	@echo "$(COLOR_INFO)  install:$(COLOR_RESET) Install dependencies"
	@echo "$(COLOR_INFO)  format:$(COLOR_RESET) Format code"
	@echo "$(COLOR_INFO)  clean:$(COLOR_RESET) Clean up"

# Rule to run the application
.PHONY: run
run:
	@echo "$(COLOR_INFO)Running the application...$(COLOR_RESET)"
	@$(VENV_DIR)/bin/python src/main.py

# Rule to check if everything is setup
.PHONY: check
check: create-env install
	@echo "$(COLOR_SUCCESS)Everything is setup!$(COLOR_RESET)"

# Rule to create the .env file
.PHONY: create-env
create-env:
	@if [ ! -f "$(ENV_FILE)" ]; then \
		echo "$(COLOR_INFO)Creating .env file...$(COLOR_RESET)"; \
		python3 scripts/create_env.py; \
		echo "$(COLOR_SUCCESS).env file created!$(COLOR_RESET)"; \
	else \
		echo "$(COLOR_SUCCESS).env file already exists.$(COLOR_RESET)"; \
	fi

# Rule to check and create the virtual environment
.PHONY: create-venv
create-venv:
	@echo "$(COLOR_INFO)Checking for virtual environment...$(COLOR_RESET)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(COLOR_INFO)Creating virtual environment...$(COLOR_RESET)"; \
		python3 -m venv $(VENV_DIR); \
		echo "$(COLOR_SUCCESS)Virtual environment created!$(COLOR_RESET)"; \
		echo "To activate the virtual environment, run: $(COLOR_INFO)source $(VENV_DIR)/bin/activate"; \
	else \
		echo "$(COLOR_SUCCESS)Virtual environment already exists.$(COLOR_RESET)"; \
	fi

# Rule to install dependencies
.PHONY: install
install: create-venv
	@echo "$(COLOR_INFO)Installing dependencies...$(COLOR_RESET)"
	@$(VENV_DIR)/bin/pip install -r $(REQ_FILE)
	@echo "$(COLOR_SUCCESS)Dependencies installed!$(COLOR_RESET)"

# Rule to format code
.PHONY: format
format:
	@echo "$(COLOR_INFO)Formatting code...$(COLOR_RESET)"
	@$(VENV_DIR)/bin/black src/
	@echo "$(COLOR_SUCCESS)Code formatted!$(COLOR_RESET)"

.PHONY: clean
clean:
	@echo "$(COLOR_INFO)Cleaning up...$(COLOR_RESET)"
	@echo "$(COLOR_INFO)Removing virtual environment...$(COLOR_RESET)"
	@rm -rf $(VENV_DIR)
	@echo "$(COLOR_INFO)Removing .env file...$(COLOR_RESET)"
	@rm -f $(ENV_FILE)
	@echo "$(COLOR_INFO)Removing __pycache__ directories...$(COLOR_RESET)"
	@find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "$(COLOR_SUCCESS)Cleanup done!$(COLOR_RESET)"
