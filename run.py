#!/usr/bin/env python3
"""
Setup and run script for VPBank Transaction Simulator
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def run_simulator():
    """Run the transaction simulator"""
    print("🚀 Starting VPBank Transaction Simulator...")
    try:
        # Change to the project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Run the simulator as a module
        subprocess.run([sys.executable, '-m', 'src.main'])
        
    except KeyboardInterrupt:
        print("\n✅ Simulator stopped by user")
    except Exception as e:
        print(f"❌ Error running simulator: {e}")
        print("💡 Make sure Kafka is running: docker-compose up -d kafka")

def main():
    """Main setup function"""
    print("🏦 === VPBank Transaction Simulator Setup ===")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('src/main.py'):
        print("❌ Error: Please run this script from the vpbank-txn-simulator directory")
        print("💡 Navigate to the project folder and try again")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("💡 Try running: pip install confluent-kafka python-dotenv faker")
        sys.exit(1)
    
    print()
    print("✅ Setup complete! Starting simulator...")
    print("💡 Make sure Kafka is running first:")
    print("   docker-compose up -d")
    print()
    
    # Run simulator
    run_simulator()

if __name__ == "__main__":
    main()
