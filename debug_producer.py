#!/usr/bin/env python3
"""
Debug script to test the producer with actual Kafka connection
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import TransactionGenerator
from config import config
import json
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_producer_with_kafka():
    """Debug the producer with actual Kafka connection"""
    
    # Import the producer here to avoid issues if Kafka is not available
    try:
        from producer import TransactionProducer
    except ImportError as e:
        logger.error(f"Failed to import TransactionProducer: {e}")
        return False
    
    try:
        # Create producer and generator
        producer = TransactionProducer()
        generator = TransactionGenerator()
        
        # Generate a small batch of transactions
        transactions = generator.generate_transactions(5)
        
        logger.info(f"Generated {len(transactions)} transactions")
        
        # Send each transaction individually to see detailed debugging
        for i, txn in enumerate(transactions, 1):
            logger.info(f"\n--- Processing Transaction {i} ---")
            logger.info(f"Transaction ID: {txn['transaction_id']}")
            logger.info(f"Transaction Type: '{txn['transaction_type']}'")
            logger.info(f"Transaction Type repr: {repr(txn['transaction_type'])}")
            logger.info(f"Transaction Type bytes: {txn['transaction_type'].encode('utf-8')}")
            
            # Try to send the transaction
            success = producer.send_transaction(txn)
            logger.info(f"Send result: {'✅ SUCCESS' if success else '❌ FAILED'}")
            
            # Add a small delay between transactions
            import time
            time.sleep(0.1)
        
        producer.close()
        return True
        
    except Exception as e:
        logger.error(f"Error in debug_producer_with_kafka: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Debug Producer with Kafka Connection")
    print("=" * 50)
    
    try:
        success = debug_producer_with_kafka()
        print(f"\n{'✅ Debug completed successfully!' if success else '❌ Debug failed!'}")
    except Exception as e:
        print(f"❌ Debug failed with error: {e}")
        import traceback
        traceback.print_exc()
