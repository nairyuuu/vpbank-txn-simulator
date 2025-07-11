"""
Main entry point for the VPBank Transaction Simulator
"""

import logging
import time
import random
import signal
import sys
from typing import NoReturn
from .config import config
from .data_generator import TransactionGenerator
from .producer import TransactionProducer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TransactionSimulator:
    """Main simulator class"""
    
    def __init__(self):
        self.generator = TransactionGenerator()
        self.producer = TransactionProducer()
        self.running = False
        
    def start(self):
        """Start the transaction simulation"""
        logger.info("Starting VPBank Transaction Simulator...")
        logger.info(f"Kafka Topics: {config.kafka.topics}")
        logger.info(f"Transaction interval: {config.transaction.min_interval}s - {config.transaction.max_interval}s")
        logger.info(f"Batch size: {config.transaction.batch_size}")
        
        self.running = True
        
        try:
            while self.running:
                # Generate batch of transactions
                transactions = self.generator.generate_transactions(config.transaction.batch_size)
                
                # Debug: Check the first few transactions
                logger.info(f"DEBUG: Generated {len(transactions)} transactions")
                for i, txn in enumerate(transactions[:3]):  # Show first 3 transactions
                    logger.info(f"DEBUG: Transaction {i+1}: type='{txn['transaction_type']}', id={txn['transaction_id']}")
                
                # Send transactions to Kafka
                successful_sends = self.producer.send_transactions_batch(transactions)
                
                logger.info(f"Generated and sent {successful_sends} transactions")
                
                # Wait for random interval before next batch
                interval = random.uniform(
                    config.transaction.min_interval,
                    config.transaction.max_interval
                )
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Received interrupt signal, shutting down...")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the simulation"""
        logger.info("Stopping transaction simulator...")
        self.running = False
        self.producer.close()
        logger.info("Transaction simulator stopped")

def signal_handler(signum, frame):
    """Handle interrupt signals"""
    logger.info("Received signal to terminate")
    sys.exit(0)

def main():
    """Main function"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start simulator
    simulator = TransactionSimulator()
    simulator.start()

if __name__ == "__main__":
    main()
