@echo off
REM Start Kafka in KRaft mode for Windows
REM This script initializes and starts Kafka without Zookeeper

set KAFKA_HOME=C:\kafka
set CONFIG_FILE=%KAFKA_HOME%\config\kraft\server.properties
set LOG_DIR=C:\tmp\kraft-combined-logs

echo Starting Kafka in KRaft mode...

REM Generate a cluster UUID
for /f %%i in ('kafka-storage.bat random-uuid') do set KAFKA_CLUSTER_ID=%%i
echo Generated Cluster ID: %KAFKA_CLUSTER_ID%

REM Format the storage directory
echo Formatting storage directory...
kafka-storage.bat format -t %KAFKA_CLUSTER_ID% -c %CONFIG_FILE%

REM Start Kafka server
echo Starting Kafka server...
kafka-server-start.bat %CONFIG_FILE%

echo Kafka started successfully in KRaft mode!
echo Bootstrap server: localhost:9092
echo Controller: localhost:9093

pause
