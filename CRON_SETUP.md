# ⏰ Cron Job Setup - 3 Day Trial

## ✅ Cron Job Installed!

Your bot is now scheduled to run **automatically at 7:00 AM** for the **next 3 days**.

## 📋 Configuration

- **Schedule:** Every day at 7:00 AM
- **Duration:** 3 days (automatically stops after day 3)
- **Start date:** Recorded on first run
- **Auto-cleanup:** Yes - removes itself after 3 days

## 🔍 How to Check Status

### View the cron job
```bash
crontab -l
```

You should see:
```
0 7 * * * /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/run_bot_with_limit.sh
```

### Monitor the logs
```bash
tail -f /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/cron_bot.log
```

### Check which day you're on
```bash
cat /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/cron_bot.log | grep "Day"
```

## 📊 What Happens Each Day

### Day 1 (First run at 7:00 AM)
- ✅ Script records the start date
- ✅ Runs the bot
- ✅ Logs: "Day 1 of 3"

### Day 2 (7:00 AM)
- ✅ Checks elapsed time
- ✅ Runs the bot
- ✅ Logs: "Day 2 of 3"

### Day 3 (7:00 AM - Last day)
- ✅ Checks elapsed time
- ✅ Runs the bot
- ✅ Logs: "Day 3 of 3"

### Day 4 (7:00 AM)
- ✅ Detects 3 days have passed
- ✅ **Automatically removes the cron job**
- ✅ Logs: "3-day period completed. Removing cron job..."
- ✅ Cleans up tracking files

## 🧪 Test the Script Manually

To test if the script works (without waiting for 7 AM):

```bash
/Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/run_bot_with_limit.sh
```

This will:
1. Run the bot immediately
2. Create the start date tracker
3. Log the execution

## 📁 Files Created

- `.cron_start_date` - Tracks when the 3-day period started
- `cron_bot.log` - Logs all cron executions

## 🛑 How to Stop Early (Manual Override)

If you want to stop before 3 days:

```bash
# Remove the cron job
crontab -r

# Or edit to remove just this job
crontab -e
# Delete the line with "run_bot_with_limit.sh"
# Save and exit
```

## 🔄 How to Extend Beyond 3 Days

### Option 1: Modify the script
```bash
nano /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/run_bot_with_limit.sh
```

Change:
```bash
DAYS_TO_RUN=3
```

To:
```bash
DAYS_TO_RUN=7  # Or any number of days
```

### Option 2: Reset and start over
```bash
# Remove the tracking file
rm /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/.cron_start_date

# The script will start counting from the next run
```

### Option 3: Switch to unlimited scheduler
```bash
# Remove the limited cron job
crontab -r

# Use the unlimited scheduler instead
cd /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin
./run_scheduler.sh
```

## 📧 Notifications (Optional)

macOS might ask for permission for cron to run. If you don't see the bot running at 7 AM:

1. Go to **System Settings** → **Privacy & Security** → **Full Disk Access**
2. Add `/usr/sbin/cron` to the allowed apps

## 🔔 What to Expect

### Before 7:00 AM
- Nothing happens (cron is waiting)

### At 7:00 AM (Each day)
- Cron wakes up
- Runs the wrapper script
- Script checks if within 3-day window
- If yes: runs the bot
- If no: removes the cron job

### After 7:00 AM
- Check the logs: `tail -20 cron_bot.log`
- Check screenshots in the project folder

## 🎯 Next Morning Checklist

Wake up at 7:05 AM and:

1. **Check if it ran:**
   ```bash
   tail -20 ~/VScodeProjects/PrenotamiBerlin/cron_bot.log
   ```

2. **Check screenshots:**
   ```bash
   ls -lt ~/VScodeProjects/PrenotamiBerlin/screenshot_* | head -5
   ```

3. **If a slot was found:**
   - Open the latest screenshot
   - Complete the booking manually ASAP!

## ⚠️ Troubleshooting

### Cron didn't run at 7 AM
```bash
# Check if cron is running
ps aux | grep cron

# Check system logs
log show --predicate 'process == "cron"' --last 1h
```

### Need to check the schedule
```bash
crontab -l
```

### Want to see all logs
```bash
cat /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/cron_bot.log
```

### Script isn't executable
```bash
chmod +x /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin/run_bot_with_limit.sh
```

## 📊 Timeline Example

**Today (Nov 20):**
- ✅ Cron job set up

**Tomorrow (Nov 21 at 7:00 AM):**
- ✅ Day 1: Bot runs, records start date

**Nov 22 at 7:00 AM:**
- ✅ Day 2: Bot runs

**Nov 23 at 7:00 AM:**
- ✅ Day 3: Bot runs (last day)

**Nov 24 at 7:00 AM:**
- ✅ Script detects 3 days passed
- ✅ **Automatically removes cron job**
- ✅ Bot stops running

## 🎉 Success Indicators

You'll know it's working if:
- ✅ `cron_bot.log` shows new entries each day at 7 AM
- ✅ New screenshots appear each morning
- ✅ Log shows "Day X of 3"
- ✅ After day 3, cron job is removed automatically

## 💡 Pro Tip

Set a reminder on your phone for **7:05 AM** for the next 3 days to check if a slot was found!

---

**Current Status:** ✅ Cron job active and scheduled for next 3 days
**Next run:** Tomorrow at 7:00 AM
**Auto-stop:** After 3 days

