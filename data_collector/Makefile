SHELL=/bin/bash #-e pipefail

CONFIG_PATH=config.json
COURCES=./sources/*.py
RESULT=./result

.PHONY: install_packages format check receive_data post_processing

install_packages:
	sudo pip install -r requirements.txt

format:
	autopep8 --in-place $(SOURCES)

check:
	pylint $(SOURCES) --disable=missing-module-docstring,missing-function-docstring,missing-class-docstring,wrong-import-position

receive_data:
	...

post_processing:
	...

