format:
	isort -rc .
	black .
pack:
	tar --exclude='venv' --exclude='.pytest_cache' --exclude='__pycache__' -czvf bme680-reader.tar.gz ./*
deploy:
	echo 'put bme680-reader.tar.gz' | sftp paula@paulapi.local:/home/paula/bme680-reader/