FROM	python:3.12-slim

ENV	PYTHONUNBUFFERED=1

WORKDIR	/app

RUN	apt-get update && apt-get install -y --no-install-recommends \
	curl \
	&& rm -rf /var/lib/apt/lists/*

COPY	requirements.txt .
RUN	pip install --no-cache-dir -r requirements.txt

RUN	chmod +x /app/deploy/entrypoint.sh

COPY 	. .

ENTRYPOINT ["/app/deploy/entrypoint.sh"]
