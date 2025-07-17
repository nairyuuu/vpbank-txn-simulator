"""
Kafka producer for streaming transaction data
"""

import json
import logging
from typing import Dict, Any, List
from confluent_kafka import Producer
from .config import config

logger = logging.getLogger(__name__)

class TransactionProducer:
    """Kafka producer for transaction messages"""
    
    def __init__(self):
        self.topics = config.kafka.topics
        self.producer_config = {
            'bootstrap.servers': config.kafka.bootstrap_servers,
            'client.id': 'vpbank-transaction-simulator',
            'acks': 'all',
            'retries': 3,
            'retry.backoff.ms': 100,
            'linger.ms': 1,
            'batch.size': 16384,
            'compression.type': 'none',  # Use no compression for simplicity
        }
        self.producer = Producer(self.producer_config)
        logger.info(f"Connected to Kafka at {config.kafka.bootstrap_servers}")
    
    def delivery_report(self, err, msg):
        """Delivery report callback"""
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')
    
    def send_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Send a single transaction to the appropriate topic"""
        try:
            transaction_type = transaction.get('transaction_type')
            logger.info(f"DEBUG: Processing transaction type: '{transaction_type}' (type: {type(transaction_type)})")
            
            # Map transaction types to topics using config
            topic_mapping = {
                'IBFT': 'IBFT',
                'QR': 'qr_payments', 
                'TOPUP': 'topup_wallet'
            }
            
            logger.info(f"DEBUG: Available topic mapping: {topic_mapping}")
            topic = topic_mapping.get(transaction_type)
            logger.info(f"DEBUG: Mapped topic: {topic}")
            
            if not topic:
                logger.error(f"Unknown transaction type: '{transaction_type}' (type: {type(transaction_type)})")
                logger.error(f"Available mapping: {list(topic_mapping.keys())}")
                logger.error(f"Available topics: {self.topics}")
                return False
            
            # Use transaction_id as the key for partitioning
            key = transaction.get('transaction_id', '')
            message = json.dumps(transaction, default=str)
            
            # Send message
            self.producer.produce(
                topic=topic,
                value=message.encode('utf-8'),
                key=key.encode('utf-8'),
                callback=self.delivery_report
            )
            
            # Trigger delivery report callbacks
            self.producer.poll(0)
            
            logger.debug(f"Sent transaction {key} to topic {topic}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending transaction: {e}")
            return False
    
    def send_transactions_batch(self, transactions: List[Dict[str, Any]]) -> int:
        """Send a batch of transactions"""
        successful_sends = 0
        
        for transaction in transactions:
            if self.send_transaction(transaction):
                successful_sends += 1
        
        # Flush to ensure all messages are sent
        self.producer.flush(timeout=10)
        
        logger.info(f"Successfully sent {successful_sends}/{len(transactions)} transactions")
        return successful_sends
    
    def close(self):
        """Close the producer connection"""
        try:
            if self.producer:
                self.producer.flush(timeout=10)
                logger.info("Kafka producer connection closed")
        except Exception as e:
            logger.error(f"Error closing producer: {e}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
