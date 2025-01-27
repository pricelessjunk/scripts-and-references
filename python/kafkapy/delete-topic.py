from confluent_kafka.admin import AdminClient

conf = {'bootstrap.servers': 'localhost:9092'}
kadmin = AdminClient(conf)

future = kadmin.delete_topics(['first_kafka_topic'])
future['first_kafka_topic'].result()
print('Topic deleted.')
