SHELL=/bin/bash #-e pipefail

CONFIG_PATH=config.json
SOURCES=./sources/*.py
RESULT=./result

all: install_packages format check receive_data

install_packages:
	sudo pip install -r requirements.txt

format:
	autopep8 --in-place --max-line-length 80 $(SOURCES)

check:
	pylint $(SOURCES) --disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,wrong-import-position,line-too-long

receive_data:
	python ./sources/main.py $(CONFIG_PATH)
