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
create-db:
	cd backend/db && python3 main.py create 
update-db:
	cd backend/db && python3 main.py update


server:
	sudo apt update && sudo apt install -y python3 python3-pip ffmpeg cron 
	flask --app ./backend/app run --host=0.0.0.0 --port=80
