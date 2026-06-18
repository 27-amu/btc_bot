install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run:
	python bot.py

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=bot --cov-report=term-missing

lint:
	python -m py_compile bot.py && echo "Syntax OK"

docker-build:
	docker build -t btc_bot .

docker-run:
	docker run --env-file .env btc_bot

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov trades_*.csv
