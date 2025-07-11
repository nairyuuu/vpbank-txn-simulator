"""
Data generator for mock banking transactions
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dataclasses import dataclass
import json
import ipaddress
from faker import Faker
from faker.providers import internet, automotive

@dataclass
class Transaction:
    """Base transaction class with normalized schema fields"""
    transaction_id: str
    timestamp: str
    customer_name: str
    transaction_type: str
    amount: float
    currency: str
    merchant_id: str = None
    sender_account: str = None
    receiver_account: str = None
    wallet_id: str = None
    location_lat: float = None
    location_long: float = None
    ip_address: str = None
    user_agent: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary"""
        return {
            "transaction_id": self.transaction_id,
            "timestamp": self.timestamp,
            "customer_name": self.customer_name,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "currency": self.currency,
            "merchant_id": self.merchant_id,
            "sender_account": self.sender_account,
            "receiver_account": self.receiver_account,
            "wallet_id": self.wallet_id,
            "location_lat": self.location_lat,
            "location_long": self.location_long,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent
        }

class TransactionGenerator:
    """Generates mock banking transactions"""
    
    def __init__(self):
        self.fake = Faker('vi_VN')  # Vietnamese locale
        self.fake.add_provider(internet)
        self.fake.add_provider(automotive)
        
        self.currencies = ["VND", "USD", "EUR"]
        self.banks = ["VPBank", "Vietcombank", "BIDV", "Techcombank", "ACB"]
        self.merchants = [
            "Starbucks Coffee", "Circle K", "Highlands Coffee", "KFC", "McDonald's", 
            "Pizza Hut", "Lotte Mart", "Big C", "Vinmart", "FamilyMart",
            "7-Eleven", "Grab", "Shopee", "Lazada", "Tiki"
        ]
        
        # Generate a fixed pool of 100 users
        self.users = self._generate_user_pool(100)
        
        # Initialize timestamp for sequential generation
        self.current_timestamp = datetime.now() - timedelta(hours=24)
    
    def _generate_user_pool(self, count: int) -> List[Dict[str, str]]:
        """Generate a fixed pool of users with consistent data"""
        users = []
        for _ in range(count):
            user = {
                'name': self.fake.name(),
                'account_number': self.fake.numerify('############'),
                'wallet_id': f"WALLET{random.randint(1000, 9999)}"
            }
            users.append(user)
        return users
    
    def get_random_user(self) -> Dict[str, str]:
        """Get a random user from the pool"""
        return random.choice(self.users)
    
    def generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        return str(uuid.uuid4())
    
    def generate_timestamp(self) -> str:
        """Generate sequential timestamp (chronological order)"""
        # Add random interval between 10 seconds to 5 minutes
        random_interval = random.uniform(10, 300)  # 10 seconds to 5 minutes
        self.current_timestamp += timedelta(seconds=random_interval)
        return self.current_timestamp.isoformat()
    
    def generate_amount(self, min_amount: float = 1000, max_amount: float = 10000000) -> float:
        """Generate random transaction amount"""
        return round(random.uniform(min_amount, max_amount), 2)
    
    def generate_account_number(self) -> str:
        """Generate bank account number"""
        return self.fake.numerify('############')
    
    def generate_location(self) -> tuple:
        """Generate random lat/long in Vietnam"""
        # Rough boundaries for Vietnam
        lat = random.uniform(8.18, 23.39)
        long = random.uniform(102.14, 109.46)
        return (round(lat, 6), round(long, 6))
    
    def generate_ip_address(self) -> str:
        """Generate random IP address"""
        return self.fake.ipv4()
    
    def generate_customer_name(self) -> str:
        """Generate Vietnamese customer name"""
        return self.fake.name()
    
    def generate_user_agent(self) -> str:
        """Generate random user agent"""
        return self.fake.user_agent()
    
    def generate_ibft_transaction(self) -> Dict[str, Any]:
        """Generate Inter-bank Fund Transfer transaction"""
        lat, long = self.generate_location()
        sender_user = self.get_random_user()
        receiver_user = self.get_random_user()
        
        transaction = Transaction(
            transaction_id=self.generate_transaction_id(),
            timestamp=self.generate_timestamp(),
            customer_name=sender_user['name'],
            transaction_type="IBFT",
            amount=self.generate_amount(10000, 50000000),
            currency=random.choice(self.currencies[:1]),
            merchant_id=None,
            sender_account=sender_user['account_number'],
            receiver_account=receiver_user['account_number'],
            wallet_id=None,
            location_lat=lat,
            location_long=long,
            ip_address=self.generate_ip_address(),
            user_agent=self.generate_user_agent()
        )
        
        return transaction.to_dict()
    
    def generate_qr_payment_transaction(self) -> Dict[str, Any]:
        """Generate QR Code Payment transaction"""
        lat, long = self.generate_location()
        user = self.get_random_user()
        
        transaction = Transaction(
            transaction_id=self.generate_transaction_id(),
            timestamp=self.generate_timestamp(),
            customer_name=user['name'],
            transaction_type="QR",
            amount=self.generate_amount(5000, 2000000),
            currency="VND",
            merchant_id=random.choice(self.merchants),
            sender_account=None,
            receiver_account=None,
            wallet_id=None,
            location_lat=lat,
            location_long=long,
            ip_address=self.generate_ip_address(),
            user_agent=self.generate_user_agent()
        )
        
        return transaction.to_dict()
    
    def generate_topup_wallet_transaction(self) -> Dict[str, Any]:
        """Generate Wallet Top-up transaction"""
        lat, long = self.generate_location()
        user = self.get_random_user()
        
        transaction = Transaction(
            transaction_id=self.generate_transaction_id(),
            timestamp=self.generate_timestamp(),
            customer_name=user['name'],
            transaction_type="TOPUP",
            amount=self.generate_amount(50000, 5000000),
            currency="VND",
            merchant_id=None,
            sender_account=None,
            receiver_account=None,
            wallet_id=user['wallet_id'],
            location_lat=lat,
            location_long=long,
            ip_address=self.generate_ip_address(),
            user_agent=self.generate_user_agent()
        )
        
        return transaction.to_dict()
    
    def generate_transactions(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate a batch of mixed transactions"""
        transactions = []
        transaction_types = [
            self.generate_ibft_transaction,
            self.generate_qr_payment_transaction,
            self.generate_topup_wallet_transaction
        ]
        
        for _ in range(count):
            transaction_func = random.choice(transaction_types)
            transaction = transaction_func()
            transactions.append(transaction)
        
        return transactions
