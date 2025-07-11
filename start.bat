@echo off
echo 🏦 === VPBank Transaction Simulator ===
echo.

echo 📦 Installing requirements...
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    echo 💡 Try: pip install confluent-kafka python-dotenv faker
    pause
    exit /b 1
)

echo.
echo ✅ Requirements installed successfully
echo.
echo 🚀 Starting simulator...
echo 💡 Make sure Kafka is running: docker-compose up -d
echo.

python -m src.main

echo.
echo ✅ Simulator finished
pause
