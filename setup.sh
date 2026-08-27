#!/bin/bash
apt-get update
apt-get install -y openssh-client unzip curl
curl -LO https://github.com/duckdb/duckdb/releases/download/v1.2.0/duckdb_cli-linux-amd64.zip
unzip -o duckdb_cli-linux-amd64.zip -d /usr/local/bin/
rm duckdb_cli-linux-amd64.zip
