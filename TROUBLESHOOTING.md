# Troubleshooting Guide

## Issue: Bot Gets Stuck at "Get LATEST chromedriver version"

This happens when the automatic ChromeDriver download is slow or fails.

### Quick Fix (Recommended for macOS)

Run these commands:

```bash
# Install ChromeDriver via Homebrew
brew install chromedriver

# Remove macOS quarantine flag
xattr -d com.apple.quarantine $(which chromedriver)

# Verify it works
chromedriver --version
```

Then run the bot again:
```bash
python3 prenotami_bot.py
```

### Alternative: Manual Download

1. Check your Chrome version:
   - Open Chrome
   - Go to `chrome://version/`
   - Note the version number (e.g., 119.0.6045.123)

2. Download matching ChromeDriver:
   - Visit: https://googlechromelabs.github.io/chrome-for-testing/
   - Download the version matching your Chrome
   - For macOS: Download the `chromedriver-mac-x64` or `chromedriver-mac-arm64` (for M1/M2)

3. Install ChromeDriver:
   ```bash
   # Unzip the downloaded file
   unzip chromedriver-mac-*.zip
   
   # Move to /usr/local/bin
   sudo mv chromedriver /usr/local/bin/
   
   # Make it executable
   sudo chmod +x /usr/local/bin/chromedriver
   
   # Remove quarantine (macOS security)
   xattr -d com.apple.quarantine /usr/local/bin/chromedriver
   ```

4. Verify installation:
   ```bash
   chromedriver --version
   ```

### Alternative: Use Firefox Instead

If Chrome continues to have issues, we can modify the bot to use Firefox:

1. Install Firefox and geckodriver:
   ```bash
   brew install firefox geckodriver
   ```

2. Let me know and I'll update the bot to use Firefox instead.

## Issue: Login Fails

### Check Credentials
Make sure your `.env` file has the correct format:
```
EMAIL=your@email.com
PASSWORD=yourpassword
```

No quotes, no spaces around the `=` sign.

### Check Website
Try logging in manually to ensure:
- Your credentials are correct
- The website isn't down
- There's no CAPTCHA

## Issue: Elements Not Found

The website structure might have changed. To debug:

1. Check the screenshots generated in the project folder
2. Look at what the bot sees
3. Update the XPath selectors if needed

## Issue: No Available Slots

This is normal! Slots fill up quickly. The bot will keep trying daily at 7:00 AM.

## Still Having Issues?

Run the test script to diagnose:
```bash
python3 test_setup.py
```

This will check:
- Python version
- Package installations
- Chrome/ChromeDriver versions
- Network connectivity

