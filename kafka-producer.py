import json
from confluent_kafka import Producer, KafkaException
from confluent_kafka.avro import AvroProducer
from confluent_kafka import avro


def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % msg.value().decode('utf-8'), str(err))
    else:
        print("Message produced: %s" % msg.value().decode('utf-8'))


def send_data():
    producer_config = {
        "bootstrap.servers": "localhost:9092",
        "schema.registry.url": "http://localhost:8081"
    }

    value_schema = avro.load("avro/mastodon-topic-value.avsc")

    try:
        producer = AvroProducer(producer_config, default_value_schema=value_schema)

        value_dict = {  "language": "en", "favourites": 0, "username": "bob", "bot": False, "tags": 0, "characters": 50, "words": 12}

        producer.produce(topic = "mastodon-topic", value = value_dict)
        producer.flush()

    except KafkaException as e:
        print('Kafka failure ' + e)



def main():
    send_data()


if __name__ == "__main__":
    main()
