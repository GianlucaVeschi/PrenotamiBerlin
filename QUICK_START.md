# Quick Start Guide

## ✅ Setup Complete!

Your bot is ready to use! Here's how to get started:

## 🚀 Run the Bot Manually (Test)

```bash
cd /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin
source venv/bin/activate
python3 prenotami_bot.py
```

This will run the bot once to test if everything works.

## ⏰ Run with Scheduler (Automatic at 7:00 AM)

To run the bot automatically every day at 7:00 AM:

```bash
cd /Users/gianluca.veschi@getyourguide.com/VScodeProjects/PrenotamiBerlin
source venv/bin/activate
python3 scheduler.py
```

**Important:** Keep the terminal window open and your computer on at 7:00 AM!

### What the Scheduler Does:
- ✅ Runs the bot every day at 7:00 AM
- ✅ Logs all actions to `scheduler.log` and `prenotami_bot.log`
- ✅ Takes screenshots at each step
- ✅ Keeps running until you stop it (Ctrl+C)

## 📊 Check the Results

### View Logs
```bash
# View the latest bot activity
tail -20 prenotami_bot.log

# Follow the log in real-time
tail -f prenotami_bot.log
```

### Check Screenshots
Screenshots are saved in the project directory with timestamps:
- `screenshot_availability_page_*.png` - The appointment availability page
- `screenshot_booking_attempt_*.png` - If a slot was found and booking was attempted
- `screenshot_*_error_*.png` - Any errors encountered

## 🎯 Current Status

The bot successfully:
1. ✅ Logs into your account
2. ✅ Navigates to the Prenota (Book) section
3. ✅ Clicks on ID card appointment booking
4. ✅ Checks for available slots
5. ⚠️  Currently no slots available (expected - try at 7:00 AM!)

## 📅 Best Time to Run

According to the embassy website:
- **7:00 AM** - System opens a new day for bookings (if it's a working day)
- The bot is configured to run automatically at this time

## 🔧 Troubleshooting

### Bot gets stuck
- Check the screenshots to see what the bot sees
- Check the logs for error messages

### No slots found at 7:00 AM
- High competition - the bot will keep trying daily
- Consider running multiple attempts: 7:00, 7:01, 7:02, etc.

### Need to update credentials
Edit the `.env` file:
```bash
nano .env
```

## ⚙️ Advanced Options

### Run in Headless Mode (No Browser Window)
Edit the bot file and change:
```python
bot = PrenotamiBot(email=email, password=password, headless=True)
```

### Add More Time Slots
Edit `scheduler.py` and add:
```python
schedule.every().day.at("07:00").do(run_bot_job)
schedule.every().day.at("07:01").do(run_bot_job)
schedule.every().day.at("07:02").do(run_bot_job)
```

### Run as Background Service (macOS)
See the main `README.md` for instructions on setting up with cron or launchd.

## 📞 What Happens When a Slot is Found?

When the bot finds an available slot:
1. It will click on the slot
2. Take a screenshot
3. Log: "Booking attempt completed! CHECK SCREENSHOTS"
4. ⚠️ You may need to complete additional steps manually (payment, confirmation, etc.)

## 💡 Tips

1. **Keep computer on at 7:00 AM** - The scheduler needs to be running
2. **Check logs daily** - Make sure the bot is running correctly
3. **Monitor screenshots** - Visual confirmation of bot actions
4. **Be patient** - Slots fill up quickly, may take multiple days
5. **Act fast** - If bot finds a slot, complete the booking quickly!

## 🎉 Good Luck!

The bot will help you secure an appointment. Remember:
- Run at 7:00 AM when new slots appear
- Check screenshots for confirmation
- Complete any manual steps immediately

Happy booking! 🇮🇹

