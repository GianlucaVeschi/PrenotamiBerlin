#!/usr/bin/env python3
"""
Test script to verify the bot setup
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check Python version"""
    print("="*60)
    print("Checking Python version...")
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠️  WARNING: Python 3.8+ recommended")
    print()

def check_package(package_name):
    """Check if a package is installed"""
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"✗ {package_name} - NOT INSTALLED")
        return False
    else:
        print(f"✓ {package_name} - installed")
        return True

def check_packages():
    """Check required packages"""
    print("="*60)
    print("Checking required packages...")
    packages = ["selenium", "dotenv", "schedule"]
    all_good = True
    for pkg in packages:
        if not check_package(pkg):
            all_good = False
    if not all_good:
        print("\n⚠️  Install missing packages: pip install -r requirements.txt")
    print()

def check_chrome():
    """Check Chrome installation"""
    print("="*60)
    print("Checking Chrome browser...")
    try:
        # Try to get Chrome version (macOS)
        result = subprocess.run(
            ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ {result.stdout.strip()}")
        else:
            print("✗ Chrome not found")
    except Exception as e:
        print(f"✗ Chrome check failed: {e}")
    print()

def check_chromedriver():
    """Check ChromeDriver installation"""
    print("="*60)
    print("Checking ChromeDriver...")
    try:
        result = subprocess.run(
            ['chromedriver', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ {result.stdout.strip()}")
        else:
            print("✗ ChromeDriver not found")
            print("\n💡 Install with: brew install chromedriver")
            print("   Then run: xattr -d com.apple.quarantine $(which chromedriver)")
    except FileNotFoundError:
        print("✗ ChromeDriver not found in PATH")
        print("\n💡 Install with: brew install chromedriver")
        print("   Then run: xattr -d com.apple.quarantine $(which chromedriver)")
    except Exception as e:
        print(f"✗ ChromeDriver check failed: {e}")
    print()

def check_env_file():
    """Check .env file"""
    print("="*60)
    print("Checking .env file...")
    import os
    if os.path.exists('.env'):
        print("✓ .env file exists")
        from dotenv import load_dotenv
        load_dotenv()
        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')
        
        if email and password:
            print(f"✓ EMAIL: {email}")
            print(f"✓ PASSWORD: {'*' * len(password)}")
        else:
            print("⚠️  EMAIL or PASSWORD not set in .env")
    else:
        print("✗ .env file not found")
        print("\n💡 Create .env file with:")
        print("   EMAIL=your@email.com")
        print("   PASSWORD=yourpassword")
    print()

def test_selenium():
    """Test Selenium with Chrome"""
    print("="*60)
    print("Testing Selenium with Chrome...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        print("Attempting to create Chrome driver...")
        driver = webdriver.Chrome(options=options)
        print("✓ Chrome driver created successfully!")
        
        print("Testing navigation...")
        driver.get("https://www.google.com")
        print(f"✓ Navigated to: {driver.current_url}")
        
        driver.quit()
        print("✓ Selenium test PASSED!")
        
    except Exception as e:
        print(f"✗ Selenium test FAILED: {e}")
        print("\n💡 Try installing ChromeDriver manually:")
        print("   brew install chromedriver")
        print("   xattr -d com.apple.quarantine $(which chromedriver)")
    print()

def main():
    print("\n" + "="*60)
    print("PRENOTAMI BOT - SETUP TEST")
    print("="*60 + "\n")
    
    check_python_version()
    check_packages()
    check_chrome()
    check_chromedriver()
    check_env_file()
    test_selenium()
    
    print("="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\nIf all checks passed (✓), you're ready to run the bot!")
    print("If any checks failed (✗), follow the suggestions above.")
    print()

if __name__ == "__main__":
    main()

