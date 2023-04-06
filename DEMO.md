
```console
source env/bin/activate

colima start --memory 12

docker-compose -f docker-compose-demo.yml up -d
```

Create access keys at http://localhost:9001/access-keys


```console
export AWS_ACCESS_KEY_ID=keyid
export AWS_SECRET_ACCESS_KEY=keysecret

aws --endpoint-url http://localhost:9000 s3 cp data_tmp/all_toots.parquet s3://mastodon
```



