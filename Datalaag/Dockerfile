FROM python:3.10-slim

WORKDIR /azuredb_connect

RUN apt-get update && apt-get install -y libpq-dev gcc && apt-get clean

COPY . /azuredb_connect/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5200

ENV FLASK_APP=azuredb_connect.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5200

CMD ["flask", "run"]
