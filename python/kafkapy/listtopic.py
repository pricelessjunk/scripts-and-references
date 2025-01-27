from confluent_kafka.admin import AdminClient

conf = {'bootstrap.servers': 'localhost:29092'}
# conf = {'bootstrap.servers': 'b-1.ebdrmskdaac.hiljnf.c8.kafka.eu-central-1.amazonaws.com:9098,b-2.ebdrmskdaac.hiljnf.c8.kafka.eu-central-1.amazonaws.com:9098,b-3.ebdrmskdaac.hiljnf.c8.kafka.eu-central-1.amazonaws.com:9098'}
kadmin = AdminClient(conf)

print(kadmin.list_topics().topics)
