#!/bin/bash
# Quick check: Did the bot run today?

echo "================================================"
echo "🤖 Did the Prenotami Bot Run Today?"
echo "================================================"
echo ""

PROJECT_DIR="/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin"
TODAY=$(date +%Y-%m-%d)

# Quick status
echo "📅 Checking for today's date: $TODAY"
echo ""

# Check 1: Cron log
echo "1️⃣  Checking cron log..."
if [ -f "${PROJECT_DIR}/cron_bot.log" ]; then
    TODAY_RUNS=$(grep "$TODAY" "${PROJECT_DIR}/cron_bot.log" 2>/dev/null | wc -l | xargs)
    if [ "$TODAY_RUNS" -gt 0 ]; then
        echo "   ✅ YES! Found $TODAY_RUNS log entries from today"
        echo ""
        echo "   Latest entries:"
        grep "$TODAY" "${PROJECT_DIR}/cron_bot.log" | tail -5 | sed 's/^/   /'
    else
        echo "   ❌ NO - No entries from today"
    fi
else
    echo "   ⚠️  No cron_bot.log file found"
fi
echo ""

# Check 2: Screenshots
echo "2️⃣  Checking for today's screenshots..."
TODAY_SIMPLE=$(date +%Y%m%d)
SCREENSHOT_COUNT=$(find "${PROJECT_DIR}" -name "screenshot_*${TODAY_SIMPLE}*.png" 2>/dev/null | wc -l | xargs)

if [ "$SCREENSHOT_COUNT" -gt 0 ]; then
    echo "   ✅ YES! Found $SCREENSHOT_COUNT screenshot(s) from today"
    echo ""
    echo "   Latest screenshots:"
    find "${PROJECT_DIR}" -name "screenshot_*${TODAY_SIMPLE}*.png" 2>/dev/null | sort -r | head -3 | xargs -I {} basename {} | sed 's/^/   /'
else
    echo "   ❌ NO - No screenshots from today"
fi
echo ""

# Check 3: Bot log
echo "3️⃣  Checking bot execution log..."
if [ -f "${PROJECT_DIR}/prenotami_bot.log" ]; then
    BOT_RUNS=$(grep "$TODAY" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | wc -l | xargs)
    if [ "$BOT_RUNS" -gt 0 ]; then
        echo "   ✅ YES! Found $BOT_RUNS log entries from today"
        
        # Check for key events
        if grep "$TODAY" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | grep -q "Login successful"; then
            echo "   ✅ Bot logged in successfully"
        fi
        
        if grep "$TODAY" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | grep -q "No available slots"; then
            echo "   ℹ️  No slots available (normal - will try again)"
        fi
        
        if grep "$TODAY" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | grep -q -i "slot.*found\|available.*slot"; then
            echo "   🎉 SLOT WAS FOUND! Check screenshots!"
        fi
        
        if grep "$TODAY" "${PROJECT_DIR}/prenotami_bot.log" 2>/dev/null | grep -q "ERROR"; then
            echo "   ⚠️  Some errors occurred - check logs"
        fi
    else
        echo "   ❌ NO - No entries from today"
    fi
else
    echo "   ⚠️  No prenotami_bot.log file found"
fi
echo ""

# Summary
echo "================================================"
echo "📊 SUMMARY"
echo "================================================"
echo ""

if [ "$TODAY_RUNS" -gt 0 ] || [ "$SCREENSHOT_COUNT" -gt 0 ]; then
    echo "✅ YES - The bot ran today!"
    echo ""
    echo "Next steps:"
    echo "  • Check screenshots: ls -lt ${PROJECT_DIR}/screenshot_*${TODAY_SIMPLE}*.png"
    echo "  • View full logs: tail -50 ${PROJECT_DIR}/cron_bot.log"
    echo "  • Detailed status: ${PROJECT_DIR}/check_bot_status.sh"
else
    echo "❌ NO - The bot has not run yet today"
    echo ""
    echo "Possible reasons:"
    echo "  • It's before 7:00 AM (bot runs at 7 AM)"
    echo "  • Computer was asleep at 7:00 AM"
    echo "  • Cron job is not active"
    echo ""
    echo "To check:"
    echo "  • Verify cron: crontab -l"
    echo "  • Check time: date"
    echo "  • Run manually: ${PROJECT_DIR}/run_bot_with_limit.sh"
fi
echo ""
echo "================================================"

