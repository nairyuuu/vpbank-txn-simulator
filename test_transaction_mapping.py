#!/usr/bin/env python3
"""
Test script to verify transaction type mapping between generator and producer
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import TransactionGenerator
from config import config
import json

def test_transaction_generation():
    """Test that transaction generation produces expected types"""
    print("Testing transaction generation...")
    
    generator = TransactionGenerator()
    
    # Test individual transaction types
    print("\n=== Testing Individual Transaction Types ===")
    
    # IBFT
    ibft_txn = generator.generate_ibft_transaction()
    print(f"IBFT Transaction Type: '{ibft_txn['transaction_type']}' (type: {type(ibft_txn['transaction_type'])})")
    
    # QR
    qr_txn = generator.generate_qr_payment_transaction()
    print(f"QR Transaction Type: '{qr_txn['transaction_type']}' (type: {type(qr_txn['transaction_type'])})")
    
    # TOPUP
    topup_txn = generator.generate_topup_wallet_transaction()
    print(f"TOPUP Transaction Type: '{topup_txn['transaction_type']}' (type: {type(topup_txn['transaction_type'])})")
    
    # Test batch generation
    print("\n=== Testing Batch Generation ===")
    transactions = generator.generate_transactions(10)
    type_counts = {}
    
    for txn in transactions:
        txn_type = txn.get('transaction_type')
        print(f"Transaction {txn['transaction_id']}: type='{txn_type}' (type: {type(txn_type)})")
        type_counts[txn_type] = type_counts.get(txn_type, 0) + 1
    
    print(f"\nTransaction type distribution: {type_counts}")
    
    return transactions

def test_producer_mapping():
    """Test producer topic mapping"""
    print("\n=== Testing Producer Topic Mapping ===")
    
    print(f"Configured topics: {config.kafka.topics}")
    
    # Create a mock producer instance to test mapping
    class MockProducer:
        def __init__(self):
            self.topics = config.kafka.topics
            
        def test_mapping(self, transaction_type):
            topic_mapping = {
                'IBFT': 'IBFT',
                'QR': 'qr_payments', 
                'TOPUP': 'topup_wallet'
            }
            return topic_mapping.get(transaction_type)
    
    mock_producer = MockProducer()
    
    test_types = ['IBFT', 'QR', 'TOPUP', 'UNKNOWN']
    for txn_type in test_types:
        topic = mock_producer.test_mapping(txn_type)
        print(f"Transaction type '{txn_type}' maps to topic: {topic}")
    
    return mock_producer

def test_end_to_end():
    """Test end-to-end transaction generation and topic mapping"""
    print("\n=== Testing End-to-End Mapping ===")
    
    generator = TransactionGenerator()
    mock_producer = test_producer_mapping()
    
    # Generate some transactions
    transactions = generator.generate_transactions(5)
    
    for txn in transactions:
        txn_type = txn.get('transaction_type')
        expected_topic = mock_producer.test_mapping(txn_type)
        
        print(f"Transaction {txn['transaction_id']}:")
        print(f"  Type: '{txn_type}' (len: {len(txn_type) if txn_type else 'None'})")
        print(f"  Expected topic: {expected_topic}")
        print(f"  Type repr: {repr(txn_type)}")
        print(f"  Type bytes: {txn_type.encode('utf-8') if txn_type else 'None'}")
        print()

if __name__ == "__main__":
    print("VPBank Transaction Simulator - Transaction Type Mapping Test")
    print("=" * 60)
    
    try:
        # Test transaction generation
        transactions = test_transaction_generation()
        
        # Test producer mapping
        test_producer_mapping()
        
        # Test end-to-end
        test_end_to_end()
        
        print("\n" + "=" * 60)
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
