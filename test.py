#!/usr/bin/env python3
"""
Test script for VPBank Transaction Simulator
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from src.config import config
        print("✅ config module imported successfully")
        
        from src.data_generator import TransactionGenerator
        print("✅ data_generator module imported successfully")
        
        from src.producer import TransactionProducer
        print("✅ producer module imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_transaction_generation():
    """Test transaction generation"""
    print("\n🧪 Testing transaction generation...")
    
    try:
        from src.data_generator import TransactionGenerator
        
        generator = TransactionGenerator()
        
        # Test each transaction type
        ibft = generator.generate_ibft_transaction()
        print(f"✅ IBFT transaction generated: {ibft['transaction_id']}")
        
        qr = generator.generate_qr_payment_transaction()
        print(f"✅ QR payment transaction generated: {qr['transaction_id']}")
        
        topup = generator.generate_topup_wallet_transaction()
        print(f"✅ Wallet topup transaction generated: {topup['transaction_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Transaction generation error: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n🧪 Testing configuration...")
    
    try:
        from src.config import config
        
        print(f"✅ Kafka bootstrap servers: {config.kafka.bootstrap_servers}")
        print(f"✅ Kafka topics: {config.kafka.topics}")
        print(f"✅ Batch size: {config.transaction.batch_size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all tests"""
    print("🏦 === VPBank Transaction Simulator Tests ===")
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed!")
        print("💡 Make sure to install requirements: pip install -r requirements.txt")
        return False
    
    # Test configuration
    if not test_config():
        print("\n❌ Configuration tests failed!")
        return False
    
    # Test transaction generation
    if not test_transaction_generation():
        print("\n❌ Transaction generation tests failed!")
        return False
    
    print("\n✅ All tests passed!")
    print("🚀 You can now run the simulator with: python run.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
