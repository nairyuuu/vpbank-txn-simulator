#!/bin/bash

# Start Kafka in KRaft mode
# This script initializes and starts Kafka without Zookeeper

KAFKA_HOME=/opt/kafka
CONFIG_FILE=$KAFKA_HOME/config/kraft/server.properties
LOG_DIR=/tmp/kraft-combined-logs

echo "Starting Kafka in KRaft mode..."

# Generate a cluster UUID
KAFKA_CLUSTER_ID=$(kafka-storage.sh random-uuid)
echo "Generated Cluster ID: $KAFKA_CLUSTER_ID"

# Format the storage directory
echo "Formatting storage directory..."
kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c $CONFIG_FILE

# Start Kafka server
echo "Starting Kafka server..."
kafka-server-start.sh $CONFIG_FILE

echo "Kafka started successfully in KRaft mode!"
echo "Bootstrap server: localhost:9092"
echo "Controller: localhost:9093"
