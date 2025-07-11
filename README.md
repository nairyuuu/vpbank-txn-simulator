# VPBank Transaction Simulator

A mock transaction data generator for Hackathon 2025.
Assigned to: nairyuuu (Lê Trần Long)

## Overview

This project simulates banking transactions and streams them to Kafka topics for real-time processing and analysis.

## Requirements

### Input
- No input required (uses random seed or streams from existing data files)

### Output
- 3 Kafka topics for different transaction types:
  - `IBFT` - Inter-bank Fund Transfer
  - `qr_payments` - QR Code Payments  
  - `topup_wallet` - Wallet Top-up
- Messages sent in JSON format
- Random timing intervals (transactions can be sent simultaneously)

### Transaction Attributes
![Transaction Attributes](source.png)

## Project Structure

```
mock-txn-data/
├── docker-compose.yml
├── kafka/
│   └── config/
│       └── server.properties
├── scripts/
│   ├── start-kraft.sh
│   └── start-kraft.bat
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── producer.py
│   ├── data_generator.py
│   └── config.py
├── requirements.txt
├── README.md
├── source.png
└── .env
```

## Getting Started

### Quick Start with Docker (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd vpbank-txn-simulator

# Start the entire stack
docker-compose up -d

# View logs
docker-compose logs -f txn-simulator

# Stop the stack
docker-compose down
```

### Manual Setup (Development)
1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables in `.env`
3. Start Kafka: `docker-compose up -d kafka kafka-ui`
4. Run the simulator: `python -m src.main`

### Services
- **Kafka**: `localhost:9092` (KRaft mode)
- **Kafka UI**: `http://localhost:8080`
- **Transaction Simulator**: Runs automatically in Docker

### Monitoring
- **Kafka Topics**: IBFT, qr_payments, topup_wallet
- **Kafka UI**: Monitor topics, messages, and consumer groups
- **Logs**: `docker-compose logs -f txn-simulator`

## Features

- Random transaction generation
- Configurable transaction rates
- Multiple transaction types
- Real-time Kafka streaming
- Docker containerization