# Data Engineering with Kafka Stream Processing: Reading and Processing Data from Kafka on Databricks

### Brief Overview

Databricks leverages Apache Spark Structured Streaming for stream processing, enabling real-time or near real-time analysis of continuously arriving data. The example code below demonstrates how to read a stream of data from Apache Kafka, process it, and then write it to a Delta Lake table.

#### A streaming DataFrame is created by connecting to a Kafka topic. This segment will start the streaming read operation.
---
```ruby
    df = (spark.readStream
      .format("kafka")   # specify Kafka as the data source
      .option("kafka.bootstrap.servers", "<your_kafka_brokers>")
      .option("subscribe", "<your_kafka_topic>")
      .option("startingOffsets", "latest") # Start reading from the latest available offset
      .load())
---




