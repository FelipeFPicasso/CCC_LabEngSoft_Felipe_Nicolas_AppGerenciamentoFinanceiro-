# help
.PHONY: help
help:
	@echo "\nComando disponivel:"
	@echo "initialize-all" 
	@echo "\o comando acima
	@echo "Exclui BD atual, recria .venv (se necessario) e inicia"
	@echo ".venv é recriado somente se ainda nao estiver instanciado"

#Variaveis
PYTHON = python3
VENV_PATH = .venv
VENV_PYTHON = $(VENV_PATH)/bin/python
PIP = $(VENV_PATH)/bin/pip

#start
.PHONY: start
start:
	python main.py

#initialize
.PHONY: initialize-all
initialize-all: $(VENV_PATH)
	service postgresql start
	sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"
	sudo -u postgres psql -c "DROP DATABASE IF EXISTS financeiro;"
	$(VENV_PYTHON) main.py
	
$(VENV_PATH):
	$(PYTHON) -m venv $(VENV_PATH)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

#start
.PHONY: start
start: postgres
	$(VENV_PYTHON) main.py

postgres:
	service postgresql start