server-dev:
	flask --app ./src/app run --debug
setup-dev:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	sudo npm install -g prettier
format:
	black src
	npx prettier . --write
lint:
	pylint src
