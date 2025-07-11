#!/usr/bin/env python3
"""
Simple test to debug the producer topic mapping issue
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_generator import TransactionGenerator
from config import config

def test_producer_logic():
    """Test the actual producer logic without Kafka connection"""
    
    print("=== Testing Producer Topic Mapping Logic ===")
    
    # Mock the producer logic
    def mock_send_transaction(transaction):
        transaction_type = transaction.get('transaction_type')
        print(f"Processing transaction type: '{transaction_type}' (type: {type(transaction_type)})")
        
        # Use the same mapping as the producer
        topic_mapping = {
            'IBFT': 'IBFT',
            'QR': 'qr_payments', 
            'TOPUP': 'topup_wallet'
        }
        
        topic = topic_mapping.get(transaction_type)
        
        if not topic:
            print(f"❌ Unknown transaction type: '{transaction_type}' (type: {type(transaction_type)})")
            print(f"Available mapping: {list(topic_mapping.keys())}")
            return False
        else:
            print(f"✅ Transaction type '{transaction_type}' mapped to topic: {topic}")
            return True
    
    # Generate some transactions and test them
    generator = TransactionGenerator()
    
    # Test individual transaction types
    print("\n--- Testing Individual Transaction Types ---")
    ibft_txn = generator.generate_ibft_transaction()
    qr_txn = generator.generate_qr_payment_transaction()
    topup_txn = generator.generate_topup_wallet_transaction()
    
    transactions = [ibft_txn, qr_txn, topup_txn]
    
    for i, txn in enumerate(transactions, 1):
        print(f"\nTransaction {i}:")
        print(f"  ID: {txn['transaction_id']}")
        print(f"  Type: '{txn['transaction_type']}'")
        print(f"  Type repr: {repr(txn['transaction_type'])}")
        success = mock_send_transaction(txn)
        print(f"  Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    # Test batch generation
    print("\n--- Testing Batch Generation ---")
    batch_txns = generator.generate_transactions(10)
    
    success_count = 0
    for txn in batch_txns:
        if mock_send_transaction(txn):
            success_count += 1
    
    print(f"\nBatch Result: {success_count}/{len(batch_txns)} transactions successfully mapped")
    
    return success_count == len(batch_txns)

if __name__ == "__main__":
    print("VPBank Transaction Simulator - Producer Logic Test")
    print("=" * 60)
    
    try:
        success = test_producer_logic()
        print(f"\n{'✅ All tests passed!' if success else '❌ Some tests failed!'}")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
