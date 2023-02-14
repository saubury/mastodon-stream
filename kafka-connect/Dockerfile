# FROM confluentinc/cp-server-connect-base:7.3.1
FROM confluentinc/cp-server-connect:7.1.0

RUN   confluent-hub install --no-prompt confluentinc/kafka-connect-s3:10.3.0

# ENTRYPOINT ["tail", "-f", "/dev/null"]
