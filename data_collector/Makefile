SHELL=/bin/bash #-e pipefail

CONFIG_PATH=config.json
SOURCES=./sources/*.py
RESULT=./result

all: install_packages format check receive_data post_process

install_packages:
	sudo pip install -r requirements.txt

format:
	autopep8 --in-place --max-line-length 80 $(SOURCES)

check:
	pylint $(SOURCES) --disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,wrong-import-position,line-too-long,logging-fstring-interpolation,wrong-import-order,broad-except,too-many-locals,invalid-name

receive_data:
	python3 ./sources/main_receive_data.py $(CONFIG_PATH)

post_process:
	python3 ./sources/main_post_process.py $(CONFIG_PATH)

async: receive_data_async post_process_async

receive_data_async:
	nohup python3 ./sources/main_receive_data.py $(CONFIG_PATH) &

post_process_async:
	nohup python3 ./sources/main_post_process.py $(CONFIG_PATH) &
