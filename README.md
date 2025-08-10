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
```
---

#### Processing the Kafka Stream. The raw Kafka messages (often in binary format) are typically parsed and transformed. For instance, if the messages are JSON strings, they can be parsed into a structured schema.
---
```ruby
    from pyspark.sql.functions import from_json, col
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType

    # Define your schema based on the expected JSON data structure. Inferschema is not used in this instance.
    schema = StructType([
        StructField("id", IntegerType()),
        StructField("name", StringType()),
        StructField("value", IntegerType())
    ])
```
---

#### Parse the 'value' column (Kafka message payload) in the desired format. We have chosen JSON as the format in this instance.
---
```ruby
    processed_df = df.selectExpr("CAST(value AS STRING) as json_data") \
                     .withColumn("data", from_json(col("json_data"), schema)) \
                     .select("data.*") # Select all fields from the parsed 'data' struct
```
---

#### Write to the Delta Lake. Delta Lake, available on Databricks, provides ACID properties and supports continuous data ingestion.
---
```ruby
    query = (processed_df.writeStream
      .format("delta")   #This will specify the Delta Lake as the sink.
      .outputMode("append") # This defines how the new data is written viz: append, complete, update.  
                                                              # Append is used in this instance 
      .option("checkpointLocation", "/path/to/checkpoint/directory") # Essential for fault tolerance. It
                                                           # stores metadata about the streaming session progress
      .toTable("your_delta_table_name"))

    # To start the stream and wait for termination (e.g., in a notebook)
    # query.awaitTermination()

```
---

Author's Background

```
> [!NOTE]
Author's Name:  Emmanuel Oyekanlu
Skillset:   I have experience spanning several years in developing scalable enterprise data pipelines,
solution architecture, architecting enterprise data and AI solutions, deep learning and LLM applications as
well as deploying solutions (apps) on-prem and in the cloud.

I can be reached through: manuelbomi@yahoo.com
Website:  http://emmanueloyekanlu.com/
Publications:  https://scholar.google.com/citations?user=S-jTMfkAAAAJ&hl=en
LinkedIn:  https://www.linkedin.com/in/emmanuel-oyekanlu-6ba98616
Github:  https://github.com/manuelbomi

```

[![Icons](https://skillicons.dev/icons?i=aws,azure,gcp,scala,mongodb,redis,cassandra,kafka,anaconda,matlab,nodejs,django,py,c,anaconda,git,github,mysql,docker,kubernetes&theme=dark)](https://skillicons.dev)







