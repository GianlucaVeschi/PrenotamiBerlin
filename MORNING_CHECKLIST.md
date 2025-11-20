# ☀️ Morning Checklist - After 7:00 AM

## 🚀 Quick Check (30 seconds)

Run this one simple command after 7:05 AM:

```bash
~/VScodeProjects/PrenotamiBerlin/check_bot_status.sh
```

This will automatically check:
- ✅ If the cron job is active
- ✅ If the bot ran today
- ✅ Which day you're on (1, 2, or 3)
- ✅ If screenshots were created
- ✅ If any slots were found
- ✅ If there were any errors

## 📋 Manual Check (if you prefer)

### 1. Check if bot ran (most important!)

```bash
tail -20 ~/VScodeProjects/PrenotamiBerlin/cron_bot.log
```

**Look for:**
- ✅ Today's date and "Running bot"
- ✅ "Day X of 3"

### 2. Check bot execution log

```bash
tail -30 ~/VScodeProjects/PrenotamiBerlin/prenotami_bot.log
```

**Look for:**
- ✅ "Login successful"
- ✅ "Navigated to booking section"
- ✅ "Clicked on ID card appointment booking"
- ⚠️ "No available slots" (normal - keep trying)
- 🎉 "Found available slot" (ACTION REQUIRED!)

### 3. View today's screenshots

```bash
# List today's screenshots
ls -lt ~/VScodeProjects/PrenotamiBerlin/screenshot_* | head -5

# Open the latest availability screenshot
open ~/VScodeProjects/PrenotamiBerlin/screenshot_availability_page_*.png
```

**Look for:**
- A popup/message about availability
- Available dates in a calendar
- Any clickable slots

### 4. Check which day you're on

```bash
grep "Day" ~/VScodeProjects/PrenotamiBerlin/cron_bot.log | tail -1
```

Should show: "Day 1 of 3", "Day 2 of 3", or "Day 3 of 3"

## 🎯 What to Look For

### ✅ SUCCESS - Bot ran correctly
You'll see:
- New entries in `cron_bot.log` with today's date
- New screenshots with today's timestamp
- "Login successful" in the bot log
- "No available slots" message (normal if no appointments)

### 🎉 JACKPOT - Slot found!
You'll see:
- Log message about "available slot"
- Screenshot showing available dates
- **ACTION:** Complete the booking IMMEDIATELY on the website!

### ⚠️ PROBLEM - Bot didn't run
You'll see:
- No new log entries today
- No new screenshots today
- Last log entry is from yesterday

**Fix:**
```bash
# Check if cron job exists
crontab -l

# Check if computer was asleep
pmset -g log | grep -i sleep

# Run manually to test
~/VScodeProjects/PrenotamiBerlin/run_bot_with_limit.sh
```

## 📊 Quick Status Commands

| What to check | Command |
|---------------|---------|
| Did bot run? | `tail -5 ~/VScodeProjects/PrenotamiBerlin/cron_bot.log` |
| Which day? | `grep "Day" ~/VScodeProjects/PrenotamiBerlin/cron_bot.log \| tail -1` |
| Latest screenshots | `ls -lt ~/VScodeProjects/PrenotamiBerlin/screenshot_* \| head -3` |
| Any slots found? | `grep "slot" ~/VScodeProjects/PrenotamiBerlin/prenotami_bot.log \| tail -5` |
| Any errors? | `grep "ERROR" ~/VScodeProjects/PrenotamiBerlin/prenotami_bot.log \| tail -5` |
| Is cron active? | `crontab -l` |

## 🔔 If Slot is Found

1. **DON'T PANIC** - You have time, but act quickly
2. **Open latest screenshot** to verify
3. **Go to website** manually: https://prenotami.esteri.it/
4. **Login** with your credentials
5. **Navigate** to Prenota → ID card booking
6. **Complete** the booking (payment, confirmation, etc.)
7. **Screenshot** your confirmation
8. **Done!** 🎉

## ⏰ Timeline

- **Before 7:00 AM:** Nothing to check
- **7:00-7:05 AM:** Bot is running (wait a bit)
- **After 7:05 AM:** Check status with the commands above

## 📅 3-Day Schedule Reminder

- **Day 1:** Tomorrow (Nov 21)
- **Day 2:** Saturday (Nov 22)
- **Day 3:** Sunday (Nov 23) - Last day
- **Day 4+:** Cron automatically stops

## 🆘 Troubleshooting

### Computer was asleep at 7 AM
Cron won't run if computer is asleep!
- **Solution:** Keep computer awake or run manually

### No log file created
Bot hasn't run yet
- **Solution:** Wait until after 7:05 AM

### Errors in log
Something went wrong during execution
- **Solution:** Check TROUBLESHOOTING.md or run manually to see error

### Cron job disappeared
3-day period completed
- **Solution:** This is expected after day 3! ✅

## 💡 Pro Tips

1. **Set phone alarm** for 7:05 AM
2. **Check immediately** - don't wait hours
3. **Keep screenshots** of successful booking
4. **Review logs** even if it seems to work
5. **Test manually** once before relying on cron

## 🎯 The One Command You Need

Just remember this:

```bash
~/VScodeProjects/PrenotamiBerlin/check_bot_status.sh
```

Run it every morning after 7:05 AM for the next 3 days!

---

**Set your alarm now!** ⏰ 7:05 AM for next 3 days

