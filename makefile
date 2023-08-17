SHELL := bash
python_version = python3.11
venv_path = .venv
# Using $$() instead of $() to run evaluation only when it's accessed
py = $$(if [ -d $(PWD)/'$(venv_path)' ]; then echo $(PWD)/"$(venv_path)/bin/python3"; else echo "$(python_version)"; fi)
pip = $(py) -m pip

.DEFAULT_GOAL := help
.PHONY: help
help: ## Display this help section
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\$$/]+.*:.*?##\s/ {printf "\033[36m%-38s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

venv: requirements.txt ## Build the virtual environment
	@$(python_version) -m venv $(venv_path)
	@touch $(venv_path)

install: requirements.txt ## Install without venv
	@$(pip) install -U pip setuptools wheel build
	@$(pip) install -r requirements.txt
	@$(pip) install .

poetry: venv ## Install poetry in venv
	@$(pip) install -U pip setuptools
	@$(pip) install poetry

activate: ## Activate venv
	@source $(venv_path)/bin/activate && exec zsh
