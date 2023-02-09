# Setup virtual python environment
Optionally, you can use a [virtual python](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) environment to keep dependencies separate. The _venv_ module is the preferred way to create and manage virtual environments. 

 ```console
python3 -m venv env
```

Before you can start installing or using packages in your virtual environment you’ll need to activate it.

```console
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
 ```


# Federated timeline
These are the most recent public posts from people on this and other servers of the decentralized network that this server knows about.
https://data-folks.masto.host/public

# Proudcer
python mastodonlisten.py --baseURL https://data-folks.masto.host/ --enableKafka

# Kafka Connect

confluent-hub install confluentinc/kafka-connect-s3:10.3.0

curl -X PUT -H  "Content-Type:application/json" localhost:8083/connectors/mastodon-sink-s3/config -d '@./config/mastodon-sink-s3.json'

curl -X PUT -H  "Content-Type:application/json" localhost:8083/connectors/mastodon-sink-s3-aws/config -d '@./config/mastodon-sink-s3-aws.json'


# DuckDB

duckdb --init duckdb/init.sql

select *  FROM read_parquet('s3://mastodon/topics/mastodon-topic*');

select 'epoch'::TIMESTAMP + INTERVAL 1675325510 seconds;


# AWS
```
aws s3 ls s3://2023mastodon --recursive --human-readable --summarize | tail

aws s3 cp s3://2023mastodon . --recursive --exclude "*" --include "*.parquet"
```

# OLD Notes

- https://martinheinz.dev/blog/86
- https://github.com/morsapaes/hex-data-council/tree/main/data-generator
- https://redpanda.com/blog/kafka-streaming-data-pipeline-from-postgres-to-duckdb


# Docker Notes

```
docker-compose up -d postgres datagen
```

Password `postgres`

```
psql -h localhost -U postgres -d postgres
select * from public.user limit 3;
```

```
docker-compose up -d redpanda redpanda-console connect
```

Redpanda Console at http://localhost:8080

```
docker exec -it connect /bin/bash

curl -X PUT -H  "Content-Type:application/json" localhost:8083/connectors/pg-src/config -d '@/connectors/pg-src.json'

curl -X PUT -H  "Content-Type:application/json" localhost:8083/connectors/s3-sink/config -d '@/connectors/s3-sink.json'


curl -X PUT -H  "Content-Type:application/json" localhost:8083/connectors/s3-sink-m/config -d '@/connectors/s3-sink-m.json'

```



```
docker-compose up -d minio mc
```
http://localhost:9000
```

Login with : `minio / minio123`

```
docker-compose up -d duckdb
```

```
docker-compose exec duckdb bash
duckdb --init duckdb/init.sql

SELECT count(value.after.id) as user_count FROM read_parquet('s3://user-payments/debezium.public.user-*');

```

## Kafka notes

python avro-producer.py -b "localhost:9092" -s "http://localhost:8081" -t aubury.mytopic



## LakeFS

docker run --pull always -p 8000:8000 \
   -e LAKEFS_BLOCKSTORE_TYPE='s3' \
   -e AWS_ACCESS_KEY_ID='YourAccessKeyValue' \
   -e AWS_SECRET_ACCESS_KEY='YourSecretKeyValue' \
   treeverse/lakefs run --local-settings

docker run --pull always -p 8000:8000 \
   -e LAKEFS_BLOCKSTORE_TYPE='s3' \
   -e LAKEFS_BLOCKSTORE_S3_FORCE_PATH_STYLE='true' \
   -e LAKEFS_BLOCKSTORE_S3_ENDPOINT='http://minio:9000' \
   -e LAKEFS_BLOCKSTORE_S3_DISCOVER_BUCKET_REGION='false' \
   -e LAKEFS_BLOCKSTORE_S3_CREDENTIALS_ACCESS_KEY_ID='minio' \
   -e LAKEFS_BLOCKSTORE_S3_CREDENTIALS_SECRET_ACCESS_KEY='minio123' \
   treeverse/lakefs run --local-settings   

set s3_endpoint='minio:9000';
set s3_access_key_id='minio';
set s3_secret_access_key='minio123';
set s3_use_ssl=false;
set s3_region='us-east-1';
set s3_url_style='path';



### Installing packages

Now that you’re in your virtual environment you can install packages.

```console
python -m pip install --requirement requirements.txt
```

### JupyterLab
Once installed, launch JupyterLab with:

```console
jupyter-lab
```

### Cleanup of virtual environment
If you want to switch projects or otherwise leave your virtual environment, simply run:

```console
deactivate
```

If you want to re-enter the virtual environment just follow the same instructions above about activating a virtual environment. There’s no need to re-create the virtual environment.
