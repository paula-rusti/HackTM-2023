format:
	isort -rc .
	black .
pack:
	tar --exclude='venv' --exclude='.pytest_cache' --exclude='__pycache__' -czvf bme680-reader.tar.gz ./*