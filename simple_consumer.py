#!/usr/bin/env python3
"""
Simple Kafka consumer to monitor VPBank transactions in real-time
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import json
import logging
from kafka import KafkaConsumer
from config import config
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simple_consumer(topics=None, duration_seconds=30):
    """
    Simple consumer that listens to all topics and prints transactions
    
    Args:
        topics: List of topics to consume from (default: all VPBank topics)
        duration_seconds: How long to run the consumer
    """
    if topics is None:
        topics = ['IBFT', 'qr_payments', 'topup_wallet']
    
    print(f"🎯 Starting simple consumer for topics: {topics}")
    print(f"⏰ Will run for {duration_seconds} seconds")
    print("=" * 60)
    
    try:
        # Create consumer
        consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',  # Only get new messages
            enable_auto_commit=True,
            group_id='simple_test_consumer',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=1000  # 1 second timeout for checking duration
        )
        
        print("✅ Connected to Kafka")
        print("🔍 Listening for transactions...")
        print()
        
        start_time = datetime.now()
        message_count = 0
        topic_counts = {topic: 0 for topic in topics}
        
        while True:
            # Check if we've exceeded the duration
            if (datetime.now() - start_time).seconds >= duration_seconds:
                break
            
            # Poll for messages
            message_batch = consumer.poll(timeout_ms=1000)
            
            for topic_partition, messages in message_batch.items():
                topic_name = topic_partition.topic
                
                for message in messages:
                    try:
                        transaction = message.value
                        message_count += 1
                        topic_counts[topic_name] += 1
                        
                        # Print transaction summary
                        print(f"📨 [{topic_name}] Transaction #{message_count}")
                        print(f"   ID: {transaction.get('transaction_id', 'N/A')}")
                        print(f"   Type: {transaction.get('transaction_type', 'N/A')}")
                        print(f"   Amount: {transaction.get('amount', 'N/A')} {transaction.get('currency', 'VND')}")
                        
                        # Type-specific details
                        if topic_name == 'IBFT':
                            print(f"   From: {transaction.get('from_account', 'N/A')}")
                            print(f"   To: {transaction.get('to_account', 'N/A')}")
                        elif topic_name == 'qr_payments':
                            print(f"   Merchant: {transaction.get('merchant_name', 'N/A')}")
                        elif topic_name == 'topup_wallet':
                            print(f"   Wallet: {transaction.get('wallet_id', 'N/A')}")
                        
                        print(f"   Time: {transaction.get('timestamp', 'N/A')}")
                        print()
                        
                    except Exception as e:
                        print(f"❌ Error processing message: {e}")
        
        consumer.close()
        
        # Print summary
        print("📊 SUMMARY")
        print("=" * 30)
        print(f"Total messages: {message_count}")
        for topic, count in topic_counts.items():
            print(f"{topic}: {count}")
        print(f"Duration: {(datetime.now() - start_time).seconds} seconds")
        
        return message_count
        
    except Exception as e:
        logger.error(f"❌ Consumer error: {e}")
        return 0

def monitor_topic(topic_name, count=10):
    """Monitor a specific topic for a number of messages"""
    print(f"🎯 Monitoring topic: {topic_name}")
    print(f"📊 Will capture {count} messages")
    print("=" * 40)
    
    try:
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id=f'monitor_{topic_name}',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=30000  # 30 second timeout
        )
        
        print(f"✅ Connected to {topic_name}")
        print("🔍 Waiting for messages...")
        print()
        
        messages_received = 0
        for message in consumer:
            try:
                transaction = message.value
                messages_received += 1
                
                print(f"📨 Message {messages_received}/{count}")
                print(f"   Transaction: {transaction.get('transaction_id', 'N/A')}")
                print(f"   Type: {transaction.get('transaction_type', 'N/A')}")
                print(f"   Amount: {transaction.get('amount', 'N/A')} {transaction.get('currency', 'VND')}")
                print(f"   Partition: {message.partition}, Offset: {message.offset}")
                print()
                
                if messages_received >= count:
                    break
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        consumer.close()
        print(f"✅ Captured {messages_received} messages from {topic_name}")
        return messages_received
        
    except Exception as e:
        logger.error(f"❌ Monitor error: {e}")
        return 0

def main():
    """Main function with simple menu"""
    print("VPBank Transaction Consumer")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Monitor all topics for 30 seconds")
        print("2. Monitor IBFT topic (10 messages)")
        print("3. Monitor QR payments topic (10 messages)")
        print("4. Monitor Topup wallet topic (10 messages)")
        print("5. Custom monitoring")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            simple_consumer(duration_seconds=30)
        elif choice == '2':
            monitor_topic('IBFT', 10)
        elif choice == '3':
            monitor_topic('qr_payments', 10)
        elif choice == '4':
            monitor_topic('topup_wallet', 10)
        elif choice == '5':
            try:
                topic = input("Enter topic name (IBFT/qr_payments/topup_wallet): ").strip()
                count = int(input("Enter number of messages to capture: ").strip())
                monitor_topic(topic, count)
            except ValueError:
                print("❌ Invalid input")
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Consumer stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
