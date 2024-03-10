package kafka

import org.apache.kafka.clients.admin.Admin
import org.apache.kafka.clients.admin.AdminClientConfig
import org.apache.kafka.clients.admin.CreateTopicsResult
import org.apache.kafka.clients.admin.NewTopic
import org.apache.kafka.clients.producer.KafkaProducer
import org.apache.kafka.clients.producer.ProducerConfig
import org.apache.kafka.clients.producer.ProducerRecord
import org.apache.kafka.common.serialization.Serdes
import org.apache.kafka.common.serialization.StringSerializer
import org.apache.kafka.streams.KafkaStreams
import org.apache.kafka.streams.StreamsBuilder
import org.apache.kafka.streams.StreamsConfig
import org.apache.kafka.streams.StreamsConfig.RACK_AWARE_ASSIGNMENT_STRATEGY_NONE
import org.apache.kafka.streams.kstream.Consumed
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.slf4j.LoggerFactory
import org.testcontainers.containers.KafkaContainer
import org.testcontainers.containers.Network
import org.testcontainers.containers.output.OutputFrame
import org.testcontainers.containers.output.WaitingConsumer
import org.testcontainers.junit.jupiter.Container
import org.testcontainers.junit.jupiter.Testcontainers
import org.testcontainers.utility.DockerImageName
import java.util.Properties
import java.util.concurrent.TimeUnit


@Testcontainers
class RackIdFailureTest {
    private val logger = LoggerFactory.getLogger(javaClass)

    companion object {
        private val kafkaImage = DockerImageName.parse("confluentinc/cp-kafka:7.4.0")
        private const val sourceTopicName = "topic-source"
        private const val destTopicName = "topic-dest"
        private const val destKTableName = "dest-ktable"
    }

    private val network: Network = Network.newNetwork()

    @Container
    val kafkaContainer: KafkaContainer = KafkaContainer(kafkaImage)
        .withEnv(
            mapOf(
                "KAFKA_AUTO_CREATE_TOPICS_ENABLE" to "true",
                "KAFKA_GROUP_MAX_SESSION_TIMEOUT_MS" to "1000000",
                "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR" to "1"
            )
        )
        .withNetwork(network)

    @BeforeEach
    fun init(){
        logger.info("Bootstraps: ${kafkaContainer.bootstrapServers}")

        createTopic()
        produceMessages()
    }

    @Test
    fun rackIdTest(){
        val builder = StreamsBuilder()
        builder.stream(sourceTopicName, Consumed.with(Serdes.String(), Serdes.String()))
            .peek { k, v -> logger.info(".........Key: $k, Value: $v") }
            //.toTable(Named.`as`(destKTableName))
            .to(destTopicName)
        val topology = builder.build()

        logger.info(topology.describe().toString())

        val streamsConfiguration = Properties()
        streamsConfiguration[StreamsConfig.APPLICATION_ID_CONFIG] = "rackIdTest"
        streamsConfiguration[StreamsConfig.BOOTSTRAP_SERVERS_CONFIG] = kafkaContainer.bootstrapServers
        // streamsConfiguration[StreamsConfig.RACK_AWARE_ASSIGNMENT_STRATEGY_CONFIG] = RACK_AWARE_ASSIGNMENT_STRATEGY_NONE

        val streams= KafkaStreams(topology, streamsConfiguration)
        streams.start()

        Thread.sleep(2000)
        streams.close()

        val logsConsumer = WaitingConsumer()
        kafkaContainer.followOutput(logsConsumer, OutputFrame.OutputType.STDOUT)

        logsConsumer.waitUntil(
            { frame -> frame.utf8String.contains(Regex("rackId")) },
            10,
            TimeUnit.SECONDS
        )
    }

    private fun createTopic() {
        val properties = Properties()
        properties[AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG] = kafkaContainer.bootstrapServers

        Admin.create(properties).use { admin ->
            val partitions = 1
            val replicationFactor: Short = 1
            val newSourceTopic = NewTopic(sourceTopicName, partitions, replicationFactor)
            val newDestTopic = NewTopic(destTopicName, partitions, replicationFactor)

            val result: CreateTopicsResult = admin.createTopics(
                setOf(newSourceTopic, newDestTopic)
            )

            val future = result.values()[sourceTopicName]!!
            future.get()
        }
    }

    private fun produceMessages() {
        val properties =  Properties()
        properties.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaContainer.bootstrapServers)
        properties.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer().javaClass.name)
        properties.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer().javaClass.name)

        val producer: KafkaProducer<String, String> = KafkaProducer(properties)
        for (i in 0..4) {
            val producerRecord = ProducerRecord(sourceTopicName, "key-$i", "value-$i")
            producer.send(producerRecord)
        }
    }
}
