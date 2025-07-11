# TODOs for VPBank Transaction Simulator

## 1. Project Setup
- [ ] Initialize Python project structure
- [ ] Set up virtual environment and install dependencies
- [ ] Configure `.env` for environment variables
- [ ] Prepare `docker-compose.yml` for Kafka and Zookeeper
- [ ] Prepare `workflow.yml` for CI/CD via github actions

## 2. Data Generation
- [ ] Design transaction schema (refer to `source.png`)
- [ ] Implement `data_generator.py` for random transaction creation
- [ ] Support multiple transaction types (`IBFT`, `qr_payments`, `topup_wallet`)
- [ ] Add configurable transaction rates

## 3. Kafka Integration
- [ ] Implement Kafka producer in `producer.py`
- [ ] Configure Kafka topics and connection settings
- [ ] Ensure JSON message formatting

## 4. Simulator Logic
- [ ] Develop main simulation loop in `main.py`
- [ ] Support random timing intervals and simultaneous sends
- [ ] Add logging for sent transactions

## 5. Containerization & Deployment
- [ ] Write Dockerfile for the simulator
- [ ] Update `docker-compose.yml` to include simulator service
- [ ] Test end-to-end with Kafka

## 6. Documentation
- [ ] Complete `README.md` with usage and setup instructions
- [ ] Add code comments and docstrings
- [ ] Update diagrams if needed

## 7. Testing & Validation
- [ ] Write unit tests for data generation and producer logic
- [ ] Validate message formats and Kafka delivery
- [ ] Add sample output data for reference

---
**Assign tasks and track progress in this file.**