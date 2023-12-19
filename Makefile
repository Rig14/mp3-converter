server-dev:
	make reset-db
	flask --app ./backend/app run --debug
web-dev:
	npx http-server public -c-1 --cors
install:
	pip install -r requirements.txt
	sudo npm install -g http-server


reset-db:
	cd backend/db && python3 main.py reset
	make add-admin 
create-db:
	cd backend/db && python3 main.py create 
update-db:
	cd backend/db && python3 main.py update
add-admin:
	cd backend/db && python3 main.py add_admin

init-db:
	make create-db
	make add-admin