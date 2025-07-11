@echo off
REM Development helper script for VPBank Transaction Simulator

if "%1"=="" goto usage
if "%1"=="help" goto usage
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="logs" goto logs
if "%1"=="logs-sim" goto logs_sim
if "%1"=="logs-kafka" goto logs_kafka
if "%1"=="build" goto build
if "%1"=="topics" goto topics
if "%1"=="status" goto status
if "%1"=="clean" goto clean
goto usage

:usage
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   start        Start all services
echo   stop         Stop all services
echo   restart      Restart all services
echo   logs         Show logs for all services
echo   logs-sim     Show logs for transaction simulator only
echo   logs-kafka   Show logs for Kafka only
echo   build        Build the transaction simulator image
echo   topics       List Kafka topics
echo   status       Show service status
echo   clean        Stop and remove all containers and volumes
echo.
goto end

:start
echo Starting VPBank Transaction Simulator...
docker-compose up -d
echo Services started successfully!
echo Kafka UI: http://localhost:8080
goto end

:stop
echo Stopping services...
docker-compose down
echo Services stopped.
goto end

:restart
echo Restarting services...
docker-compose down
docker-compose up -d
echo Services restarted successfully!
goto end

:logs
docker-compose logs -f
goto end

:logs_sim
docker-compose logs -f txn-simulator
goto end

:logs_kafka
docker-compose logs -f kafka
goto end

:build
echo Building transaction simulator image...
docker-compose build txn-simulator
echo Image built successfully!
goto end

:topics
echo Kafka topics:
docker exec kafka /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
goto end

:status
echo Service Status:
docker-compose ps
goto end

:clean
echo Cleaning up all containers and volumes...
docker-compose down -v
docker system prune -f
echo Cleanup completed.
goto end

:end
