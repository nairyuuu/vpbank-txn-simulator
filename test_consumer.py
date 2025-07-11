#!/usr/bin/env python3
"""
Simple test consumer to verify Kafka messages are being produced correctly
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import json
import logging
from kafka import KafkaConsumer
from config import config

# Enable debug logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestConsumer:
    def __init__(self):
        """Initialize the test consumer"""
        self.consumers = {}
        self.topics = ['IBFT', 'qr_payments', 'topup_wallet']
        
    def create_consumers(self):
        """Create consumers for each topic"""
        try:
            for topic in self.topics:
                consumer = KafkaConsumer(
                    topic,
                    bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
                    auto_offset_reset='latest',  # Start from latest messages
                    enable_auto_commit=True,
                    group_id=f'test_consumer_{topic}',
                    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                    consumer_timeout_ms=5000  # 5 second timeout
                )
                self.consumers[topic] = consumer
                logger.info(f"✅ Created consumer for topic: {topic}")
        except Exception as e:
            logger.error(f"❌ Failed to create consumers: {e}")
            raise
    
    def consume_messages(self, max_messages=10):
        """Consume messages from all topics"""
        logger.info(f"🔍 Starting to consume messages (max {max_messages} per topic)...")
        
        message_counts = {topic: 0 for topic in self.topics}
        
        try:
            for topic, consumer in self.consumers.items():
                logger.info(f"\n📡 Consuming from topic: {topic}")
                logger.info("-" * 40)
                
                for message in consumer:
                    try:
                        # Parse the message
                        transaction = message.value
                        
                        # Display message info
                        logger.info(f"📨 Message {message_counts[topic] + 1}:")
                        logger.info(f"   Topic: {message.topic}")
                        logger.info(f"   Partition: {message.partition}")
                        logger.info(f"   Offset: {message.offset}")
                        logger.info(f"   Transaction ID: {transaction.get('transaction_id', 'N/A')}")
                        logger.info(f"   Transaction Type: {transaction.get('transaction_type', 'N/A')}")
                        logger.info(f"   Amount: {transaction.get('amount', 'N/A')}")
                        logger.info(f"   Currency: {transaction.get('currency', 'N/A')}")
                        logger.info(f"   Timestamp: {transaction.get('timestamp', 'N/A')}")
                        
                        # Show transaction-specific fields
                        if transaction.get('transaction_type') == 'IBFT':
                            logger.info(f"   From Account: {transaction.get('from_account', 'N/A')}")
                            logger.info(f"   To Account: {transaction.get('to_account', 'N/A')}")
                        elif transaction.get('transaction_type') == 'QR':
                            logger.info(f"   Merchant: {transaction.get('merchant_name', 'N/A')}")
                            logger.info(f"   QR Code: {transaction.get('qr_code', 'N/A')}")
                        elif transaction.get('transaction_type') == 'TOPUP':
                            logger.info(f"   Wallet ID: {transaction.get('wallet_id', 'N/A')}")
                            logger.info(f"   Source: {transaction.get('source_account', 'N/A')}")
                        
                        logger.info("")
                        
                        message_counts[topic] += 1
                        
                        # Stop after max messages for this topic
                        if message_counts[topic] >= max_messages:
                            break
                            
                    except Exception as e:
                        logger.error(f"❌ Error processing message: {e}")
                        continue
                
                if message_counts[topic] == 0:
                    logger.info(f"⏰ No messages received for topic {topic} within timeout period")
        
        except Exception as e:
            logger.error(f"❌ Error consuming messages: {e}")
        
        # Summary
        logger.info("\n📊 CONSUMPTION SUMMARY")
        logger.info("=" * 40)
        total_messages = 0
        for topic, count in message_counts.items():
            logger.info(f"{topic}: {count} messages")
            total_messages += count
        logger.info(f"Total: {total_messages} messages")
        
        return message_counts
    
    def close(self):
        """Close all consumers"""
        for topic, consumer in self.consumers.items():
            try:
                consumer.close()
                logger.info(f"✅ Closed consumer for topic: {topic}")
            except Exception as e:
                logger.error(f"❌ Error closing consumer for {topic}: {e}")

def test_single_topic_consumer(topic_name, max_messages=5):
    """Test consuming from a single topic"""
    logger.info(f"\n🎯 Testing single topic consumer for: {topic_name}")
    logger.info("=" * 50)
    
    try:
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id=f'single_test_consumer_{topic_name}',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=10000  # 10 second timeout
        )
        
        logger.info(f"✅ Connected to topic: {topic_name}")
        logger.info("🔍 Waiting for messages...")
        
        message_count = 0
        for message in consumer:
            try:
                transaction = message.value
                logger.info(f"📨 Message {message_count + 1}: {transaction.get('transaction_id', 'N/A')}")
                logger.info(f"   Type: {transaction.get('transaction_type', 'N/A')}")
                logger.info(f"   Amount: {transaction.get('amount', 'N/A')} {transaction.get('currency', 'N/A')}")
                
                message_count += 1
                if message_count >= max_messages:
                    break
                    
            except Exception as e:
                logger.error(f"❌ Error processing message: {e}")
                continue
        
        consumer.close()
        logger.info(f"✅ Consumed {message_count} messages from {topic_name}")
        return message_count
        
    except Exception as e:
        logger.error(f"❌ Error with single topic consumer: {e}")
        return 0

def main():
    """Main test function"""
    print("VPBank Transaction Consumer Test")
    print("=" * 50)
    
    try:
        # Test 1: Create and test multi-topic consumer
        logger.info("🚀 Starting multi-topic consumer test...")
        test_consumer = TestConsumer()
        test_consumer.create_consumers()
        message_counts = test_consumer.consume_messages(max_messages=5)
        test_consumer.close()
        
        # Test 2: Test individual topics if no messages were received
        if sum(message_counts.values()) == 0:
            logger.info("\n🔄 No messages found, testing individual topics...")
            for topic in ['IBFT', 'qr_payments', 'topup_wallet']:
                test_single_topic_consumer(topic, max_messages=3)
        
        logger.info("\n✅ Consumer test completed!")
        
    except Exception as e:
        logger.error(f"❌ Consumer test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
