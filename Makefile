server-dev:
	flask --app ./backend/app run --debug
web-dev:
	npx http-server public
dev:
	make server-dev & make web-dev
setup-dev:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	sudo npm install -g prettier http-server
format:
	black backend
	npx prettier . --write
lint:
	pylint backend
