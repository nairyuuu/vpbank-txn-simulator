"""
Configuration settings for the VPBank Transaction Simulator
"""

import os
from dataclasses import dataclass
from typing import List

@dataclass
class KafkaConfig:
    """Kafka configuration settings"""
    bootstrap_servers: str = "localhost:9092"
    topics: List[str] = None
    
    def __post_init__(self):
        if self.topics is None:
            self.topics = ["IBFT", "qr_payments", "topup_wallet"]

@dataclass
class TransactionConfig:
    """Transaction generation configuration"""
    min_interval: float = 0.1  # Minimum seconds between transactions
    max_interval: float = 5.0  # Maximum seconds between transactions
    batch_size: int = 100      # Number of transactions to generate per batch
    
@dataclass
class AppConfig:
    """Application configuration"""
    kafka: KafkaConfig
    transaction: TransactionConfig
    
    @classmethod
    def from_env(cls):
        """Load configuration from environment variables"""
        kafka_config = KafkaConfig(
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        )
        
        transaction_config = TransactionConfig(
            min_interval=float(os.getenv("MIN_INTERVAL", "0.1")),
            max_interval=float(os.getenv("MAX_INTERVAL", "5.0")),
            batch_size=int(os.getenv("BATCH_SIZE", "100"))
        )
        
        return cls(kafka=kafka_config, transaction=transaction_config)

# Global configuration instance
config = AppConfig.from_env()
