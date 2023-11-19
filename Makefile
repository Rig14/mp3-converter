server-dev:
	make reset-db
	flask --app ./backend/app run --debug
web-dev:
	npx http-server public -c-1 --cors
install:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	sudo npm install -g http-server



reset-db:
	cd backend/db && python3 main.py reset 
update-db:
	cd backend/db && python3 main.py update