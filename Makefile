server-dev:
	flask --app ./backend/app run --debug
web-dev:
	npx http-server public -c-1
dev:
	make server-dev & make web-dev
setup-dev:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	sudo npm install -g http-server
