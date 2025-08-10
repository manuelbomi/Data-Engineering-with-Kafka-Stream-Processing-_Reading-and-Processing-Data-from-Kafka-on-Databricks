# Connect to a Kafka topic.
# This segment will start the streaming read operation.
    df = (spark.readStream
      .format("kafka")   # specify Kafka as the data source
      .option("kafka.bootstrap.servers", "<your_kafka_brokers>")
      .option("subscribe", "<your_kafka_topic>")
      .option("startingOffsets", "latest") # Start reading from the latest available offset
      .load())

# Process the Kafka stream.
    from pyspark.sql.functions import from_json, col
    from pyspark.sql.types import StructType, StructField, StringType, IntegerType

    # Define your schema based on the expected JSON data structure. Inferschema # is not used in this instance.
    schema = StructType([
        StructField("id", IntegerType()),
        StructField("name", StringType()),
        StructField("value", IntegerType())
    ])

    # Parse the 'value' column (Kafka message payload) as JSON
    processed_df = df.selectExpr("CAST(value AS STRING) as json_data") \
                     .withColumn("data", from_json(col("json_data"), schema)) \
                     .select("data.*") # Select all fields from the parsed 'data' struct

# Write to Delta Lake.
    query = (processed_df.writeStream
      .format("delta")   #This will specify the Delta Lake as the sink.
      .outputMode("append") # This defines how the new data is written viz: append, complete, update.  
                                                              # Append is used in this instance 
      .option("checkpointLocation", "/path/to/checkpoint/directory") # Essential for fault tolerance. It
                                                           # stores metadata about the streaming session progress
      .toTable("your_delta_table_name"))

    # To start the stream and wait for termination (e.g., in a notebook)
    # query.awaitTermination()
