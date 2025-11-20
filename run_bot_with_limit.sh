#!/bin/bash
# Wrapper script that runs the bot for a limited number of days

# Configuration
PROJECT_DIR="/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin"
DAYS_TO_RUN=3
START_DATE_FILE="${PROJECT_DIR}/.cron_start_date"

cd "$PROJECT_DIR"

# Check if this is the first run
if [ ! -f "$START_DATE_FILE" ]; then
    # First run - save the start date
    date +%s > "$START_DATE_FILE"
    echo "$(date): First run - starting 3-day trial period" >> "${PROJECT_DIR}/cron_bot.log"
fi

# Read the start date
START_DATE=$(cat "$START_DATE_FILE")
CURRENT_DATE=$(date +%s)
DAYS_ELAPSED=$(( (CURRENT_DATE - START_DATE) / 86400 ))

echo "$(date): Day $((DAYS_ELAPSED + 1)) of ${DAYS_TO_RUN}" >> "${PROJECT_DIR}/cron_bot.log"

# Check if we should still run
if [ $DAYS_ELAPSED -lt $DAYS_TO_RUN ]; then
    echo "$(date): Running bot (day $((DAYS_ELAPSED + 1))/${DAYS_TO_RUN})" >> "${PROJECT_DIR}/cron_bot.log"
    
    # Activate virtual environment and run the bot
    source "${PROJECT_DIR}/venv/bin/activate"
    python3 "${PROJECT_DIR}/prenotami_bot.py" >> "${PROJECT_DIR}/cron_bot.log" 2>&1
    
    echo "$(date): Bot execution completed" >> "${PROJECT_DIR}/cron_bot.log"
    
    # Send email notification
    echo "$(date): Sending email notification..." >> "${PROJECT_DIR}/cron_bot.log"
    python3 "${PROJECT_DIR}/send_email_notification.py" >> "${PROJECT_DIR}/cron_bot.log" 2>&1
else
    echo "$(date): 3-day period completed. Removing cron job..." >> "${PROJECT_DIR}/cron_bot.log"
    
    # Remove the cron job
    crontab -l | grep -v "run_bot_with_limit.sh" | crontab -
    
    echo "$(date): ✓ Cron job removed automatically" >> "${PROJECT_DIR}/cron_bot.log"
    echo "$(date): If you want to continue, run: ./run_scheduler.sh" >> "${PROJECT_DIR}/cron_bot.log"
    
    # Clean up
    rm -f "$START_DATE_FILE"
fi

