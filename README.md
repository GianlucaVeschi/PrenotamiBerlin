# Prenotami Berlin - ID Card Appointment Booking Bot

An automated bot to help book appointments on [prenotami.esteri.it](https://prenotami.esteri.it/) for ID card renewals at the Italian embassy/consulate.

## 🎯 Purpose

The embassy's booking system adds new appointment slots every day at 7:00 AM for the next 100 days. This bot automates the booking process to help you secure an appointment during this narrow time window.

## 📋 Features

- Automated login to prenotami.esteri.it
- Navigation to ID card appointment booking section
- Checks for available slots
- Automatic screenshot capture for verification
- Detailed logging of all actions
- Scheduler to run the bot at 7:00 AM daily

## 🚀 Setup Instructions

### 1. Install Python

Make sure you have Python 3.8 or higher installed:

```bash
python3 --version
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Credentials

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   EMAIL=your_email@example.com
   PASSWORD=your_password_here
   ```

### 5. Install Chrome Browser

The bot uses Chrome browser. Make sure you have Google Chrome installed on your system.

## 🏃 Usage

### Option 1: Run Once (Manual Test)

To run the bot once for testing:

```bash
python3 prenotami_bot.py
```

### Option 2: Run with Scheduler (Recommended)

To run the bot automatically at 7:00 AM every day:

```bash
python3 scheduler.py
```

The scheduler will:
- Run the bot immediately once for testing
- Then run it every day at 7:00 AM
- Keep running until you stop it (Ctrl+C)

## 📊 Monitoring

### Logs

Check the log files to see what happened:

```bash
# Bot execution log
tail -f prenotami_bot.log

# Scheduler log
tail -f scheduler.log
```

### Screenshots

The bot automatically takes screenshots at key points:
- `screenshot_login_*` - Login page
- `screenshot_availability_page_*` - Appointment availability page
- `screenshot_booking_attempt_*` - Booking confirmation
- `screenshot_*_error_*` - Error states

Check these screenshots to verify the bot's actions.

## ⚙️ Customization

### Modify Booking Times

Edit `scheduler.py` to add more time slots:

```python
schedule.every().day.at("07:00").do(run_bot_job)
schedule.every().day.at("07:05").do(run_bot_job)  # Backup attempt
schedule.every().day.at("07:10").do(run_bot_job)  # Another backup
```

### Run in Headless Mode

To run the browser in the background (no visible window):

Edit `prenotami_bot.py` or `scheduler.py` and change:
```python
bot = PrenotamiBot(email=email, password=password, headless=True)
```

### Adjust Wait Times

If the website is slow, you can increase wait times in `prenotami_bot.py`:
```python
time.sleep(5)  # Increase from 2 to 5 seconds
```

## 🔧 Troubleshooting

### "Could not find element" errors

The website structure may have changed. Check the screenshots to see what the bot sees, then update the XPath selectors in `prenotami_bot.py`.

### Chrome driver issues

If you get ChromeDriver errors, try:
```bash
pip install --upgrade webdriver-manager
```

### Login fails

1. Verify your credentials in `.env`
2. Check if the website has CAPTCHA
3. Try running with `headless=False` to see what's happening

### No slots available

This is normal! The slots fill up quickly. The bot will keep trying daily at 7:00 AM.

## ⚠️ Important Notes

1. **Website Terms of Service**: Make sure using automation doesn't violate the website's terms of service
2. **Rate Limiting**: The bot includes delays to avoid overwhelming the server
3. **CAPTCHA**: If the website adds CAPTCHA, you may need to solve it manually
4. **Keep Computer On**: For scheduled runs, your computer must be on and awake at 7:00 AM
5. **Internet Connection**: Ensure stable internet connection during bot execution

## 📝 Legal Disclaimer

This bot is for personal use only. The user is responsible for:
- Ensuring compliance with the website's terms of service
- Respecting rate limits and server resources
- Using the bot ethically and responsibly

## 🤝 Contributing

Feel free to improve the bot by:
- Adding better error handling
- Improving element selectors
- Adding notification features (email, SMS, etc.)
- Making it more robust

## 📧 Support

Check the logs and screenshots first. If issues persist, review the website's structure and update the XPath selectors accordingly.

Good luck booking your appointment! 🍀

