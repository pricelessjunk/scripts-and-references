from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaConsumer


admin_client = KafkaAdminClient(bootstrap_servers=["localhost:9092"])
admin_client.list_topics()

topic_names = ['topic1', 'topic2']

def create_topics(topic_names):

    existing_topic_list = consumer.topics()
    print(list(consumer.topics()))
    topic_list = []
    for topic in topic_names:
        if topic not in existing_topic_list:
            print('Topic : {} added '.format(topic))
            topic_list.append(NewTopic(name=topic, num_partitions=3, replication_factor=3))
        else:
            print('Topic : {topic} already exist ')
    try:
        if topic_list:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print("Topic Created Successfully")
        else:
            print("Topic Exist")
    except TopicAlreadyExistsError as e:
        print("Topic Already Exist")
    except  Exception as e:
        print(e)

'''
def delete_topics(topic_names):
    try:
        admin_client.delete_topics(topics=topic_names)
        print("Topic Deleted Successfully")
    except UnknownTopicOrPartitionError as e:
        print("Topic Doesn't Exist")
    except  Exception as e:
        print(e)
'''

consumer = KafkaConsumer(
        bootstrap_servers = "kcmacbook.local:9092",
    )
# print(consumer.topics())
# create_topics(topic_names)
