server-dev:
	make erase-db
	pip install -r requirements.txt
	pip install -r dev-requirements.txt
	flask --app ./backend/app run --debug
web-dev:
	sudo npm install -g http-server
	npx http-server public -c-1
erase-db:
	cd backend && python db.py erase_database && python db.py update
update-db:
	cd backend && python db.py update
dev:
	make server-dev & make web-dev
