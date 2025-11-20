#!/bin/bash
# Convenient script to run the scheduler

# Navigate to project directory
cd "$(dirname "$0")"

echo "=========================================="
echo "Prenotami Bot Scheduler"
echo "=========================================="
echo ""
echo "Starting scheduler..."
echo "The bot will run every day at 7:00 AM"
echo ""
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

# Activate virtual environment and run scheduler
source venv/bin/activate
python3 scheduler.py

