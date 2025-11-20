#!/bin/bash
# Quick status check script - run this after 7:00 AM to verify the bot ran

echo "========================================"
echo "🤖 Prenotami Bot Status Checker"
echo "========================================"
echo ""

PROJECT_DIR="/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin"
cd "$PROJECT_DIR"

# Check 1: Cron job exists
echo "1️⃣  Checking if cron job is active..."
if crontab -l 2>/dev/null | grep -q "run_bot_with_limit.sh"; then
    echo "   ✅ Cron job is active"
else
    echo "   ⚠️  Cron job not found (may have completed 3 days)"
fi
echo ""

# Check 2: Cron log exists and has recent entries
echo "2️⃣  Checking cron bot log..."
if [ -f "${PROJECT_DIR}/cron_bot.log" ]; then
    echo "   ✅ Log file exists"
    echo ""
    echo "   📋 Last 10 log entries:"
    tail -10 "${PROJECT_DIR}/cron_bot.log" | sed 's/^/      /'
else
    echo "   ⚠️  No log file found yet (bot hasn't run)"
fi
echo ""

# Check 3: Check which day we're on
echo "3️⃣  Checking current day of 3-day cycle..."
if [ -f "${PROJECT_DIR}/.cron_start_date" ]; then
    START_DATE=$(cat "${PROJECT_DIR}/.cron_start_date")
    CURRENT_DATE=$(date +%s)
    DAYS_ELAPSED=$(( (CURRENT_DATE - START_DATE) / 86400 ))
    echo "   📅 Currently on day $((DAYS_ELAPSED + 1)) of 3"
else
    echo "   ℹ️  Not started yet (will start at 7:00 AM)"
fi
echo ""

# Check 4: Check for today's screenshots
echo "4️⃣  Checking for today's screenshots..."
TODAY=$(date +%Y%m%d)
SCREENSHOTS=$(find "${PROJECT_DIR}" -name "screenshot_*${TODAY}*.png" 2>/dev/null | wc -l | xargs)
if [ "$SCREENSHOTS" -gt 0 ]; then
    echo "   ✅ Found ${SCREENSHOTS} screenshot(s) from today"
    echo ""
    echo "   📸 Latest screenshots:"
    ls -lt "${PROJECT_DIR}"/screenshot_*${TODAY}*.png 2>/dev/null | head -3 | awk '{print "      " $9}' | xargs -I {} basename {}
else
    echo "   ⚠️  No screenshots from today yet"
fi
echo ""

# Check 5: Check main bot log
echo "5️⃣  Checking main bot log for today's activity..."
if [ -f "${PROJECT_DIR}/prenotami_bot.log" ]; then
    TODAY_LOGS=$(grep "$(date +%Y-%m-%d)" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | wc -l | xargs)
    if [ "$TODAY_LOGS" -gt 0 ]; then
        echo "   ✅ Found ${TODAY_LOGS} log entries from today"
        echo ""
        echo "   📋 Recent bot activity:"
        grep "$(date +%Y-%m-%d)" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | tail -5 | sed 's/^/      /'
    else
        echo "   ℹ️  No activity from today yet"
    fi
else
    echo "   ℹ️  No bot log file yet"
fi
echo ""

# Check 6: Look for success/failure indicators
echo "6️⃣  Checking for booking results..."
if [ -f "${PROJECT_DIR}/prenotami_bot.log" ]; then
    if grep -q "Login successful" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | tail -1; then
        echo "   ✅ Bot logged in successfully"
    fi
    
    if grep -q "No available slots" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | tail -1; then
        echo "   ℹ️  No slots available (expected - will try again tomorrow)"
    fi
    
    if grep -q "available slot" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | tail -1; then
        echo "   🎉 SLOT FOUND! Check screenshots immediately!"
    fi
    
    if grep -q "ERROR" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | tail -20; then
        echo "   ⚠️  Errors detected - check logs for details"
    fi
else
    echo "   ℹ️  Bot hasn't run yet"
fi
echo ""

# Summary
echo "========================================"
echo "📊 SUMMARY"
echo "========================================"
echo ""

# Determine overall status
if [ -f "${PROJECT_DIR}/cron_bot.log" ] && [ "$SCREENSHOTS" -gt 0 ]; then
    echo "✅ Status: Bot ran successfully today!"
    echo ""
    echo "👉 Next steps:"
    echo "   1. Check latest screenshots for available slots"
    echo "   2. If slot found, complete booking immediately"
    echo "   3. Bot will run again tomorrow at 7:00 AM"
elif [ -f "${PROJECT_DIR}/cron_bot.log" ]; then
    echo "⚠️  Status: Bot started but may have encountered issues"
    echo ""
    echo "👉 Next steps:"
    echo "   1. Review the logs above for errors"
    echo "   2. Check TROUBLESHOOTING.md for solutions"
else
    echo "ℹ️  Status: Bot hasn't run yet"
    echo ""
    echo "👉 Next steps:"
    echo "   1. Wait until after 7:00 AM"
    echo "   2. Run this script again after 7:05 AM"
    echo "   3. Make sure computer is on and awake at 7:00 AM"
fi
echo ""
echo "========================================"
echo ""
echo "Commands for more details:"
echo "  📋 Full cron log:  tail -50 ${PROJECT_DIR}/cron_bot.log"
echo "  📋 Full bot log:   tail -50 ${PROJECT_DIR}/prenotami_bot.log"
echo "  📸 View screenshots: open ${PROJECT_DIR}/screenshot_*.png"
echo ""

