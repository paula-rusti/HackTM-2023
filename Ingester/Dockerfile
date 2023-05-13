FROM python:3.10.11-slim-bullseye

WORKDIR /app

# copy requirements
COPY requirements.txt /app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# copy code
COPY . .

CMD python3 data_reader.py