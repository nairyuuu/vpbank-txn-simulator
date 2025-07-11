#!/bin/bash

# Development helper script for VPBank Transaction Simulator

set -e

COMPOSE_FILE="docker-compose.yml"

function usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start        Start all services"
    echo "  stop         Stop all services"
    echo "  restart      Restart all services"
    echo "  logs         Show logs for all services"
    echo "  logs-sim     Show logs for transaction simulator only"
    echo "  logs-kafka   Show logs for Kafka only"
    echo "  build        Build the transaction simulator image"
    echo "  topics       List Kafka topics"
    echo "  consume      Start console consumer for all topics"
    echo "  status       Show service status"
    echo "  clean        Stop and remove all containers and volumes"
    echo "  troubleshoot Troubleshoot common issues"
    echo ""
}

function start_services() {
    echo "Starting VPBank Transaction Simulator..."
    docker-compose up -d
    echo "Services started successfully!"
    echo "Kafka UI: http://localhost:8080"
}

function stop_services() {
    echo "Stopping services..."
    docker-compose down
    echo "Services stopped."
}

function restart_services() {
    echo "Restarting services..."
    docker-compose down
    docker-compose up -d
    echo "Services restarted successfully!"
}

function show_logs() {
    docker-compose logs -f
}

function show_simulator_logs() {
    docker-compose logs -f txn-simulator
}

function show_kafka_logs() {
    docker-compose logs -f kafka
}

function build_image() {
    echo "Building transaction simulator image..."
    docker-compose build txn-simulator
    echo "Image built successfully!"
}

function list_topics() {
    echo "Kafka topics:"
    docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list
}

function consume_messages() {
    echo "Starting console consumer (Ctrl+C to exit)..."
    echo "Choose a topic:"
    echo "1. IBFT"
    echo "2. qr_payments"
    echo "3. topup_wallet"
    read -p "Enter choice (1-3): " choice
    
    case $choice in
        1) topic="IBFT" ;;
        2) topic="qr_payments" ;;
        3) topic="topup_wallet" ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac
    
    docker exec -it kafka kafka-console-consumer.sh \
        --bootstrap-server localhost:9092 \
        --topic $topic \
        --from-beginning \
        --property print.timestamp=true
}

function show_status() {
    echo "Service Status:"
    docker-compose ps
}

function clean_all() {
    echo "Cleaning up all containers and volumes..."
    docker-compose down -v
    docker system prune -f
    echo "Cleanup completed."
}

function troubleshoot() {
    echo "=== VPBank Transaction Simulator Troubleshooting ==="
    echo ""
    echo "1. Service Status:"
    docker-compose ps
    echo ""
    echo "2. Kafka Health Check:"
    docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list 2>/dev/null && echo "✓ Kafka is healthy" || echo "✗ Kafka is not responding"
    echo ""
    echo "3. Available Topics:"
    docker exec kafka kafka-topics.sh --bootstrap-server localhost:9092 --list 2>/dev/null || echo "✗ Cannot list topics"
    echo ""
    echo "4. Kafka Logs (last 20 lines):"
    docker-compose logs --tail=20 kafka
    echo ""
    echo "5. Simulator Logs (last 20 lines):"
    docker-compose logs --tail=20 txn-simulator
    echo ""
    echo "Common Solutions:"
    echo "  - If Kafka won't start: ./dev.sh clean && ./dev.sh start"
    echo "  - If simulator can't connect: Check Kafka is running first"
    echo "  - If topics missing: ./dev.sh restart"
}

# Main script logic
case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    logs-sim)
        show_simulator_logs
        ;;
    logs-kafka)
        show_kafka_logs
        ;;
    build)
        build_image
        ;;
    topics)
        list_topics
        ;;
    consume)
        consume_messages
        ;;
    status)
        show_status
        ;;
    clean)
        clean_all
        ;;
    troubleshoot)
        troubleshoot
        ;;
    *)
        usage
        exit 1
        ;;
esac
